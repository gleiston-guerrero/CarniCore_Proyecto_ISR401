"""
m1_02_reconstruir_clave.py
Corrección M1, Fase 1.2 -- CarniCore.

Reconstruye la clave ítem -> RF de las plantillas del panel de expertos.
La clave original de aleatorización no se conservó, así que la clave que
produce este script es RECONSTRUIDA y así debe declararse en el manuscrito.

Método (sin ninguna intervención manual):
  1. Para cada ítem de T_A se calcula la similitud textual con cada requisito
     de rf27.json (v2.0): difflib.SequenceMatcher(autojunk=False).ratio().
     autojunk=False es obligatorio: con el valor por defecto, difflib descarta
     los caracteres frecuentes en textos de más de 200 caracteres y la
     similitud deja de ser fiable.
  2. Se asigna a cada ítem el RF más similar.
  3. Las asignaciones con similitud < 0,60 o con margen < 0,10 sobre el
     segundo RF más similar se listan para revisión humana documentada.

Validaciones (el script se detiene con código 1 si alguna falla):
  - la clave es biyectiva: 27 ítems <-> 27 RF distintos;
  - las 81 marcas de las plantillas (27 ítems x 3 expertos), reordenadas con
    la clave, coinciden con etiquetas_expertos.csv.

Limitación que el script informa: la validación por marcas solo discrimina
entre RF con patrón de marcas distinto. Para los ítems que ningún experto
marcó (patrón 0,0,0), la única evidencia de la asignación es la similitud
textual.

Entradas:  07_Datos/m1/corpus_TA_items.json        (m1_01_extraer_TA.py)
           07_Datos/m1/marcas_TA_items.csv          (m1_01_extraer_TA.py)
           07_Datos/scripts/rf27.json               (T_B, SRS v2.0)
           07_Datos/datos_procesados/etiquetas_expertos.csv
Salidas:   <salida>/clave_items_rf.csv
               item,rf_id,similitud,segundo_rf,margen,revisar
           <salida>/corpus_TA_rf.json
               [{"id": "RF-01", "nombre": "", "descripcion": <texto evaluado>}, ...]
               Mismo formato que rf27.json, para que el detector lo lea sin
               cambios. "nombre" va vacío a propósito: los expertos no lo
               vieron y el detector no lo usa.

Uso (desde la raíz del repositorio):
    python 07_Datos/m1/m1_02_reconstruir_clave.py
    python 07_Datos/m1/m1_02_reconstruir_clave.py --salida <carpeta>
"""

import argparse
import csv
import difflib
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
M1 = RAIZ / "07_Datos" / "m1"
CORPUS_TA = M1 / "corpus_TA_items.json"
MARCAS_TA = M1 / "marcas_TA_items.csv"
RF27 = RAIZ / "07_Datos" / "scripts" / "rf27.json"
ETIQUETAS = RAIZ / "07_Datos" / "datos_procesados" / "etiquetas_expertos.csv"
EXPERTOS = ["experto_1", "experto_2", "experto_3"]

UMBRAL_SIMILITUD = 0.60
UMBRAL_MARGEN = 0.10


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def leer_json(ruta):
    if not ruta.exists():
        fallar(f"no existe {ruta.relative_to(RAIZ)}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def leer_csv(ruta):
    if not ruta.exists():
        fallar(f"no existe {ruta.relative_to(RAIZ)}")
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sha256(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=M1,
                        help="carpeta de salida (por defecto 07_Datos/m1)")
    args = parser.parse_args()

    items = leer_json(CORPUS_TA)
    rf27 = {r["id"]: r["descripcion"] for r in leer_json(RF27)}
    marcas = {f["item"]: tuple(int(f[e]) for e in EXPERTOS) for f in leer_csv(MARCAS_TA)}
    etiquetas = {f["rf_id"]: tuple(int(f[e]) for e in EXPERTOS) for f in leer_csv(ETIQUETAS)}

    if len(items) != 27 or len(rf27) != 27 or len(marcas) != 27 or len(etiquetas) != 27:
        fallar("se esperaban 27 elementos en cada entrada")

    clave = []
    for it in items:
        ranking = sorted(
            ((difflib.SequenceMatcher(None, it["descripcion"], texto, autojunk=False).ratio(), rf)
             for rf, texto in rf27.items()),
            reverse=True,
        )
        (sim1, rf1), (sim2, rf2) = ranking[0], ranking[1]
        clave.append({
            "item": it["item"], "rf_id": rf1, "similitud": round(sim1, 2),
            "segundo_rf": rf2, "margen": round(sim1 - sim2, 2),
            "revisar": int(sim1 < UMBRAL_SIMILITUD or sim1 - sim2 < UMBRAL_MARGEN),
        })

    repetidos = [rf for rf, n in Counter(c["rf_id"] for c in clave).items() if n > 1]
    if repetidos or {c["rf_id"] for c in clave} != set(rf27):
        fallar(f"la clave no es biyectiva; RF repetidos: {repetidos}")

    discrepancias = [(c["item"], c["rf_id"]) for c in clave
                     if marcas[c["item"]] != etiquetas[c["rf_id"]]]
    if discrepancias:
        fallar(f"las marcas de las plantillas no coinciden con etiquetas_expertos.csv en {discrepancias}")

    args.salida.mkdir(parents=True, exist_ok=True)
    ruta_clave = args.salida / "clave_items_rf.csv"
    ruta_corpus = args.salida / "corpus_TA_rf.json"

    with open(ruta_clave, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["item", "rf_id", "similitud", "segundo_rf", "margen", "revisar"])
        for c in sorted(clave, key=lambda c: c["item"]):
            w.writerow([c["item"], c["rf_id"], f"{c['similitud']:.2f}",
                        c["segundo_rf"], f"{c['margen']:.2f}", c["revisar"]])

    texto_por_item = {it["item"]: it["descripcion"] for it in items}
    corpus = [{"id": c["rf_id"], "nombre": "", "descripcion": texto_por_item[c["item"]]}
              for c in sorted(clave, key=lambda c: c["rf_id"])]
    with open(ruta_corpus, "w", encoding="utf-8", newline="\n") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
        f.write("\n")

    patrones = Counter(etiquetas.values())
    unicos = sum(1 for c in clave if patrones[etiquetas[c["rf_id"]]] == 1)
    print("Clave reconstruida automáticamente: 27 ítems <-> 27 RF distintos")
    print("Validación por marcas: 81 de 81 coinciden con etiquetas_expertos.csv")
    print(f"  Ítems con patrón de marcas único (validación discriminante): {unicos}")
    print(f"  Ítems con patrón compartido (solo evidencia textual): {27 - unicos}")
    revisar = [c for c in clave if c["revisar"]]
    print(f"Asignaciones para revisión humana (similitud < {UMBRAL_SIMILITUD:.2f} "
          f"o margen < {UMBRAL_MARGEN:.2f}):")
    for c in sorted(revisar, key=lambda c: c["item"]):
        print(f"  ítem {c['item']} -> {c['rf_id']}  similitud {c['similitud']:.2f}  "
              f"(segundo: {c['segundo_rf']}, margen {c['margen']:.2f})")
    if not revisar:
        print("  ninguna")
    for ruta in (ruta_clave, ruta_corpus):
        print(f"{sha256(ruta)}  {ruta.name}")


if __name__ == "__main__":
    main()
