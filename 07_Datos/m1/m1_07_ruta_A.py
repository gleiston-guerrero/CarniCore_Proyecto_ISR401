"""
m1_07_ruta_A.py
Corrección M1, Fase 3 -- CarniCore.

Ejecuta el análisis registrado sobre T_A, el texto que el panel de expertos
evaluó realmente el 31-08-2026, en lugar de sobre T_B (ERS v2.0), que es el
corpus que el detector viene usando desde el 14-09-2026 y que el panel nunca
vio.

Principio: NO se modifica ni una línea del pipeline publicado. El script crea
un espacio de trabajo temporal con la misma estructura de carpetas, copia allí
los scripts tal cual, sustituye únicamente el corpus (rf27.json <- T_A) y
ejecuta los mismos pasos, en el mismo orden:

    detector_ambiguedad.py -> 01_importar_datos.py -> 02_calcular_kappa.py
    -> 03_matriz_confusion_prf1.py -> 04_bootstrap_ic95.py
    -> 06_analisis_potencia.py

Las etiquetas del panel no se tocan: son las mismas que en el análisis
original. Lo único que cambia es a qué texto corresponden, que es justamente
el problema que M1 corrige.

El paso 05 (figuras) se omite a propósito: genera PDF cuya huella depende de
las fuentes del equipo y no aporta ninguna cifra.

Entradas:  07_Datos/m1/corpus_TA_rf.json
           07_Datos/scripts/ (pipeline sin modificar)
           07_Datos/datos_procesados/etiquetas_expertos.csv
Salidas:   07_Datos/m1/resultados_TA/  (mismos nombres que 07_Datos/resultados/)
           07_Datos/m1/comparacion_TA_TB.json

Uso (desde la raíz del repositorio):
    python 07_Datos/m1/m1_07_ruta_A.py
    python 07_Datos/m1/m1_07_ruta_A.py --salida <carpeta>
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
M1 = RAIZ / "07_Datos" / "m1"
CORPUS_TA = M1 / "corpus_TA_rf.json"
SCRIPTS = RAIZ / "07_Datos" / "scripts"
ETIQUETAS = RAIZ / "07_Datos" / "datos_procesados" / "etiquetas_expertos.csv"
RESULTADOS_TB = RAIZ / "07_Datos" / "resultados"

PASOS = [
    "detector_ambiguedad.py",
    "01_importar_datos.py",
    "02_calcular_kappa.py",
    "03_matriz_confusion_prf1.py",
    "04_bootstrap_ic95.py",
    "06_analisis_potencia.py",
]
ARTEFACTOS = [
    "dataset_consolidado.csv",
    "kappa_resultados.json",
    "matriz_confusion_prf1.json",
    "tabla_confusion.csv",
    "bootstrap_ic95.json",
    "analisis_potencia.json",
]


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def preparar(tmp):
    """Réplica de la estructura del repositorio, con T_A como corpus."""
    scripts = tmp / "07_Datos" / "scripts"
    scripts.mkdir(parents=True)
    for origen in SCRIPTS.glob("*.py"):
        shutil.copy2(origen, scripts / origen.name)
    shutil.copy2(CORPUS_TA, scripts / "rf27.json")
    procesados = tmp / "07_Datos" / "datos_procesados"
    procesados.mkdir(parents=True)
    shutil.copy2(ETIQUETAS, procesados / "etiquetas_expertos.csv")
    (tmp / "07_Datos" / "resultados").mkdir(parents=True)
    for sub in ("figuras", "tablas"):
        (tmp / "08_Publicacion" / sub).mkdir(parents=True)
    return scripts


def ejecutar(scripts, paso):
    r = subprocess.run([sys.executable, str(scripts / paso)], cwd=str(scripts),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        fallar(f"{paso} terminó con código {r.returncode}:\n{(r.stderr or r.stdout).strip()}")
    return r.stdout


def cargar(ruta):
    return json.loads(ruta.read_text(encoding="utf-8-sig"))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=M1 / "resultados_TA",
                        help="carpeta de salida (por defecto 07_Datos/m1/resultados_TA)")
    args = parser.parse_args()

    for ruta in (CORPUS_TA, ETIQUETAS, SCRIPTS):
        if not ruta.exists():
            fallar(f"no existe {ruta.relative_to(RAIZ)}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        scripts = preparar(tmp)
        for paso in PASOS:
            if not (scripts / paso).exists():
                fallar(f"el pipeline no contiene {paso}")
            ejecutar(scripts, paso)
            print(f"  ejecutado {paso}")

        args.salida.mkdir(parents=True, exist_ok=True)
        shutil.copy2(scripts / "clasificaciones_detector.csv",
                     args.salida / "clasificaciones_detector.csv")
        for nombre in ARTEFACTOS:
            origen = tmp / "07_Datos" / "resultados" / nombre
            if not origen.exists():
                fallar(f"el pipeline no produjo {nombre}")
            shutil.copy2(origen, args.salida / nombre)

    conf_ta = cargar(args.salida / "matriz_confusion_prf1.json")
    conf_tb = cargar(RESULTADOS_TB / "matriz_confusion_prf1.json")
    kappa_ta = cargar(args.salida / "kappa_resultados.json")
    kappa_tb = cargar(RESULTADOS_TB / "kappa_resultados.json")
    det_ta = (args.salida / "clasificaciones_detector.csv").read_text(encoding="utf-8")
    marcados_ta = sum(1 for linea in det_ta.splitlines()[1:] if linea.split(",")[1] == "1")

    comparacion = {
        "corpus_T_A": {
            "descripcion": "texto evaluado por el panel el 31-08-2026",
            "archivo": "07_Datos/m1/corpus_TA_rf.json",
            "sha256": hashlib.sha256(CORPUS_TA.read_bytes()).hexdigest(),
            "rf_marcados_por_el_detector": marcados_ta,
            "matriz_confusion": conf_ta["matriz_confusion"],
            "precision": conf_ta["precision"], "recall": conf_ta["recall"], "f1": conf_ta["f1"],
            "kappa_fleiss_panel": kappa_ta["fleiss_consenso"],
        },
        "corpus_T_B": {
            "descripcion": "ERS v2.0, corpus del análisis publicado",
            "archivo": "07_Datos/scripts/rf27.json",
            "sha256": hashlib.sha256((SCRIPTS / "rf27.json").read_bytes()).hexdigest(),
            "matriz_confusion": conf_tb["matriz_confusion"],
            "precision": conf_tb["precision"], "recall": conf_tb["recall"], "f1": conf_tb["f1"],
            "kappa_fleiss_panel": kappa_tb["fleiss_consenso"],
        },
        "etiquetas_del_panel": {
            "archivo": "07_Datos/datos_procesados/etiquetas_expertos.csv",
            "sha256": hashlib.sha256(ETIQUETAS.read_bytes()).hexdigest(),
            "nota": "las mismas en ambos análisis; solo cambia el texto al que corresponden",
        },
        "pipeline": "07_Datos/scripts, sin modificar; paso 05 (figuras) omitido",
    }
    ruta_comparacion = M1 / "comparacion_TA_TB.json"
    with open(ruta_comparacion, "w", encoding="utf-8", newline="\n") as f:
        json.dump(comparacion, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nRF marcados por el detector sobre T_A: {marcados_ta} de 27")
    print(f"{'':<26}{'T_A (evaluado)':>16}{'T_B (publicado)':>18}")
    m_ta, m_tb = conf_ta["matriz_confusion"], conf_tb["matriz_confusion"]
    for etiqueta, clave in (("Verdaderos positivos", "verdaderos_positivos"),
                            ("Falsos positivos", "falsos_positivos"),
                            ("Falsos negativos", "falsos_negativos"),
                            ("Verdaderos negativos", "verdaderos_negativos")):
        print(f"{etiqueta:<26}{m_ta[clave]:>16}{m_tb[clave]:>18}")
    for etiqueta, clave in (("Precisión", "precision"), ("Recall", "recall"), ("F1", "f1")):
        print(f"{etiqueta:<26}{conf_ta[clave]:>16.4f}{conf_tb[clave]:>18.4f}")
    print(f"{'Kappa de Fleiss (panel)':<26}{kappa_ta['fleiss_consenso']:>16.4f}"
          f"{kappa_tb['fleiss_consenso']:>18.4f}")
    print()
    for nombre in ["clasificaciones_detector.csv"] + ARTEFACTOS:
        ruta = args.salida / nombre
        print(f"{hashlib.sha256(ruta.read_bytes()).hexdigest()}  {nombre}")
    print(f"{hashlib.sha256(ruta_comparacion.read_bytes()).hexdigest()}  {ruta_comparacion.name}")


if __name__ == "__main__":
    main()
