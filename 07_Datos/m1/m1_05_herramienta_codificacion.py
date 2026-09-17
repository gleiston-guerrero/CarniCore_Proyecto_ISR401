"""
m1_05_herramienta_codificacion.py
Corrección M1, Fase 2 -- CarniCore.

Genera una herramienta de codificación autocontenida (un único archivo HTML que
se abre con doble clic, sin instalar nada y sin conexión a internet) para que
las personas codificadoras apliquen el libro de códigos de la Tabla S1.

La herramienta:
  - muestra cada uno de los 21 RF que cambian, con T_A y T_B lado a lado y las
    palabras eliminadas y añadidas resaltadas;
  - ofrece las cuatro dimensiones (L, R, G, C) como casillas, con la definición
    completa del libro de códigos a la vista;
  - guarda el avance en el propio navegador y, al terminar, descarga
    hoja_codificador_A.csv o hoja_codificador_B.csv con EXACTAMENTE el formato de
    codificacion_S1_plantilla.csv, y muestra su SHA-256.

Para evitar discrepancias, nada se copia a mano: los textos salen de
tabla_S1_diferencias_TA_TB.csv, las filas de la hoja salen de
codificacion_S1_plantilla.csv y las definiciones y reglas salen literalmente de
codificacion_S1/libro_codigos_S1.md. Si el libro cambia, hay que regenerar.

Entradas:  07_Datos/m1/tabla_S1_diferencias_TA_TB.csv
           07_Datos/m1/codificacion_S1_plantilla.csv
           07_Datos/m1/codificacion_S1/libro_codigos_S1.md
Salida:    <salida>/herramienta_codificacion_S1.html

Uso (desde la raíz del repositorio):
    python 07_Datos/m1/m1_05_herramienta_codificacion.py
    python 07_Datos/m1/m1_05_herramienta_codificacion.py --salida <carpeta>
"""

import argparse
import csv
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
M1 = RAIZ / "07_Datos" / "m1"
TABLA = M1 / "tabla_S1_diferencias_TA_TB.csv"
PLANTILLA = M1 / "codificacion_S1_plantilla.csv"
LIBRO = M1 / "codificacion_S1" / "libro_codigos_S1.md"
DIMENSIONES = ["L", "R", "G", "C"]
CAMPOS_DEFINICION = ["Definición", "Incluye", "Excluye", "Ejemplo ancla (ficticio)"]
PREGUNTAS = {
    "L": "¿T_B elimina o sustituye una expresión vaga de T_A?",
    "R": "¿T_B añade un umbral, condición, regla o comportamiento?",
    "G": "¿Cambia quién ejecuta la acción, o aparece una pasiva sin agente?",
    "C": "¿Solo cambian la redacción o las referencias cruzadas?",
}


def fallar(mensaje):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


def leer_csv(ruta):
    if not ruta.exists():
        fallar(f"no existe {ruta.relative_to(RAIZ)}")
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def unir_parrafo(texto):
    """Une las líneas de un párrafo y quita el formato Markdown (`código`, **negrita**, *cursiva*)."""
    texto = re.sub(r"`([^`]*)`", r"\1", texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto, flags=re.DOTALL)
    texto = re.sub(r"\*(.+?)\*", r"\1", texto, flags=re.DOTALL)
    return re.sub(r"\s+", " ", texto).strip()


