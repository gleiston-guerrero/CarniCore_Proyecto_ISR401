# Retrospectiva del equipo — Proyecto CarniCore

**Asignatura:** Ingeniería de Requisitos (ISR-401 / 20303) — 2026–2027 PPA
**Repositorio:** https://github.com/gleiston-guerrero/CarniCore_Proyecto_ISR401
**Fecha:** 2026-09-16 *(actualizar a la fecha real del commit de cierre antes de firmar)*
**Integrantes:** Castro Bajaña Ariel Omar · Crespo Espinoza Kleber Obed · Gamarra Araujo Edhu Xavier ·
Pérez Ruiz Carlos Andrés · Quintero Gende Erick Jahir
**Estado del repositorio a la fecha de este documento:** HEAD `6afa2a0`, 652 commits totales.

> Este documento se redacta después de aplicar las correcciones de cierre del examen suspenso
> (§4 flujos alternativos y matriz de trazabilidad, §12 paquete de datos, §16 esta misma
> retrospectiva, §2 CHANGELOG) y antes de la regeneración final de los manifiestos de integridad
> y la creación de la etiqueta anotada de cierre (§3), conforme al orden de ejecución de la guía.
> **§3 es, a la fecha de esta versión, el único punto de la rúbrica que sigue pendiente.**

---

## 1. Qué hicimos

El proyecto se desarrolló entre el **28 de julio y el 15 de septiembre de 2026**, con 16 sesiones
de trabajo remoto asíncrono registradas hasta el 14/09 en `10_Autoria/bitacora_sesiones.csv`
(`aporte_individual.md` documenta 514 commits hasta el 08/09), más el trabajo de cierre del
15/09 que llevó el repositorio a **631 commits** (`git rev-list --count HEAD` sobre `db51466`,
verificado directamente contra el historial de Git, no contra el conteo de `aporte_individual.md`,
que a la fecha de este documento aún no se actualizó con la última sesión). El trabajo se
organizó en cuatro bloques:

- **Elicitación y modelado (28/07 – 02/08, SES-001 a SES-004):** estructura del repositorio,
  entrevistas de campo (16 informantes), protocolo ético, consentimientos, y el primer ERS/SRS
  (versión 2A). Se sentaron las bases de trazabilidad y del MVP ejecutable.
- **Componente empírico y manuscrito (01/09 – 04/09, SES-007 a SES-009):** migración del ERS a
  la versión 2B v2.0, panel de tres expertos clasificando los 27 RF de forma ciega, cálculo del
  acuerdo interevaluador (κ de Cohen y de Fleiss), matriz de confusión detector-vs-panel,
  bootstrap IC95% y análisis de potencia; redacción y primera compilación del manuscrito.
- **Integridad, reproducibilidad y cierre (05/09 – 14/09, SES-010 a SES-016):** esta fue la
  fase más costosa y menos visible del proyecto. Ocupó 6 de las 16 sesiones y estuvo dedicada
  casi por completo a hacer reproducible, verificable y consistente lo que ya existía:
  corrección del metadato del ERS, **múltiples regeneraciones de `checksums.sha256` y
  `checksums_datos.sha256`** por problemas de BOM, terminadores de línea (CRLF vs LF) y
  autorreferencia del hash, y finalmente la detección y corrección de **DEV-03**: el corpus
  `rf27.json` sobre el que corría el detector de ambigüedad conservaba la redacción de una
  entrega anterior (2A) en 21 de los 27 requisitos, en vez de reflejar el ERS v2.0 entregado.
  Esa desviación se documentó en `07_Datos/desviaciones.md` y se resolvió reemplazando el
  mantenimiento manual del corpus por `extraer_rf_desde_tex.py`, un extractor determinista que
  lo regenera directamente desde el `.tex` fuente.

- **Cierre del examen suspenso (12/09 – 16/09/2026):** corrección del identificador y la fecha
  de `osf_registration`/`osf_deviations` (Crespo Espinoza Kleber Obed, Gamarra Araujo Edhu
  Xavier); corrección de la URL canónica del repositorio en `CITATION.cff`, `README.md` y
  `registro_deposito.md` tras el cambio de propietario (Gamarra Araujo Edhu Xavier, Quintero
  Gende Erick Jahir); eliminación de `rf25.json` y depósito del comprobante externo del
  registro previo de OSF (Quintero Gende Erick Jahir); a cada uno de los 12 casos de uso del
  ERS se añadió un flujo alternativo y una excepción explícitos (commits `9d35a98` a
  `f88d191`, uno por CU, recompilación en `40a7c8e`); se amplió la matriz de trazabilidad de
  66 a 90 filas con una columna `Flujo` nueva (`065633d`, `7fe89c9`); se redactó y firmaron
  los cinco integrantes de esta misma retrospectiva (`3cf3c43`, `323f3a9`); se completó el
  `CHANGELOG.md` con las versiones 2.2.1 a 2.3.2 y la entrada de cierre 2.4.0, y se documentó
  en el `README.md` la desviación de numeración de `09_Etica`/`11_Defensa` (`ce435b9`,
  `d6970ea`); y se actualizaron las fotografías del entorno y su inventario EXIF
  (`2839f0a`…`6afa2a0`).

Queda pendiente un solo punto, según el orden de ejecución de la guía: **regenerar por última
vez `checksums.sha256` y `checksums_datos.sha256`** (ahora mismo el manifiesto raíz falla,
porque el CHANGELOG, el README, el ERS y las fotos cambiaron después de la última regeneración)
**y crear la etiqueta anotada de cierre (§3)** sobre el commit que resulte de esa regeneración.
Con eso, los cinco puntos de la rúbrica del examen suspenso quedan en Hecho.

