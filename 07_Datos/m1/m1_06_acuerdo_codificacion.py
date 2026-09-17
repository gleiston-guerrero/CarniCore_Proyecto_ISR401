"""
m1_06_acuerdo_codificacion.py
Corrección M1, Fase 2 -- CarniCore.

Calcula la concordancia entre las tres personas codificadoras de la Tabla S1 y
produce la codificación de consenso.

Para cada dimensión (L, R, G, C) por separado:
  - prevalencia de cada codificador (cuántos de los 21 RF marcó);
  - acuerdo bruto de los tres (RF en que las tres coinciden);
  - kappa de Cohen y acuerdo bruto de cada par;
  - kappa de Fleiss de las tres personas.

Consenso: mayoría simple (>= 2 de 3), regla fijada antes de calcular nada.

Nota sobre kappa: con prevalencias muy desequilibradas kappa baja aunque el
acuerdo bruto sea alto (paradoja de Feinstein y Cicchetti, 1990), y queda
indefinido si una dimensión es constante para un par. Por eso se informan
siempre el acuerdo bruto, el kappa y, como referencia robusta a la prevalencia,
PABAK = 2 x acuerdo bruto - 1. Las hojas originales no se modifican.

Entradas:  07_Datos/m1/codificacion_S1/hoja_codificador_{A,B,C}.csv
           07_Datos/m1/codificacion_S1_plantilla.csv
Salidas:   <salida>/codificacion_S1_consenso.csv
               rf_id,L,R,G,C,unanime
           <salida>/discrepancias_S1.csv
               rf_id,dimension,A,B,C,consenso
           <salida>/acuerdo_S1.json

Uso (desde la raíz del repositorio):
    python 07_Datos/m1/m1_06_acuerdo_codificacion.py
    python 07_Datos/m1/m1_06_acuerdo_codificacion.py --salida <carpeta>
"""

import argparse
import csv
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
M1 = RAIZ / "07_Datos" / "m1"
CODIF = M1 / "codificacion_S1"
PLANTILLA = M1 / "codificacion_S1_plantilla.csv"
CODIFICADORES = ["A", "B", "C"]
DIMENSIONES = ["L", "R", "G", "C"]


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def leer_csv(ruta):
    if not ruta.exists():
        fallar(f"no existe {ruta.relative_to(RAIZ)}")
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def leer_hoja(letra, plantilla):
    ruta = CODIF / f"hoja_codificador_{letra}.csv"
    filas = leer_csv(ruta)
    if [f["rf_id"] for f in filas] != [f["rf_id"] for f in plantilla]:
        fallar(f"hoja {letra}: los RF o su orden no coinciden con la plantilla")
    for f in filas:
        for d in DIMENSIONES:
            if f[d] not in ("0", "1"):
                fallar(f"hoja {letra}, {f['rf_id']}, dimensión {d}: valor {f[d]!r}; se esperaba 0 o 1")
        if sum(int(f[d]) for d in DIMENSIONES) == 0:
            fallar(f"hoja {letra}, {f['rf_id']}: ninguna dimensión marcada")
        for col in ("palabras_eliminadas", "palabras_anadidas"):
            original = next(x[col] for x in plantilla if x["rf_id"] == f["rf_id"])
            if f[col] != original:
                fallar(f"hoja {letra}, {f['rf_id']}: la columna {col} fue modificada")
    return {f["rf_id"]: {d: int(f[d]) for d in DIMENSIONES} for f in filas}, ruta


def kappa_cohen(x, y):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    px, py = sum(x) / n, sum(y) / n
    pe = px * py + (1 - px) * (1 - py)
    return (None if pe == 1 else round((po - pe) / (1 - pe), 4)), round(po, 4)


