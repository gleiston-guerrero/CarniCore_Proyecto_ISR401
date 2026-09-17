"""
rev_01_estadisticos_complementarios.py
Estadísticos complementarios para la revisión del manuscrito -- CarniCore.

Cubre dos carencias señaladas en la revisión:

M4 (fidelidad al pre-registro). El protocolo registró el contraste kappa entre
el detector y el consenso experto, con corrección de Bonferroni, y los IC del
95 % por bootstrap para las métricas. Ninguno de los dos se informaba. Aquí se
calculan.

M5 (informe estadístico). Añade lo que el análisis publicado no daba:
  - contraste directo de kappa = 0 para el panel, en lugar de deducirlo del
    kappa mínimo detectable, que no responde esa pregunta;
  - IC del 95 % por bootstrap para todos los kappa;
  - acuerdo bruto por par, que kappa no muestra;
  - índices robustos a la prevalencia (PABAK y AC1 de Gwet), porque kappa cae
    cuando el rasgo es raro (Feinstein y Cicchetti, 1990);
  - IC exactos de Clopper-Pearson para exhaustividad, especificidad, valor
    predictivo negativo y prevalencia;
  - las dos maneras de calcular el kappa mínimo detectable, para dejar clara
    cuál se usó.

La precisión no se informa como 0: con VP = 0 y FP = 0 es 0/0, indefinida.

El bootstrap replica el procedimiento registrado: 10.000 réplicas, semilla 42,
percentiles 2,5 y 97,5.

Entradas:  07_Datos/datos_procesados/etiquetas_expertos.csv
           07_Datos/m1/resultados_TA/clasificaciones_detector.csv
Salida:    <salida>/estadisticos_complementarios.json

Uso (desde la raíz del repositorio):
    python 07_Datos/revision/rev_01_estadisticos_complementarios.py
"""

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from itertools import combinations
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
REV = RAIZ / "07_Datos" / "revision"
ETIQUETAS = RAIZ / "07_Datos" / "datos_procesados" / "etiquetas_expertos.csv"
DETECTOR = RAIZ / "07_Datos" / "m1" / "resultados_TA" / "clasificaciones_detector.csv"
EXPERTOS = ["experto_1", "experto_2", "experto_3"]
N_REPLICAS = 10_000
SEMILLA = 42
Z_ALFA_2 = 1.959963984540054   # normal(0,1), cola bilateral al 5 %
Z_BETA = 0.8416212335729143    # potencia 0,80


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def leer_csv(ruta):
    if not ruta.exists():
        fallar(f"no existe {ruta.relative_to(RAIZ)}")
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def cohen(x, y):
    """kappa de Cohen, acuerdo bruto y acuerdo esperado por azar."""
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    px, py = sum(x) / n, sum(y) / n
    pe = px * py + (1 - px) * (1 - py)
    return (None if pe == 1 else (po - pe) / (1 - pe)), po, pe


def fleiss(columnas):
    """kappa de Fleiss, acuerdo medio observado y acuerdo esperado."""
    m, n = len(columnas), len(columnas[0])
    p = sum(sum(c) for c in columnas) / (n * m)
    pe = p * p + (1 - p) ** 2
    p_barra = sum((k * (k - 1) + (m - k) * (m - k - 1)) / (m * (m - 1))
                  for k in (sum(c[i] for c in columnas) for i in range(n))) / n
    return (None if pe == 1 else (p_barra - pe) / (1 - pe)), p_barra, pe, p


def gwet_ac1(columnas):
    m, n = len(columnas), len(columnas[0])
    p = sum(sum(c) for c in columnas) / (n * m)
    pe = 2 * p * (1 - p)
    p_barra = sum((k * (k - 1) + (m - k) * (m - k - 1)) / (m * (m - 1))
                  for k in (sum(c[i] for c in columnas) for i in range(n))) / n
    return (p_barra - pe) / (1 - pe), p_barra


def bootstrap_ic(indices, estadistico):
    """IC percentil del 95 % remuestreando requisitos, como el análisis registrado."""
    rng = random.Random(SEMILLA)
    n = len(indices)
    valores = []
    for _ in range(N_REPLICAS):
        muestra = [rng.randrange(n) for _ in range(n)]
        v = estadistico(muestra)
        if v is not None and v == v:
            valores.append(v)
    valores.sort()
    if not valores:
        return None, None, 0
    return (valores[int(0.025 * len(valores))],
            valores[min(int(0.975 * len(valores)), len(valores) - 1)],
            len(valores))


def clopper_pearson(exitos, n, alfa=0.05):
    """IC exacto para una proporción, por inversión de la binomial."""
    def cdf(k, p):
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))

    def biseccion(f):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            medio = (lo + hi) / 2
            if f(medio) < 0:
                lo = medio
            else:
                hi = medio
        return (lo + hi) / 2

    inferior = 0.0 if exitos == 0 else biseccion(lambda p: 1 - cdf(exitos - 1, p) - alfa / 2)
    superior = 1.0 if exitos == n else biseccion(lambda p: alfa / 2 - cdf(exitos, p))
    return inferior, superior


