"""
m1_03_cronologia_corpus.py
Corrección M1, Fase 1.3 -- CarniCore.

Reconstruye, a partir del historial de git, qué redacción de los requisitos
funcionales contenía cada versión relevante del corpus y del ERS, y la compara
con las dos redacciones en juego:

  T_A  texto evaluado por el panel de expertos (07_Datos/m1/corpus_TA_rf.json)
  T_B  texto del ERS v2.0 sobre el que corre hoy el detector
       (07_Datos/scripts/rf27.json)

Para cada versión informa cuántos requisitos coinciden literalmente con T_A y
cuántos con T_B. Las versiones del ERS se leen con el mismo extractor que genera
rf27.json (07_Datos/scripts/extraer_rf_desde_tex.py), así que la comparación es
homogénea.

Requisito: un clon con el historial completo (no superficial), porque se leen
commits antiguos con `git show`.

Entradas:  historial de git; 07_Datos/m1/corpus_TA_rf.json; 07_Datos/scripts/rf27.json
Salida:    <salida>/cronologia_corpus.csv
               fecha,commit,autor,archivo,n_rf,iguales_TA,iguales_TB,mensaje

Uso (desde la raíz del repositorio):
    python 07_Datos/m1/m1_03_cronologia_corpus.py
    python 07_Datos/m1/m1_03_cronologia_corpus.py --salida <carpeta>
"""

import argparse
import csv
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
CORPUS_TB = RAIZ / "07_Datos" / "scripts" / "rf27.json"
EXTRACTOR = RAIZ / "07_Datos" / "scripts" / "extraer_rf_desde_tex.py"

# (commit, ruta en ese commit). Las rutas son las que tenía cada archivo en su
# momento: el corpus estuvo en 06_Experimento/scripts_analisis/ hasta el 03-09
# y el ERS se llamó ERS_SRS_2A_v1.0.tex hasta el 01-09.
VERSIONES = [
    ("87f2fc2", "06_Experimento/scripts_analisis/rf25.json"),
    ("b921494", "01_ERS/ERS_SRS_2A_v1.0.tex"),
    ("a2fea20", "06_Experimento/scripts_analisis/rf27.json"),
    ("446a828", "01_ERS/ERS_SRS_2B_v2.0.tex"),
    ("77fad51", "01_ERS/ERS_SRS_2B_v2.0.tex"),
    ("899f9a7", "07_Datos/scripts/rf27.json"),
    ("456d109", "01_ERS/ERS_SRS_2B_v2.0.tex"),
    ("c9e90f0", "07_Datos/scripts/rf27.json"),
]


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def git(*args):
    r = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True)
    if r.returncode != 0:
        fallar(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout


def cargar_extractor():
    spec = importlib.util.spec_from_file_location("extraer_rf_desde_tex", EXTRACTOR)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def requisitos_de(commit, ruta, extractor):
    contenido = git("show", f"{commit}:{ruta}")
    if ruta.endswith(".json"):
        return {r["id"]: r["descripcion"] for r in json.loads(contenido.decode("utf-8"))}
    with tempfile.TemporaryDirectory() as tmp:
        tex = Path(tmp) / "ers.tex"
        tex.write_bytes(contenido)
        return {r["id"]: r["descripcion"] for r in extractor.extraer(str(tex))}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=M1,
                        help="carpeta de salida (por defecto 07_Datos/m1)")
    args = parser.parse_args()

    for ruta in (CORPUS_TA, CORPUS_TB, EXTRACTOR):
        if not ruta.exists():
            fallar(f"no existe {ruta.relative_to(RAIZ)}")
    t_a = {r["id"]: r["descripcion"] for r in json.loads(CORPUS_TA.read_text(encoding="utf-8"))}
    t_b = {r["id"]: r["descripcion"] for r in json.loads(CORPUS_TB.read_text(encoding="utf-8"))}
    extractor = cargar_extractor()

    filas = []
    for commit, ruta in VERSIONES:
        meta = git("log", "-1", "--format=%ad%x1f%h%x1f%an%x1f%s",
                   "--date=format:%Y-%m-%d %H:%M %z", commit).decode("utf-8").strip()
        fecha, corto, autor, mensaje = meta.split("\x1f")
        req = requisitos_de(commit, ruta, extractor)
        filas.append({
            "fecha": fecha, "commit": corto, "autor": autor, "archivo": ruta,
            "n_rf": len(req),
            "iguales_TA": sum(t_a.get(k) == v for k, v in req.items()),
            "iguales_TB": sum(t_b.get(k) == v for k, v in req.items()),
            "mensaje": mensaje,
        })
    filas.sort(key=lambda f: f["fecha"])

    args.salida.mkdir(parents=True, exist_ok=True)
    ruta_csv = args.salida / "cronologia_corpus.csv"
    campos = ["fecha", "commit", "autor", "archivo", "n_rf", "iguales_TA", "iguales_TB", "mensaje"]
    with open(ruta_csv, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=campos, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)

    print(f"{'fecha':<23}{'commit':<9}{'n_rf':>5}{'=T_A':>6}{'=T_B':>6}  archivo")
    for f in filas:
        print(f"{f['fecha']:<23}{f['commit']:<9}{f['n_rf']:>5}{f['iguales_TA']:>6}"
              f"{f['iguales_TB']:>6}  {f['archivo']}")
    print(f"{hashlib.sha256(ruta_csv.read_bytes()).hexdigest()}  {ruta_csv.name}")


if __name__ == "__main__":
    main()
