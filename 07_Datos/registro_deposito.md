# Registro de depósito de datos

Proyecto CarniCore — Sistema de Distribución y Trazabilidad de Carne
Equipo CCGaPQ — Universidad Técnica Estatal de Quevedo

Fecha de actualización: 2026-09-03

---

## 1. Estado del depósito

*Estado:* publicado / estructurado en Zenodo.

| Campo | Valor |
|---|---|
| Plataforma | Zenodo |
| Tipo de recurso | Dataset / Paquete de Replicación |
| Nombre del archivo principal | CarniCore_Zenodo_Package.zip |
| DOI de versión / Concept DOI | 10.5281/zenodo.22225854 |
| Registro previo OSF | https://osf.io/yp7t3 (Fecha: 2026-08-02) |
| Repositorio de trabajo (GitHub) | https://github.com/gleiston-guerrero/carnicore-requirements-ambiguity.git |
| Licencia del dataset abierto | CC BY 4.0 |
| Institución | Universidad Técnica Estatal de Quevedo |
| Proyecto | CarniCore — Sistema de Distribución y Trazabilidad de Carne |

---

## 2. Contenido exacto del paquete publicado (CarniCore_Zenodo_Package.zip)

El archivo comprimido y su estructura interna reflejan los elementos reales depositados para garantizar la reproducibilidad, el cumplimiento ético y la trazabilidad del análisis:

### 2.1. Documentación y Directrices Principales

- **ANONYMIZATION.md** (3.3 kB): Protocolo y pautas de anonimización aplicadas al conjunto de datos.
- **ÉTICA.md** (3.6 kB): Marco ético y consideraciones sobre el consentimiento y tratamiento de las entrevistas.
- **README_dataset.md** (5.2 kB): Descripción detallada de la estructura, variables y diccionarios del depósito.
- **Matriz_Trazabilidad.csv** (5.2 kB): Matriz que vincula requisitos, fuentes y componentes del sistema.
- **cuestionario_respuestas.csv** (22.9 kB): Respuestas estructuradas del cuestionario aplicado.
- **Categorías_detector.csv** (625 Bytes): Categorías analizadas por el script de detección de ambigüedad/requisitos.

### 2.2. Scripts y Automatización (Guiones/)

- **detector_ambiguedad.py** (6.1 kB): Script principal para la detección y análisis automatizado.
- **run_all.py** (7.7 kB): Script de ejecución global para reproducir la cadena analítica.
- **required.txt** (470 Bytes): Dependencias de software necesarias.
- **rf27.json** (7.2 kB): Archivo de configuración/datos estructurados del modelo o requisitos.

### 2.3. Asistencia de Modelos (prompts_llm/)

- **prompt_01_revision_preguntas_entrevista.md** (527 Bytes)
- **prompt_02_correccion_transcripcion.md** (473 Bytes)
- **prompt_03_revision_requisitos_esfuncional.md** (502 Bytes)

### 2.4. Transcripciones de Entrevistas Anonimizadas (transcripciones/)

El conjunto recopila las interacciones clave que sustentan la elicitación de requisitos del sistema:

- 2026-07-31_Propietaria_ENTR-05_Transcripcion.txt (12.3 kB)
- 2026-08-01_AdministradorDeBodega_ENTR-01_Transcripcion.txt (10.6 kB)
- 2026-08-01_AdministradorDeBodega_ENTR-02_Transcripcion.txt (12.4 kB)
- 2026-08-01_OperarioRecepciónPesaje_ENTR-04_Transcripcion.txt (11.2 kB)
- 2026-08-02_Carnicero_Despachador_ENTR-03_Transcripcion.txt (12.1 kB)
- 2026-08-29_Chofer_ENTR-06_Transcripcion.txt (8.8 kB)
- 2026-08-30_Recepcion_Bodega_ENTR-07_Transcripcion.txt (9.9 kB)
- 2026-08-31_Carnicero_Despachador_ENTR-14_Transcripcion.txt (9.6 kB)
- 2026-08-31_Chofer_Despachador_ENTR-15_Transcripcion.txt (9.8 kB)
- 2026-08-31_OperarioRecepciónPesaje_ENTR-08_Transcripcion.txt (8.4 kB)
- 2026-08-31_VendedorMostrador_ENTR-09_Transcripcion.txt (10.6 kB)
- 2026-08-31_VenderMostrador_ENTR-10_Transcripcion.txt (10.8 kB)
- 2026-08-31_Vendedor_Demostrador_ENTR-16_Transcripcion.txt (11.5 kB)
- 2026-09-01_Administrador_Contador_ENTR-12_Transcripcion.txt (10.9 kB)
- 2026-09-01_Chofer_Despacho_ENTR-13_Transcripcion.txt (11.7 kB)
- 2026-09-01_Encargada_Sucursal_ENTR-11_Transcripcion.txt

---

## 3. Notas críticas y defensa ante el tribunal

### 3.1. Sobre la precedencia temporal (OSF vs. Entrevistas)

- **Fecha del registro OSF:** 2 de agosto de 2026 (https://osf.io/yp7t3).
- **Primera transcripción registrada (ENTR-05):** 31 de julio de 2026 (y la sesión inicial ENTR-05 documentada el 28 de julio).
- **Argumento de defensa:** El protocolo pre-registrado en OSF ampara formalmente el *análisis metodológico y el funcionamiento del detector frente al panel experto* (ejecutado posterior al 2 de agosto). Las entrevistas de campo previas constituyen la fase de adquisición y elicitación de requisitos bajo aval ético institucional propio documentado en el repositorio.
