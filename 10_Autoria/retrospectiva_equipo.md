# Retrospectiva del equipo — Proyecto CarniCore

**Asignatura:** Ingeniería de Requisitos (ISR-401 / 20303) — 2026–2027 PPA
**Repositorio:** https://github.com/gleiston-guerrero/CarniCore_Proyecto_ISR401
**Fecha:** 2026-09-15 *(actualizar a la fecha real del commit de cierre antes de firmar)*
**Integrantes:** Castro Bajaña Ariel Omar · Crespo Espinoza Kleber Obed · Gamarra Araujo Edhu Xavier ·
Pérez Ruiz Carlos Andrés · Quintero Gende Erick Jahir
**Estado del repositorio a la fecha de este documento:** HEAD `db51466`, 631 commits totales.

> Este documento se redacta después de aplicar las correcciones de cierre del examen suspenso
> (§4 flujos alternativos y matriz de trazabilidad, §12 paquete de datos) y antes de completar
> §2 (CHANGELOG), regenerar los manifiestos finales y crear la etiqueta anotada de cierre (§3),
> conforme al orden de ejecución de la guía.

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

- **Cierre del examen suspenso (15/09/2026, 17 commits, `9d35a98`…`db51466`):** se añadió a
  cada uno de los 12 casos de uso del ERS un flujo alternativo y una excepción explícitos
  (commits `9d35a98` a `f88d191`, uno por CU, más la recompilación `40a7c8e`); se amplió la
  matriz de trazabilidad de 66 a 90 filas con una columna `Flujo` nueva que traza cada flujo
  alternativo y excepción a su requisito y componente (`065633d`, `7fe89c9`); y se regeneró el
  manifiesto de integridad (`27371b0`) tras confirmar, reejecutando el pipeline completo sobre
  el corpus vigente, que ninguna cifra publicada cambia (`db51466`).

Quedan pendientes, según el orden de ejecución de la guía: completar el CHANGELOG con la entrada
del examen suspenso (§2), la regeneración final de ambos manifiestos ya con este documento y el
CHANGELOG incluidos, y la etiqueta anotada de cierre sobre el último commit (§3).

## 2. Quién hizo qué

Distribución real de commits, contada directamente sobre `git log` sobre el estado actual del
repositorio (HEAD `db51466`, 631 commits, `.mailmap` aplicado para unificar alias de usuario) —
no sobre el conteo de `aporte_individual.md`, que quedó fijado el 08/09 y no incluye ni las
sesiones SES-010 a SES-016 ni el cierre del 15/09:

| Integrante | GitHub | Commits | % | Rol principal observado en la bitácora |
|---|---|---:|---:|---|
| Pérez Ruiz Carlos Andrés | @cperezr3 | 144 | 22.8% | Integridad del repositorio: manifiestos de checksums, registro de depósito, cierre del pipeline |
| Gamarra Araujo Edhu Xavier | @EdhuXav | 133 | 21.1% | Liderazgo técnico, estructura del repositorio, evidencias, ética y cierre de flujos CU-07 a CU-12 |
| Quintero Gende Erick Jahir | @equinteroj | 129 | 20.4% | Entrevistas de campo, notas de campo, documentación OSF, matriz de trazabilidad y flujos CU-01 a CU-06 |
| Crespo Espinoza Kleber Obed | @kcrespoe | 126 | 20.0% | Componente empírico: panel de expertos, kappa, matriz de confusión |
| Castro Bajaña Ariel Omar | @arielca868 | 99 | 15.7% | Modelado UML, trazabilidad, corrección de figuras |
| **Total** | — | **631** | **100%** | |

La distribución sigue siendo equilibrada (entre 15.7% y 22.8%); ningún integrante concentra el
trabajo crítico de un único entregable. Esto se sostuvo incluso en el cierre del examen suspenso
del 15/09: los flujos alternativos de los CU se repartieron entre Erick Jahir Quintero Gende
(CU-01 a CU-06) y Edhu Xavier Gamarra Araujo (CU-07 a CU-12), y la regeneración final de
checksums quedó, como el resto del trabajo de integridad del proyecto, a cargo de Carlos Andrés
Pérez Ruiz.

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