def leer_libro():
    if not LIBRO.exists():
        fallar(f"no existe {LIBRO.relative_to(RAIZ)}")
    md = LIBRO.read_text(encoding="utf-8").replace("\r\n", "\n")

    definiciones = {}
    bloques = re.split(r"^### ", md, flags=re.MULTILINE)
    for bloque in bloques[1:]:
        cabecera, _, cuerpo = bloque.partition("\n")
        m = re.match(r"([LRGC]) — (.+)", cabecera.strip())
        if not m:
            continue
        cuerpo = cuerpo.split("\n## ")[0]
        campos = {}
        for parrafo in re.split(r"\n\s*\n", cuerpo):
            p = re.match(r"\*\*(.+?):\*\*\s*(.*)", parrafo.strip(), flags=re.DOTALL)
            if p and p.group(1) in CAMPOS_DEFINICION:
                campos[p.group(1)] = unir_parrafo(p.group(2))
        faltan = [c for c in CAMPOS_DEFINICION if c not in campos]
        if faltan:
            fallar(f"libro de códigos: a la dimensión {m.group(1)} le faltan {faltan}")
        definiciones[m.group(1)] = {"nombre": m.group(2).strip(), **campos}
    if sorted(definiciones) != sorted(DIMENSIONES):
        fallar(f"libro de códigos: dimensiones encontradas {sorted(definiciones)}")

    seccion = re.search(r"^## 4\. Reglas de aplicación\n(.*?)(?=^## )", md, flags=re.MULTILINE | re.DOTALL)
    if not seccion:
        fallar("libro de códigos: no se encontró la sección 4")
    reglas = [unir_parrafo(r) for r in re.split(r"^\d+\.\s", seccion.group(1), flags=re.MULTILINE)[1:]]
    if not reglas:
        fallar("libro de códigos: la sección 4 no tiene reglas numeradas")
    return definiciones, reglas


def segmentos(a, b):
    pa, pb = a.split(), b.split()
    salida = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pa, pb, autojunk=False).get_opcodes():
        salida.append([op, " ".join(pa[i1:i2]), " ".join(pb[j1:j2])])
    return salida


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--salida", type=Path, default=M1 / "codificacion_S1",
                        help="carpeta de salida (por defecto 07_Datos/m1/codificacion_S1)")
    args = parser.parse_args()

    tabla = {f["rf_id"]: f for f in leer_csv(TABLA)}
    plantilla = leer_csv(PLANTILLA)
    definiciones, reglas = leer_libro()

    requisitos = []
    for fila in plantilla:
        t = tabla.get(fila["rf_id"])
        if t is None or t["identico"] != "0":
            fallar(f"{fila['rf_id']} está en la plantilla pero no como RF con cambios en la Tabla S1")
        requisitos.append({
            "rf_id": fila["rf_id"],
            "palabras_eliminadas": fila["palabras_eliminadas"],
            "palabras_anadidas": fila["palabras_anadidas"],
            "segmentos": segmentos(t["texto_TA"], t["texto_TB"]),
        })

    huella = hashlib.sha256(PLANTILLA.read_bytes()).hexdigest()
    datos = {
        "huella_plantilla": huella,
        "cabecera": ["rf_id", "palabras_eliminadas", "palabras_anadidas", *DIMENSIONES, "comentario"],
        "dimensiones": [{"codigo": d, "pregunta": PREGUNTAS[d], **definiciones[d]} for d in DIMENSIONES],
        "reglas": reglas,
        "requisitos": requisitos,
    }
    json_datos = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA_HTML.replace("__DATOS__", json_datos)

    args.salida.mkdir(parents=True, exist_ok=True)
    ruta = args.salida / "herramienta_codificacion_S1.html"
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    print(f"Herramienta generada con {len(requisitos)} RF y las dimensiones {', '.join(DIMENSIONES)}")
    print(f"  Definiciones y {len(reglas)} reglas tomadas de {LIBRO.relative_to(RAIZ).as_posix()}")
    print(f"  Plantilla de referencia: SHA-256 {huella[:8]}…")
    print(f"{hashlib.sha256(ruta.read_bytes()).hexdigest()}  {ruta.name}")