def r4(x):
    return None if x is None else round(x, 4)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=REV)
    args = parser.parse_args()

    filas = leer_csv(ETIQUETAS)
    detector_filas = {f["id_rf"]: int(f["ambiguo_detector"]) for f in leer_csv(DETECTOR)}
    if len(filas) != 27 or len(detector_filas) != 27:
        fallar("se esperaban 27 requisitos en cada entrada")
    ids = [f["rf_id"] for f in filas]
    panel = {e: [int(f[e]) for f in filas] for e in EXPERTOS}
    consenso = [1 if sum(panel[e][i] for e in EXPERTOS) >= 2 else 0 for i in range(len(ids))]
    detector = [detector_filas[rf] for rf in ids]
    n = len(ids)

    def sub(col, muestra):
        return [col[i] for i in muestra]

    salida = {
        "n_rf": n,
        "bootstrap": {"n_replicas": N_REPLICAS, "semilla": SEMILLA, "metodo": "percentil 2,5 y 97,5"},
        "prevalencias": {**{e: sum(panel[e]) for e in EXPERTOS},
                         "consenso": sum(consenso), "detector": sum(detector)},
    }

    # --- M4: contraste registrado entre detector y consenso -----------------
    k_det, po_det, pe_det = cohen(detector, consenso)
    lo, hi, _ = bootstrap_ic(range(n), lambda m: cohen(sub(detector, m), sub(consenso, m))[0])
    salida["detector_vs_consenso"] = {
        "kappa_cohen": r4(k_det), "ic95_bootstrap": [r4(lo), r4(hi)],
        "acuerdo_bruto": r4(po_det), "acuerdo_esperado_pe": r4(pe_det),
        "nota": ("El detector no marca ningún requisito, de modo que su columna es "
                 "constante: kappa vale exactamente 0 y la hipótesis registrada "
                 "H1 (kappa > 0) no puede sostenerse. No hace falta prueba: el "
                 "valor no es estimado, es forzado por una columna sin variación."),
    }

    # --- Panel: kappa por pares, Fleiss, IC y contraste kappa = 0 ------------
    pares = {}
    for a, b in combinations(EXPERTOS, 2):
        k, po, pe = cohen(panel[a], panel[b])
        lo, hi, _ = bootstrap_ic(range(n), lambda m, a=a, b=b: cohen(sub(panel[a], m), sub(panel[b], m))[0])
        pares[f"{a}_vs_{b}"] = {"kappa_cohen": r4(k), "ic95_bootstrap": [r4(lo), r4(hi)],
                                "acuerdo_bruto": r4(po), "acuerdo_esperado_pe": r4(pe)}
    columnas = [panel[e] for e in EXPERTOS]
    kf, p_barra, pe_f, p_medio = fleiss(columnas)
    lo, hi, _ = bootstrap_ic(range(n), lambda m: fleiss([sub(c, m) for c in columnas])[0])
    se0_fleiss = math.sqrt(2 / (n * len(EXPERTOS) * (len(EXPERTOS) - 1)))
    z = kf / se0_fleiss
    p_valor = math.erfc(abs(z) / math.sqrt(2))
    ac1, _ = gwet_ac1(columnas)
    salida["panel"] = {
        "cohen_pares": pares,
        "bonferroni_3_pares": {"alfa_nominal": 0.05, "alfa_corregido": round(0.05 / 3, 4)},
        "fleiss": {
            "kappa": r4(kf), "ic95_bootstrap": [r4(lo), r4(hi)],
            "acuerdo_medio_observado": r4(p_barra), "acuerdo_esperado_pe": r4(pe_f),
            "proporcion_media_de_marcas": r4(p_medio),
            "contraste_kappa_igual_0": {
                "metodo": "error estándar asintótico bajo H0 (Fleiss, 1971): sqrt(2/(N·m·(m-1)))",
                "se0": r4(se0_fleiss), "z": r4(z), "p_bilateral": r4(p_valor),
            },
        },
        "robustos_a_la_prevalencia": {"pabak": r4(2 * p_barra - 1), "gwet_ac1": r4(ac1)},
    }

    # --- M5: métricas diagnósticas con IC exactos ---------------------------
    vp = sum(1 for i in range(n) if detector[i] == 1 and consenso[i] == 1)
    fp = sum(1 for i in range(n) if detector[i] == 1 and consenso[i] == 0)
    fn = sum(1 for i in range(n) if detector[i] == 0 and consenso[i] == 1)
    vn = sum(1 for i in range(n) if detector[i] == 0 and consenso[i] == 0)
    def ic(exitos, total):
        lo, hi = clopper_pearson(exitos, total)
        return {"estimacion": r4(exitos / total), "ic95_exacto": [r4(lo), r4(hi)], "n": total}
    salida["diagnostico"] = {
        "matriz": {"vp": vp, "fp": fp, "fn": fn, "vn": vn},
        "precision": {"estimacion": None, "nota": "indefinida: VP + FP = 0"},
        "exhaustividad_recall": ic(vp, vp + fn),
        "especificidad": ic(vn, vn + fp),
        "valor_predictivo_negativo": ic(vn, vn + fn),
        "prevalencia_por_consenso": ic(vp + fn, n),
    }

    # --- M5: kappa mínimo detectable, las dos formas ------------------------
    p1 = sum(consenso) / n
    p2 = sum(panel["experto_1"]) / n
    pe_c = p1 * p2 + (1 - p1) * (1 - p2)
    se0_cohen = math.sqrt(pe_c + pe_c ** 2 - (p1 * p2 * (p1 + p2)
                                              + (1 - p1) * (1 - p2) * ((1 - p1) + (1 - p2)))) \
        / ((1 - pe_c) * math.sqrt(n))
    salida["kappa_minimo_detectable"] = {
        "publicado": {
            "formula": ("error estándar de kappa de Cohen bajo H0 para una tabla 2x2, "
                        "aplicado a las marginales del consenso y del experto_1"),
            "p1_consenso": r4(p1), "p2_experto_1": r4(p2), "pe": r4(pe_c),
            "se0": r4(se0_cohen), "kappa_minimo": r4(Z_ALFA_2 * se0_cohen * (1 + Z_BETA / Z_ALFA_2)),
            "objecion": ("El kappa informado es el de Fleiss, de tres evaluadores; este "
                         "error estándar es de dos, y el par elegido (consenso y experto 1) "
                         "no es independiente, porque el consenso se deriva de los tres."),
        },
        "coherente_con_fleiss": {
            "formula": "error estándar asintótico de Fleiss bajo H0: sqrt(2/(N·m·(m-1)))",
            "se0": r4(se0_fleiss),
            "kappa_minimo": r4((Z_ALFA_2 + Z_BETA) * se0_fleiss),
            "n_para_kappa_0_40": math.ceil(((Z_ALFA_2 + Z_BETA) * math.sqrt(2 / (len(EXPERTOS) * (len(EXPERTOS) - 1))) / 0.40) ** 2),
        },
    }

    args.salida.mkdir(parents=True, exist_ok=True)
    ruta = args.salida / "estadisticos_complementarios.json"
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
        f.write("\n")

    d = salida["detector_vs_consenso"]
    print(f"Detector vs consenso: kappa = {d['kappa_cohen']:.4f}  IC95 {d['ic95_bootstrap']}  "
          f"acuerdo bruto {d['acuerdo_bruto']:.4f}")
    print("Panel:")
    for par, v in pares.items():
        print(f"  {par:<24} kappa {v['kappa_cohen']:.4f}  IC95 [{v['ic95_bootstrap'][0]:.4f}, "
              f"{v['ic95_bootstrap'][1]:.4f}]  acuerdo bruto {v['acuerdo_bruto']:.4f}")
    fl = salida["panel"]["fleiss"]
    c = fl["contraste_kappa_igual_0"]
    print(f"  Fleiss                   kappa {fl['kappa']:.4f}  IC95 [{fl['ic95_bootstrap'][0]:.4f}, "
          f"{fl['ic95_bootstrap'][1]:.4f}]  z {c['z']:.4f}  p {c['p_bilateral']:.4f}")
    r = salida["panel"]["robustos_a_la_prevalencia"]
    print(f"  PABAK {r['pabak']:.4f}   AC1 de Gwet {r['gwet_ac1']:.4f}")
    dg = salida["diagnostico"]
    print("Diagnóstico (IC exactos de Clopper-Pearson):")
    print("  precisión: indefinida (VP + FP = 0)")
    for clave in ("exhaustividad_recall", "especificidad", "valor_predictivo_negativo",
                  "prevalencia_por_consenso"):
        v = dg[clave]
        print(f"  {clave:<26} {v['estimacion']:.4f}  IC95 [{v['ic95_exacto'][0]:.4f}, {v['ic95_exacto'][1]:.4f}]  n = {v['n']}")
    k = salida["kappa_minimo_detectable"]
    print(f"kappa mínimo detectable: publicado {k['publicado']['kappa_minimo']:.4f} "
          f"(SE0 {k['publicado']['se0']:.4f}, fórmula de dos evaluadores) · "
          f"coherente con Fleiss {k['coherente_con_fleiss']['kappa_minimo']:.4f} "
          f"(SE0 {k['coherente_con_fleiss']['se0']:.4f}); N para kappa = 0,40: "
          f"{k['coherente_con_fleiss']['n_para_kappa_0_40']}")
    print(f"{hashlib.sha256(ruta.read_bytes()).hexdigest()}  {ruta.name}")


if __name__ == "__main__":
    main()