## 2. Quién hizo qué

Distribución real de commits, contada directamente sobre `git log` sobre el estado actual del
repositorio (HEAD `6afa2a0`, 652 commits, `.mailmap` aplicado para unificar alias de usuario) —
no sobre el conteo de `aporte_individual.md`, cuyo total histórico (514, al 08/09) se actualizó
en paralelo a este documento; ver la nota de esa actualización para el detalle de por qué los
totales no son una simple suma "histórico + nuevos":

| Integrante | GitHub | Commits | % | Rol principal observado en la bitácora |
|---|---|---:|---:|---|
| Pérez Ruiz Carlos Andrés | @cperezr3 | 144 | 22.09% | Integridad del repositorio: manifiestos de checksums, registro de depósito, cierre del pipeline |
| Quintero Gende Erick Jahir | @equinteroj | 142 | 21.78% | Entrevistas de campo, notas de campo, documentación OSF, matriz de trazabilidad, flujos CU-01 a CU-06, DEV-03 y retrospectiva |
| Gamarra Araujo Edhu Xavier | @EdhuXav | 141 | 21.63% | Liderazgo técnico, estructura del repositorio, evidencias, ética, cambio de URL del repo y flujos CU-07 a CU-12 |
| Crespo Espinoza Kleber Obed | @kcrespoe | 126 | 19.33% | Componente empírico: panel de expertos, kappa, matriz de confusión, corrección de osf_registration |
| Castro Bajaña Ariel Omar | @arielca868 | 99 | 15.18% | Modelado UML, trazabilidad, corrección de figuras |
| **Total** | — | **652** | **100%** | |

La distribución sigue siendo equilibrada (entre 15.18% y 22.09%); ningún integrante concentra el
trabajo crítico de un único entregable. Esto se sostuvo hasta el final del cierre del examen
suspenso: los flujos alternativos de los CU se repartieron entre Erick Jahir Quintero Gende
(CU-01 a CU-06) y Edhu Xavier Gamarra Araujo (CU-07 a CU-12); la corrección DEV-03 y el comprobante
del registro previo quedaron a cargo de Erick Jahir Quintero Gende; la corrección del identificador
OSF, a cargo de Kleber Obed Crespo Espinoza; y la regeneración final de checksums y el CHANGELOG,
como el resto del trabajo de integridad del proyecto, a cargo de Carlos Andrés Pérez Ruiz y
Edhu Xavier Gamarra Araujo.

*(Sustituir o ampliar esta sección con el detalle de tareas puntuales — por ejemplo, quién
redactó qué caso de uso o qué script — según lo recuerde cada integrante; la bitácora completa
por sesión está en `10_Autoria/bitacora_sesiones.csv`.)*

## 3. Qué aprendimos

- **La reproducibilidad no es un paso final, es un costo recurrente.** Seis de las dieciséis
  sesiones del proyecto (37%) se dedicaron a hacer que los manifiestos de integridad
  verificaran limpio (BOM, EOL, autorreferencia del hash) y a sincronizar el corpus con el ERS.
  Si hubiéramos fijado desde el inicio una convención de codificación y terminador de línea
  (`.gitattributes`) y un script único de regeneración de checksums, ese tiempo se habría
  reducido de forma significativa.
- **Un corpus mantenido a mano es una desviación esperando ocurrir.** DEV-03 (21 de 27 RF
  desincronizados) no fue un error puntual: fue la consecuencia directa de mantener `rf27.json`
  editado manualmente en paralelo a un ERS que seguía evolucionando. La solución no fue corregir
  el archivo una vez, sino eliminar la posibilidad de que se repita (`extraer_rf_desde_tex.py`
  como fuente única de verdad). La lección: cuando un artefacto se deriva de otro, debe
  generarse por script, no mantenerse a mano.
- **Declarar una desviación no basta si no se verifica que se ejecutó.** El equipo aprendió,
  durante el cierre, la diferencia entre documentar una corrección y demostrarla: no alcanza con
  que `scripts/README.md` afirme que el corpus se regeneró y que las salidas son idénticas byte
  a byte — hay que volver a ejecutar la cadena sobre un árbol limpio y comprobarlo.
- **La trazabilidad de flujos alternativos y excepciones se dejó para el final, y no debió ser
  así.** Especificar solo el flujo principal de los 12 casos de uso fue más rápido en su momento,
  pero dejó al ERS incompleto según IEEE 29148 y generó trabajo de corrección bajo presión de
  tiempo en el examen suspenso, en vez de ser parte natural de la especificación inicial.
- **La distribución de trabajo por bloques temáticos (evidencias, empírico, integridad) funcionó
  mejor que dividir por "quien tenga tiempo esa semana"**, porque permitió que cada persona
  desarrollara contexto profundo en su área en vez de retrabajar decisiones ya tomadas.

## 4. Firma

Este documento fue elaborado y revisado por los cinco integrantes del equipo, quienes dan fe de
que su contenido refleja el desarrollo real del proyecto.

| Integrante | Firma / conformidad |
|---|---|
| Castro Bajaña Ariel Omar | Castro Bajaña Ariel Omar |
| Crespo Espinoza Kleber Obed | Crespo Espinoza Kleber Obed |
| Gamarra Araujo Edhu Xavier | Gamarra Araujo Edhu Xavier |
| Pérez Ruiz Carlos Andrés | Pérez Ruiz Carlos Andrés |
| Quintero Gende Erick Jahir | Quintero Gende Erick Jahir |