PLANTILLA_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Codificación Tabla S1</title>
<style>
:root {
  --fondo: #f6f7f9; --panel: #ffffff; --texto: #1d2430; --suave: #5b6576;
  --borde: #d9dee6; --acento: #1f5fbf; --acento-suave: #e6eefb;
  --del-fondo: #fde2e1; --del-texto: #9b1c1c; --ins-fondo: #dcf5e3; --ins-texto: #13653a;
  --ok: #13653a; --pendiente: #b45309;
}
@media (prefers-color-scheme: dark) {
  :root {
    --fondo: #12151b; --panel: #1b2029; --texto: #e6e9ef; --suave: #9aa4b5;
    --borde: #2f3643; --acento: #7aa7ff; --acento-suave: #1f2a3d;
    --del-fondo: #4a1f22; --del-texto: #ffb4ae; --ins-fondo: #173b28; --ins-texto: #9be3b4;
    --ok: #6fd39a; --pendiente: #f0b35a;
  }
}
* { box-sizing: border-box; }
body { margin: 0; font: 16px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; background: var(--fondo); color: var(--texto); }
header { position: sticky; top: 0; z-index: 2; background: var(--panel); border-bottom: 1px solid var(--borde); padding: 10px 16px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
header h1 { font-size: 17px; margin: 0; }
.progreso { flex: 1; min-width: 160px; height: 8px; background: var(--borde); border-radius: 4px; overflow: hidden; }
.progreso > div { height: 100%; background: var(--acento); width: 0; transition: width .2s; }
.contador { color: var(--suave); font-variant-numeric: tabular-nums; }
main { max-width: 1180px; margin: 0 auto; padding: 16px; }
.panel { background: var(--panel); border: 1px solid var(--borde); border-radius: 10px; padding: 18px; margin-bottom: 16px; }
h2 { margin: 0 0 8px; font-size: 20px; }
h3 { margin: 0 0 6px; font-size: 15px; color: var(--suave); text-transform: uppercase; letter-spacing: .04em; }
button { font: inherit; border-radius: 8px; border: 1px solid var(--borde); background: var(--panel); color: var(--texto); padding: 8px 14px; cursor: pointer; }
button.primario { background: var(--acento); border-color: var(--acento); color: #fff; }
button:disabled { opacity: .45; cursor: default; }
.rol { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; }
.rol button { padding: 14px 22px; font-size: 17px; }
.diseno { display: grid; grid-template-columns: 210px 1fr; gap: 16px; }
@media (max-width: 820px) { .diseno { grid-template-columns: 1fr; } }
.lista button { display: flex; width: 100%; justify-content: space-between; margin-bottom: 6px; text-align: left; }
.lista button.actual { border-color: var(--acento); background: var(--acento-suave); }
.punto { width: 10px; height: 10px; border-radius: 50%; background: var(--borde); align-self: center; margin-left: 8px; }
.punto.hecho { background: var(--ok); }
@media (max-width: 820px) { .lista { display: flex; flex-wrap: wrap; gap: 6px; } .lista button { width: auto; margin-bottom: 0; } }
.textos { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 820px) { .textos { grid-template-columns: 1fr; } }
.texto { border: 1px solid var(--borde); border-radius: 8px; padding: 12px; }
del { background: var(--del-fondo); color: var(--del-texto); text-decoration: line-through; border-radius: 3px; padding: 0 2px; }
ins { background: var(--ins-fondo); color: var(--ins-texto); text-decoration: none; border-radius: 3px; padding: 0 2px; }
.leyenda { color: var(--suave); font-size: 14px; margin-top: 8px; }
.dims { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px; }
@media (max-width: 820px) { .dims { grid-template-columns: 1fr; } }
.dim { border: 2px solid var(--borde); border-radius: 10px; padding: 12px; }
.dim.marcada { border-color: var(--acento); background: var(--acento-suave); }
.dim label { display: flex; gap: 10px; cursor: pointer; align-items: flex-start; }
.dim input { width: 22px; height: 22px; margin-top: 2px; flex: none; }
.dim .nombre { font-weight: 600; }
.dim .pregunta { color: var(--suave); font-size: 14px; }
.dim details { margin-top: 8px; font-size: 14px; }
.dim details p { margin: 6px 0; }
kbd { border: 1px solid var(--borde); border-bottom-width: 2px; border-radius: 4px; padding: 0 5px; font-size: 13px; }
textarea { width: 100%; font: inherit; min-height: 64px; border: 1px solid var(--borde); border-radius: 8px; padding: 8px; background: var(--panel); color: var(--texto); }
.nav { display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; margin-top: 14px; }
.aviso { color: var(--pendiente); font-weight: 600; min-height: 1.5em; }
.hash { font-family: ui-monospace, Consolas, monospace; word-break: break-all; background: var(--fondo); padding: 8px; border-radius: 6px; }
ol li { margin-bottom: 6px; }
.oculto { display: none; }
</style>
</head>
<body>
<header>
  <h1>Codificación de cambios · Tabla S1</h1>
  <div class="progreso" aria-hidden="true"><div id="barra"></div></div>
  <span class="contador" id="contador"></span>
</header>
<main>

<section id="inicio" class="panel">
  <h2>Antes de empezar</h2>
  <p>Va a revisar <strong id="n-rf"></strong> requisitos de software. Cada uno aparece en dos versiones: <strong>T_A</strong> (anterior) y <strong>T_B</strong> (posterior). Para cada requisito, marque <strong>todas</strong> las dimensiones de cambio que estén presentes; al menos una.</p>
  <h3>Reglas de aplicación</h3>
  <ol id="reglas"></ol>
  <p>Su avance se guarda automáticamente en este navegador. Puede cerrar y volver a abrir el archivo con el mismo navegador. Al terminar, la herramienta descargará su hoja para enviarla.</p>
  <h3>¿Qué letra de codificador le asignaron?</h3>
  <div class="rol">
    <button class="primario" data-rol="A">Soy el codificador A</button>
    <button class="primario" data-rol="B">Soy el codificador B</button>
  </div>
</section>

<section id="trabajo" class="oculto">
  <div class="diseno">
    <nav class="panel lista" id="lista" aria-label="Requisitos"></nav>
    <div>
      <div class="panel">
        <h2 id="titulo"></h2>
        <div class="textos">
          <div class="texto"><h3>T_A · versión anterior</h3><div id="texto-a"></div></div>
          <div class="texto"><h3>T_B · versión posterior</h3><div id="texto-b"></div></div>
        </div>
        <p class="leyenda"><del>tachado</del> = eliminado en T_B · <ins>resaltado</ins> = añadido en T_B. Es una ayuda: lea ambos textos completos.</p>
      </div>
      <div class="panel">
        <h3>Dimensiones presentes (marque todas las que apliquen)</h3>
        <div class="dims" id="dims"></div>
        <h3 style="margin-top:14px">Comentario (solo si tiene una duda real)</h3>
        <textarea id="comentario" aria-label="Comentario"></textarea>
        <p class="aviso" id="aviso"></p>
        <div class="nav">
          <button id="anterior">← Anterior</button>
          <span class="leyenda">Atajos: <kbd>1</kbd>–<kbd>4</kbd> marcar · <kbd>←</kbd> <kbd>→</kbd> moverse</span>
          <button class="primario" id="siguiente">Siguiente →</button>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="final" class="panel oculto">
  <h2>Revisión final</h2>
  <p id="resumen"></p>
  <div class="nav" style="justify-content:flex-start">
    <button id="volver">← Volver a revisar</button>
    <button class="primario" id="descargar">Descargar mi hoja</button>
  </div>
  <div id="entrega" class="oculto">
    <p>Se descargó <strong id="nombre-archivo"></strong>. Envíelo por correo tal como está, sin abrirlo con Excel, e incluya en el mensaje esta huella del archivo:</p>
    <p class="hash" id="huella"></p>
  </div>
</section>

</main>
<script>
const DATOS = __DATOS__;
const N = DATOS.requisitos.length;
let rol = null, indice = 0, respuestas = {};

const $ = (id) => document.getElementById(id);
const clave = () => "codificacion_S1_" + rol + "_" + DATOS.huella_plantilla.slice(0, 12);

function guardar() {
  try { localStorage.setItem(clave(), JSON.stringify({ indice, respuestas })); } catch (e) {}
}
function cargar() {
  try {
    const s = JSON.parse(localStorage.getItem(clave()) || "null");
    if (s && s.respuestas) { respuestas = s.respuestas; indice = Math.min(s.indice || 0, N - 1); }
  } catch (e) {}
}
function respuesta(rf) {
  if (!respuestas[rf]) respuestas[rf] = { L: 0, R: 0, G: 0, C: 0, comentario: "" };
  return respuestas[rf];
}
const completo = (rf) => { const r = respuestas[rf]; return !!r && (r.L + r.R + r.G + r.C) > 0; };
const nCompletos = () => DATOS.requisitos.filter((q) => completo(q.rf_id)).length;

function escapar(t) {
  return t.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
function unir(partes) { return partes.filter((p) => p).join(" "); }

function pintarProgreso() {
  const n = nCompletos();
  $("barra").style.width = (100 * n / N) + "%";
  $("contador").textContent = rol ? `Codificador ${rol} · ${n} de ${N} completos` : "";
}

function pintarLista() {
  $("lista").innerHTML = "";
  DATOS.requisitos.forEach((q, i) => {
    const b = document.createElement("button");
    b.className = i === indice ? "actual" : "";
    b.innerHTML = `<span>${q.rf_id}</span><span class="punto ${completo(q.rf_id) ? "hecho" : ""}"></span>`;
    b.onclick = () => { indice = i; pintar(); };
    $("lista").appendChild(b);
  });
}

function pintar() {
  const q = DATOS.requisitos[indice];
  const r = respuesta(q.rf_id);
  $("titulo").textContent = `${q.rf_id}  (${indice + 1} de ${N})`;
  const a = [], b = [];
  q.segmentos.forEach(([op, ta, tb]) => {
    if (op === "equal") { a.push(escapar(ta)); b.push(escapar(tb)); }
    if (op === "delete" || op === "replace") a.push(`<del>${escapar(ta)}</del>`);
    if (op === "insert" || op === "replace") b.push(`<ins>${escapar(tb)}</ins>`);
  });
  $("texto-a").innerHTML = unir(a);
  $("texto-b").innerHTML = unir(b);

  $("dims").innerHTML = "";
  DATOS.dimensiones.forEach((d, k) => {
    const caja = document.createElement("div");
    caja.className = "dim" + (r[d.codigo] ? " marcada" : "");
    caja.innerHTML = `
      <label><input type="checkbox" ${r[d.codigo] ? "checked" : ""}>
        <span><span class="nombre"><kbd>${k + 1}</kbd> ${d.codigo} · ${escapar(d.nombre)}</span><br>
        <span class="pregunta">${escapar(d.pregunta)}</span></span></label>
      <details><summary>Definición completa</summary>
        <p><strong>Definición:</strong> ${escapar(d["Definición"])}</p>
        <p><strong>Incluye:</strong> ${escapar(d["Incluye"])}</p>
        <p><strong>Excluye:</strong> ${escapar(d["Excluye"])}</p>
        <p><strong>Ejemplo ancla (ficticio):</strong> ${escapar(d["Ejemplo ancla (ficticio)"])}</p>
      </details>`;
    caja.querySelector("input").onchange = (ev) => {
      r[d.codigo] = ev.target.checked ? 1 : 0;
      caja.classList.toggle("marcada", ev.target.checked);
      $("aviso").textContent = "";
      guardar(); pintarProgreso(); pintarLista();
    };
    $("dims").appendChild(caja);
  });
  $("comentario").value = r.comentario;
  $("aviso").textContent = "";
  $("anterior").disabled = indice === 0;
  $("siguiente").textContent = indice === N - 1 ? "Terminar →" : "Siguiente →";
  guardar(); pintarProgreso(); pintarLista();
}

function avanzar() {
  const q = DATOS.requisitos[indice];
  if (!completo(q.rf_id)) { $("aviso").textContent = "Marque al menos una dimensión antes de continuar."; return; }
  if (indice < N - 1) { indice++; pintar(); window.scrollTo(0, 0); } else { mostrarFinal(); }
}

function mostrarFinal() {
  const pendientes = DATOS.requisitos.filter((q) => !completo(q.rf_id)).map((q) => q.rf_id);
  $("trabajo").classList.add("oculto");
  $("final").classList.remove("oculto");
  $("entrega").classList.add("oculto");
  if (pendientes.length) {
    $("resumen").textContent = `Faltan por completar: ${pendientes.join(", ")}. Vuelva a revisarlos antes de descargar.`;
    $("descargar").disabled = true;
  } else {
    $("resumen").textContent = `Los ${N} requisitos tienen al menos una dimensión marcada. Si quiere, vuelva a revisar; si no, descargue su hoja.`;
    $("descargar").disabled = false;
  }
}

function campoCsv(v) {
  const s = String(v);
  return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}
function construirCsv() {
  const lineas = [DATOS.cabecera.join(",")];
  DATOS.requisitos.forEach((q) => {
    const r = respuestas[q.rf_id];
    const comentario = (r.comentario || "").replace(/\s+/g, " ").trim();
    lineas.push([q.rf_id, q.palabras_eliminadas, q.palabras_anadidas, r.L, r.R, r.G, r.C, comentario].map(campoCsv).join(","));
  });
  return lineas.join("\n") + "\n";
}

function sha256(bytes) {
  const K = new Uint32Array([0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]);
  const H = new Uint32Array([0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]);
  const len = bytes.length, total = Math.ceil((len + 9) / 64) * 64;
  const m = new Uint8Array(total); m.set(bytes); m[len] = 0x80;
  const dv = new DataView(m.buffer);
  dv.setUint32(total - 8, Math.floor(len / 0x20000000)); dv.setUint32(total - 4, (len << 3) >>> 0);
  const w = new Uint32Array(64);
  for (let o = 0; o < total; o += 64) {
    for (let i = 0; i < 16; i++) w[i] = dv.getUint32(o + 4 * i);
    for (let i = 16; i < 64; i++) {
      const s0 = ((w[i-15] >>> 7) | (w[i-15] << 25)) ^ ((w[i-15] >>> 18) | (w[i-15] << 14)) ^ (w[i-15] >>> 3);
      const s1 = ((w[i-2] >>> 17) | (w[i-2] << 15)) ^ ((w[i-2] >>> 19) | (w[i-2] << 13)) ^ (w[i-2] >>> 10);
      w[i] = (w[i-16] + s0 + w[i-7] + s1) >>> 0;
    }
    let [a, b, c, d, e, f, g, h] = H;
    for (let i = 0; i < 64; i++) {
      const s = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      const t1 = (h + s + ((e & f) ^ (~e & g)) + K[i] + w[i]) >>> 0;
      const t2 = ((((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10))) + ((a & b) ^ (a & c) ^ (b & c))) >>> 0;
      h = g; g = f; f = e; e = (d + t1) >>> 0; d = c; c = b; b = a; a = (t1 + t2) >>> 0;
    }
    H[0] += a; H[1] += b; H[2] += c; H[3] += d; H[4] += e; H[5] += f; H[6] += g; H[7] += h;
  }
  return Array.from(H, (x) => x.toString(16).padStart(8, "0")).join("");
}

function descargar() {
  const texto = construirCsv();
  const bytes = new TextEncoder().encode(texto);
  const nombre = `hoja_codificador_${rol}.csv`;
  const url = URL.createObjectURL(new Blob([bytes], { type: "text/csv;charset=utf-8" }));
  const a = document.createElement("a");
  a.href = url; a.download = nombre; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  $("nombre-archivo").textContent = nombre;
  $("huella").textContent = sha256(bytes);
  $("entrega").classList.remove("oculto");
}

$("n-rf").textContent = N;
DATOS.reglas.forEach((t) => { const li = document.createElement("li"); li.textContent = t; $("reglas").appendChild(li); });
document.querySelectorAll("[data-rol]").forEach((b) => b.onclick = () => {
  rol = b.dataset.rol; cargar();
  $("inicio").classList.add("oculto"); $("trabajo").classList.remove("oculto");
  pintar();
});
$("anterior").onclick = () => { if (indice > 0) { indice--; pintar(); } };
$("siguiente").onclick = avanzar;
$("volver").onclick = () => { $("final").classList.add("oculto"); $("trabajo").classList.remove("oculto"); pintar(); };
$("descargar").onclick = descargar;
$("comentario").oninput = (ev) => { respuesta(DATOS.requisitos[indice].rf_id).comentario = ev.target.value; guardar(); };
document.addEventListener("keydown", (ev) => {
  if ($("trabajo").classList.contains("oculto") || ev.target.tagName === "TEXTAREA") return;
  if (ev.key >= "1" && ev.key <= "4") { $("dims").querySelectorAll("input")[+ev.key - 1].click(); }
  if (ev.key === "ArrowRight") avanzar();
  if (ev.key === "ArrowLeft" && indice > 0) { indice--; pintar(); }
});
pintarProgreso();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