def kappa_fleiss(columnas):
    n, m = len(columnas[0]), len(columnas)
    p = sum(sum(c) for c in columnas) / (n * m)
    pe = p * p + (1 - p) ** 2
    concordancia = []
    for i in range(n):
        k = sum(c[i] for c in columnas)
        concordancia.append((k * (k - 1) + (m - k) * (m - k - 1)) / (m * (m - 1)))
    p_barra = sum(concordancia) / n
    return (None if pe == 1 else round((p_barra - pe) / (1 - pe), 4)), round(p_barra, 4)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=CODIF,
                        help="carpeta de salida (por defecto 07_Datos/m1/codificacion_S1)")
    args = parser.parse_args()

    plantilla = leer_csv(PLANTILLA)
    ids = [f["rf_id"] for f in plantilla]
    hojas, rutas = {}, {}
    for letra in CODIFICADORES:
        hojas[letra], rutas[letra] = leer_hoja(letra, plantilla)

    resumen = {"n_rf": len(ids), "codificadores": CODIFICADORES,
               "regla_consenso": "mayoría simple (>= 2 de 3)",
               "hojas": {l: hashlib.sha256(rutas[l].read_bytes()).hexdigest() for l in CODIFICADORES},
               "dimensiones": {}}

    for d in DIMENSIONES:
        columnas = [[hojas[l][rf][d] for rf in ids] for l in CODIFICADORES]
        acuerdo_total = sum(len(set(col[i] for col in columnas)) == 1 for i in range(len(ids))) / len(ids)
        pares = {}
        for (i, li), (j, lj) in combinations(enumerate(CODIFICADORES), 2):
            k, po = kappa_cohen(columnas[i], columnas[j])
            pares[f"{li}_vs_{lj}"] = {"kappa_cohen": k, "acuerdo_bruto": po}
        kf, p_barra = kappa_fleiss(columnas)
        resumen["dimensiones"][d] = {
            "marcas_por_codificador": {l: sum(columnas[i]) for i, l in enumerate(CODIFICADORES)},
            "acuerdo_unanime": round(acuerdo_total, 4),
            "pabak_unanime": round(2 * acuerdo_total - 1, 4),
            "pares": pares,
            "kappa_fleiss": kf,
            "acuerdo_medio_fleiss": p_barra,
        }

    consenso, discrepancias = [], []
    for rf in ids:
        fila = {"rf_id": rf}
        unanime = 1
        for d in DIMENSIONES:
            votos = [hojas[l][rf][d] for l in CODIFICADORES]
            fila[d] = 1 if sum(votos) >= 2 else 0
            if len(set(votos)) > 1:
                unanime = 0
                discrepancias.append({"rf_id": rf, "dimension": d,
                                      **{l: votos[i] for i, l in enumerate(CODIFICADORES)},
                                      "consenso": fila[d]})
        fila["unanime"] = unanime
        consenso.append(fila)

    resumen["rf_unanimes"] = sum(f["unanime"] for f in consenso)
    resumen["n_discrepancias"] = len(discrepancias)
    resumen["marcas_consenso"] = {d: sum(f[d] for f in consenso) for d in DIMENSIONES}

    args.salida.mkdir(parents=True, exist_ok=True)
    ruta_consenso = args.salida / "codificacion_S1_consenso.csv"
    ruta_discrepancias = args.salida / "discrepancias_S1.csv"
    ruta_json = args.salida / "acuerdo_S1.json"

    with open(ruta_consenso, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=["rf_id", *DIMENSIONES, "unanime"], lineterminator="\n")
        w.writeheader()
        w.writerows(consenso)
    with open(ruta_discrepancias, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=["rf_id", "dimension", *CODIFICADORES, "consenso"], lineterminator="\n")
        w.writeheader()
        w.writerows(discrepancias)
    with open(ruta_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Codificadores: {', '.join(CODIFICADORES)} · RF: {len(ids)} · "
          f"decisiones: {len(ids) * len(DIMENSIONES) * len(CODIFICADORES)}")
    print(f"{'dim':<4}{'marcas A/B/C':>14}{'unánime':>10}{'PABAK':>8}{'Fleiss k':>10}   kappa de Cohen por pares")
    for d in DIMENSIONES:
        r = resumen["dimensiones"][d]
        m = "/".join(str(r["marcas_por_codificador"][l]) for l in CODIFICADORES)
        pares = "  ".join(f"{p}: {'indef.' if v['kappa_cohen'] is None else format(v['kappa_cohen'], '.4f')}"
                          for p, v in r["pares"].items())
        kf = "indef." if r["kappa_fleiss"] is None else f"{r['kappa_fleiss']:.4f}"
        print(f"{d:<4}{m:>14}{r['acuerdo_unanime']:>10.4f}{r['pabak_unanime']:>8.4f}{kf:>10}   {pares}")
    print(f"RF con las cuatro dimensiones unánimes: {resumen['rf_unanimes']} de {len(ids)}; "
          f"discrepancias: {len(discrepancias)} de {len(ids) * len(DIMENSIONES)}")
    print(f"Marcas por consenso: {resumen['marcas_consenso']}")
    for ruta in (ruta_consenso, ruta_discrepancias, ruta_json):
        print(f"{hashlib.sha256(ruta.read_bytes()).hexdigest()}  {ruta.name}")


if __name__ == "__main__":
    main()
