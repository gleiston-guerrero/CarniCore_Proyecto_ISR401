"""
m1_04_tabla_S1.py
Corrección M1, Fase 2 -- CarniCore.

Genera la Tabla S1 del material suplementario: requisito por requisito, en qué
difiere el texto evaluado por el panel (T_A) del texto del ERS v2.0 (T_B), y en
qué commit del ERS aparece por primera vez la redacción T_B.

Este script solo produce la parte OBJETIVA de la comparación (qué palabras se
eliminan y cuáles se añaden). La clasificación del TIPO de cambio es un juicio
humano: el script genera además una hoja de codificación en blanco para que dos
autores la completen por separado, según 07_Datos/m1/codificacion_S1/libro_codigos_S1.md.

Diferencia por palabras: difflib.SequenceMatcher(autojunk=False) sobre los
textos divididos en espacios. Los tramos eliminados o añadidos no contiguos se
separan con " | ".

Requisito: un clon con el historial completo, porque se recorren todas las
versiones de 01_ERS/ERS_SRS_2B_v2.0.tex (y de su nombre anterior,
ERS_SRS_2A_v1.0.tex) con el extractor 07_Datos/scripts/extraer_rf_desde_tex.py.

Entradas:  07_Datos/m1/corpus_TA_rf.json; 07_Datos/scripts/rf27.json; historial de git
Salidas:   <salida>/tabla_S1_diferencias_TA_TB.csv
               rf_id,item,identico,similitud,palabras_eliminadas,
               palabras_anadidas,commit_aparicion_TB,fecha_aparicion_TB,
               texto_TA,texto_TB
           <salida>/codificacion_S1_plantilla.csv   (solo los RF que cambian)
               rf_id,palabras_eliminadas,palabras_anadidas,L,R,G,C,comentario
               (L, R, G y C se dejan vacíos: cada codificador escribe 0 o 1)

Uso (desde la raíz del repositorio):
    python 07_Datos/m1/m1_04_tabla_S1.py
    python 07_Datos/m1/m1_04_tabla_S1.py --salida <carpeta>
"""

import argparse
import csv
import difflib
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

