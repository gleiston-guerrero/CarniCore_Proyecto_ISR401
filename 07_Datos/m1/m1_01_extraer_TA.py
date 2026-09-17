"""
m1_01_extraer_TA.py
Corrección M1, Fase 1.1 -- CarniCore.

Reconstruye T_A: el texto EXACTO que evaluó el panel de expertos el
31-08-2026, tal como aparece en las plantillas anonimizadas. No se copia
nada a mano: el corpus se extrae por programa desde los datos brutos.

El script NO asigna identificadores RF. Las plantillas presentan los ítems en
orden aleatorio y la clave ítem -> RF se documenta en un paso aparte (Fase 1.2).

Validaciones (el script se detiene con código 1 si alguna falla):
  - cada plantilla contiene exactamente 27 ítems, numerados 01..27 sin huecos;
  - cada ítem tiene exactamente una casilla marcada ("No ambiguo" o "Ambiguo");
  - las tres plantillas presentan el mismo texto en el mismo orden.

Entradas:  07_Datos/datos_crudos/Plantilla_Experto_{1,2,3}_ANONIMIZADA.md
Salidas:   <salida>/corpus_TA_items.json
               [{"item": "01", "descripcion": "..."}, ...]
           <salida>/marcas_TA_items.csv
               item,experto_1,experto_2,experto_3   (0 no ambiguo, 1 ambiguo)

Uso (desde la raíz del repositorio):
    python 07_Datos/m1/m1_01_extraer_TA.py
    python 07_Datos/m1/m1_01_extraer_TA.py --salida <carpeta>
"""

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PLANTILLAS = [
    RAIZ / "07_Datos" / "datos_crudos" / f"Plantilla_Experto_{i}_ANONIMIZADA.md"
    for i in (1, 2, 3)
]
N_ITEMS = 27

RE_ITEM = re.compile(r"^## Ítem (\d{2})\s*$", re.MULTILINE)
RE_CASILLA = re.compile(r"^- \[( |x|X)\] (No ambiguo|Ambiguo)\s*$", re.MULTILINE)
RE_FECHA = re.compile(r"^- Fecha de evaluación:\s*(\S+)\s*$", re.MULTILINE)


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def leer_plantilla(ruta):
    if not ruta.exists():
        fallar(f"no existe {ruta.relative_to(RAIZ)}")
    texto = ruta.read_text(encoding="utf-8").replace("\r\n", "\n")

    cabeceras = list(RE_ITEM.finditer(texto))
    numeros = [m.group(1) for m in cabeceras]
    esperados = [f"{i:02d}" for i in range(1, N_ITEMS + 1)]
    if numeros != esperados:
        fallar(f"{ruta.name}: ítems encontrados {numeros}, se esperaban 01..{N_ITEMS}")

    items = []
    for k, cab in enumerate(cabeceras):
        fin = cabeceras[k + 1].start() if k + 1 < len(cabeceras) else len(texto)
        bloque = texto[cab.end():fin]

        lineas_cita = [l[1:].strip() for l in bloque.split("\n") if l.startswith(">")]
        if not lineas_cita:
            fallar(f"{ruta.name}, ítem {cab.group(1)}: no se encontró el texto citado")
        descripcion = " ".join(lineas_cita)

        marcadas = [m.group(2) for m in RE_CASILLA.finditer(bloque) if m.group(1) in "xX"]
        if len(marcadas) != 1:
            fallar(f"{ruta.name}, ítem {cab.group(1)}: {len(marcadas)} casillas marcadas, se esperaba 1")

        items.append({
            "item": cab.group(1),
            "descripcion": descripcion,
            "marca": 1 if marcadas[0] == "Ambiguo" else 0,
        })

    fecha = RE_FECHA.search(texto)
    return items, fecha.group(1) if fecha else None


def sha256(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=RAIZ / "07_Datos" / "m1",
                        help="carpeta de salida (por defecto 07_Datos/m1)")
    args = parser.parse_args()

    plantillas = [leer_plantilla(r) for r in PLANTILLAS]

    base = [(it["item"], it["descripcion"]) for it in plantillas[0][0]]
    for n, (items, _) in enumerate(plantillas[1:], start=2):
        otra = [(it["item"], it["descripcion"]) for it in items]
        if otra != base:
            distintos = [a[0] for a, b in zip(base, otra) if a != b]
            fallar(f"la plantilla {n} difiere de la plantilla 1 en los ítems {distintos}")

    args.salida.mkdir(parents=True, exist_ok=True)
    ruta_corpus = args.salida / "corpus_TA_items.json"
    ruta_marcas = args.salida / "marcas_TA_items.csv"

    corpus = [{"item": item, "descripcion": desc} for item, desc in base]
    with open(ruta_corpus, "w", encoding="utf-8", newline="\n") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
        f.write("\n")

    with open(ruta_marcas, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["item", "experto_1", "experto_2", "experto_3"])
        for k, (item, _) in enumerate(base):
            w.writerow([item] + [plantillas[e][0][k]["marca"] for e in range(3)])

    print(f"Plantillas leídas: {len(plantillas)}; ítems por plantilla: {N_ITEMS}")
    for n, (_, fecha) in enumerate(plantillas, start=1):
        print(f"  Experto {n}: fecha de evaluación {fecha}")
    print("Texto y orden idénticos en las tres plantillas: sí")
    for n in range(3):
        print(f"  Ítems marcados como ambiguos por el experto {n + 1}: "
              f"{sum(it['marca'] for it in plantillas[n][0])}")
    for ruta in (ruta_corpus, ruta_marcas):
        print(f"{sha256(ruta)}  {ruta.name}")


if __name__ == "__main__":
    main()