RAIZ = Path(__file__).resolve().parents[2]
M1 = RAIZ / "07_Datos" / "m1"
CORPUS_TA = M1 / "corpus_TA_rf.json"
CLAVE = M1 / "clave_items_rf.csv"
CORPUS_TB = RAIZ / "07_Datos" / "scripts" / "rf27.json"
EXTRACTOR = RAIZ / "07_Datos" / "scripts" / "extraer_rf_desde_tex.py"
ERS = "01_ERS/ERS_SRS_2B_v2.0.tex"


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def git(*args):
    r = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True)
    if r.returncode != 0:
        fallar(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8")


def cargar_extractor():
    spec = importlib.util.spec_from_file_location("extraer_rf_desde_tex", EXTRACTOR)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def historial_ers():
    """Lista (commit, fecha, ruta) de todas las versiones del ERS, de la más antigua a la más reciente."""
    # --follow no admite --reverse de forma fiable: se ordena después.
    salida = git("log", "--follow", "--name-only",
                 "--format=@%h%x1f%ad", "--date=format:%Y-%m-%d %H:%M %z", "--", ERS)
    versiones, actual = [], None
    for linea in salida.splitlines():
        if linea.startswith("@"):
            actual = linea[1:].split("\x1f")
        elif linea.strip() and actual:
            versiones.append((actual[0], actual[1], linea.strip()))
            actual = None
    if not versiones:
        fallar(f"no se encontró historial de {ERS}; ¿clon superficial?")
    return versiones[::-1]


def requisitos_tex(commit, ruta, extractor):
    with tempfile.TemporaryDirectory() as tmp:
        tex = Path(tmp) / "ers.tex"
        tex.write_bytes(subprocess.run(["git", "-C", str(RAIZ), "show", f"{commit}:{ruta}"],
                                       capture_output=True, check=True).stdout)
        try:
            return {r["id"]: r["descripcion"] for r in extractor.extraer(str(tex))}
        except Exception:
            return {}


def diferencia_palabras(a, b):
    pa, pb = a.split(), b.split()
    eliminadas, anadidas = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pa, pb, autojunk=False).get_opcodes():
        if op in ("delete", "replace"):
            eliminadas.append(" ".join(pa[i1:i2]))
        if op in ("insert", "replace"):
            anadidas.append(" ".join(pb[j1:j2]))
    return " | ".join(eliminadas), " | ".join(anadidas)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=M1,
                        help="carpeta de salida (por defecto 07_Datos/m1)")
    args = parser.parse_args()

    for ruta in (CORPUS_TA, CLAVE, CORPUS_TB, EXTRACTOR):
        if not ruta.exists():
            fallar(f"no existe {ruta.relative_to(RAIZ)}")
    t_a = {r["id"]: r["descripcion"] for r in json.loads(CORPUS_TA.read_text(encoding="utf-8"))}
    t_b = {r["id"]: r["descripcion"] for r in json.loads(CORPUS_TB.read_text(encoding="utf-8"))}
    with open(CLAVE, encoding="utf-8", newline="") as f:
        item_de = {fila["rf_id"]: fila["item"] for fila in csv.DictReader(f)}
    if set(t_a) != set(t_b) or set(t_a) != set(item_de) or len(t_a) != 27:
        fallar("T_A, T_B y la clave no contienen los mismos 27 RF")

    extractor = cargar_extractor()
    aparicion = {}
    for commit, fecha, ruta in historial_ers():
        req = requisitos_tex(commit, ruta, extractor)
        for rf, texto in req.items():
            if rf in t_b and rf not in aparicion and texto == t_b[rf]:
                aparicion[rf] = (commit, fecha)

    filas = []
    for rf in sorted(t_a):
        identico = int(t_a[rf] == t_b[rf])
        eliminadas, anadidas = ("", "") if identico else diferencia_palabras(t_a[rf], t_b[rf])
        commit, fecha = aparicion.get(rf, ("", ""))
        filas.append({
            "rf_id": rf, "item": item_de[rf], "identico": identico,
            "similitud": f"{difflib.SequenceMatcher(None, t_a[rf], t_b[rf], autojunk=False).ratio():.2f}",
            "palabras_eliminadas": eliminadas, "palabras_anadidas": anadidas,
            "commit_aparicion_TB": commit, "fecha_aparicion_TB": fecha,
            "texto_TA": t_a[rf], "texto_TB": t_b[rf],
        })

    args.salida.mkdir(parents=True, exist_ok=True)
    ruta_tabla = args.salida / "tabla_S1_diferencias_TA_TB.csv"
    ruta_plantilla = args.salida / "codificacion_S1_plantilla.csv"

    with open(ruta_tabla, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)

    with open(ruta_plantilla, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["rf_id", "palabras_eliminadas", "palabras_anadidas", "L", "R", "G", "C", "comentario"])
        for fila in filas:
            if not fila["identico"]:
                w.writerow([fila["rf_id"], fila["palabras_eliminadas"], fila["palabras_anadidas"],
                            "", "", "", "", ""])

    cambian = [f for f in filas if not f["identico"]]
    print(f"Requisitos comparados: {len(filas)}; idénticos: {len(filas) - len(cambian)}; "
          f"con cambios: {len(cambian)}")
    print(f"  Idénticos: {', '.join(f['rf_id'] for f in filas if f['identico'])}")
    sin_eliminar = [f["rf_id"] for f in cambian if not f["palabras_eliminadas"]]
    print(f"  Cambios que solo añaden texto: {len(sin_eliminar)}; "
          f"que eliminan o sustituyen texto: {len(cambian) - len(sin_eliminar)}")
    commits = sorted({(f["fecha_aparicion_TB"], f["commit_aparicion_TB"]) for f in cambian})
    print("Commit del ERS en que aparece por primera vez la redacción T_B de los RF que cambian:")
    for fecha, commit in commits:
        n = sum(1 for f in cambian if f["commit_aparicion_TB"] == commit)
        print(f"  {commit or '(no encontrado)'}  {fecha}  {n} RF")
    for ruta in (ruta_tabla, ruta_plantilla):
        print(f"{hashlib.sha256(ruta.read_bytes()).hexdigest()}  {ruta.name}")


if __name__ == "__main__":
    main()
