# Retrospectiva del equipo — Proyecto CarniCore

**Asignatura:** Ingeniería de Requisitos (ISR-401 / 20303) — 2026–2027 PPA
**Repositorio:** https://github.com/gleiston-guerrero/CarniCore_Proyecto_ISR401
**Fecha:** 16 de septiembre de 2026
**Integrantes:** Castro Bajaña Ariel Omar · Crespo Espinoza Kleber Obed · Gamarra Araujo Edhu Xavier ·
Pérez Ruiz Carlos Andrés · Quintero Gende Erick Jahir
**Estado del repositorio a la fecha de este documento:** HEAD `b7d58df`, 664 commits totales.

> Este documento se redacta después de aplicar las correcciones de cierre del examen suspenso
> señaladas en la guía del 15/09/2026 y en el informe de evaluación del 16/09/2026: §4 (flujo
> alternativo y excepción propios en los 12 casos de uso, con las contradicciones precondición–flujo
> corregidas, y la matriz de trazabilidad sincronizada tanto en `04_Trazabilidad/Matriz_Trazabilidad.csv`
> como en la tabla interna del ERS), §12 (paquete de datos) y §2 (CHANGELOG). La etiqueta anotada
> `v2.4.0` ya existe, pero apunta a un commit (`785b86d`) anterior a estas últimas correcciones de §4
> y §16; según la propia regla de dependencia de la guía, su estado efectivo queda congelado al
> estado de lo que etiqueta. **Falta crear una nueva etiqueta sobre el commit final, una vez firmada
> esta retrospectiva, para que §3 quede en Hecho.**
>
> **Alcance de esta retrospectiva.** El informe de evaluación del docente (16/09/2026, §5,
> "Calificación individual") establece que la calificación de esta fase corresponde a quienes la
> trabajaron, y que quien no registra commits en la fase de cierre no forma parte de ella. Verificado
> contra `git log`: desde el 14/09/2026 (fecha de corte que usa el propio informe docente) solo
> **Quintero Gende Erick Jahir** y **Gamarra Araujo Edhu Xavier** registran commits en el repositorio.
> **Castro Bajaña Ariel Omar, Crespo Espinoza Kleber Obed y Pérez Ruiz Carlos Andrés no forman parte
> de la fase de cierre del examen suspenso** y, en consecuencia, no firman esta retrospectiva de
> cierre (§4 más abajo). Esto no altera ni reescribe el historial de commits del repositorio: la
> participación de los cinco integrantes en el resto del proyecto (28/07 al 13/09/2026) permanece
> íntegra y verificable en `git log`, y así queda documentada en las secciones 1 y 2 de este mismo
> archivo. Lo que se declara aquí es, exclusivamente, que estos tres integrantes no trabajaron en
> la fase de cierre del examen suspenso evaluada por el informe del 16/09/2026.

---

## 1. Qué hicimos

El proyecto se desarrolló entre el **28 de julio y el 16 de septiembre de 2026**, con 16 sesiones
de trabajo remoto asíncrono registradas en `10_Autoria/bitacora_sesiones.csv` (ampliada el 16/09
con el detalle de las sesiones del 15 y 16 de septiembre), sobre un total de **664 commits**
(`git rev-list --count HEAD`, verificado directamente contra el historial de Git). El trabajo se
organizó en cinco bloques:

- **Elicitación y modelado (28/07 – 02/08, SES-001 a SES-004):** estructura del repositorio,
  entrevistas de campo (16 informantes), protocolo ético, consentimientos, y el primer ERS/SRS
  (versión 2A). Se sentaron las bases de trazabilidad y del MVP ejecutable.
- **Componente empírico y manuscrito (01/09 – 04/09, SES-007 a SES-009):** migración del ERS a
  la versión 2B v2.0, panel de tres expertos clasificando los 27 RF de forma ciega, cálculo del
  acuerdo interevaluador (κ de Cohen y de Fleiss), matriz de confusión detector-vs-panel,
  bootstrap IC95% y análisis de potencia; redacción y primera compilación del manuscrito.
- **Integridad, reproducibilidad y cierre inicial (05/09 – 12/09, SES-010 a SES-013):** corrección
  del metadato del ERS, múltiples regeneraciones de `checksums.sha256` y `checksums_datos.sha256`
  por problemas de BOM y terminadores de línea (Pérez Ruiz Carlos Andrés), y detección de **DEV-03**:
  el corpus `rf27.json` conservaba la redacción de la Entrega 3 (2A) en 21 de los 27 requisitos, en
  vez del ERS v2.0 entregado.
- **Corrección de identificadores y registro previo (13/09 – 14/09, SES-014 a SES-015):**
  corrección del identificador OSF en `osf_registration.tex`/`.pdf` (Crespo Espinoza Kleber Obed,
  con apoyo de Castro Bajaña Ariel Omar); corrección de la fecha errónea en `osf_deviations.tex`
  y resolución definitiva de DEV-03 —eliminación de `rf25.json` y reemplazo del mantenimiento
  manual del corpus por `extraer_rf_desde_tex.py`— y depósito del comprobante externo del registro
  previo de OSF (Gamarra Araujo Edhu Xavier y Quintero Gende Erick Jahir).
- **Cierre del examen suspenso (15/09 – 16/09/2026):** corrección de la URL canónica del
  repositorio en `CITATION.cff`, `README.md` y `registro_deposito.md` tras el cambio de propietario
  (Gamarra Araujo Edhu Xavier, Quintero Gende Erick Jahir); a los 12 casos de uso del ERS se les dio
  flujo alternativo y excepción propios, con condición de disparo y poscondición, y se resolvieron
  las cinco contradicciones entre precondición y flujo detectadas en la revisión docente del 16/09
  (commits `d6e503e`, `b7d58df` — Gamarra Araujo Edhu Xavier y Quintero Gende Erick Jahir); la
  matriz de trazabilidad se amplió de 66 a 90 filas con columna `Flujo`, y la tabla equivalente
  dentro del propio ERS (Sección 5) se sincronizó de 60 a 84 filas, incluida la creación de las
  historias de usuario HU-05 y HU-12 (mismos commits); se completó el `CHANGELOG.md` con las
  versiones 2.2.1 a 2.3.2 y la entrada de cierre 2.4.0, y se documentó en `README.md` la desviación
  de numeración de `09_Etica`/`11_Defensa` (Gamarra Araujo Edhu Xavier, commit `ce435b9`); la
  regeneración final de `checksums.sha256` —incluida la corrección del BOM que hacía que
  `sha256sum -c` omitiera la primera línea sin verificarla— quedó a cargo de Gamarra Araujo Edhu
  Xavier y Quintero Gende Erick Jahir (commits `785b86d`, `4142f7b`, `1e3c1f8`); y se actualizaron
  las fotografías del entorno y su inventario EXIF (Quintero Gende Erick Jahir, Gamarra Araujo Edhu
  Xavier).

## 2. Quién hizo qué

Distribución real de commits, contada directamente sobre `git log` sobre el estado actual del
repositorio (HEAD `b7d58df`, 664 commits, `.mailmap` aplicado para unificar alias de usuario):

| Integrante | GitHub | Commits | % | Rol principal observado en la bitácora y en el historial |
|---|---|---:|---:|---|
| Quintero Gende Erick Jahir | @equinteroj | 148 | 22.29% | Entrevistas de campo, notas de campo, documentación OSF, matriz de trazabilidad, flujos CU-01 a CU-06, DEV-03, retrospectiva, README de la etiqueta vigente |
| Gamarra Araujo Edhu Xavier | @EdhuXav | 147 | 22.14% | Liderazgo técnico, estructura del repositorio, evidencias, ética, cambio de URL del repositorio, flujos CU-07 a CU-12, CHANGELOG, manifiesto raíz final |
| Pérez Ruiz Carlos Andrés | @cperezr3 | 144 | 21.69% | Integridad del repositorio hasta el 12/09: manifiestos de checksums, registro de depósito, estabilización de BOM/EOL |
| Crespo Espinoza Kleber Obed | @kcrespoe | 126 | 18.98% | Componente empírico: panel de expertos, kappa, matriz de confusión; corrección del identificador OSF (13/09) |
| Castro Bajaña Ariel Omar | @arielca868 | 99 | 14.91% | Modelado UML, trazabilidad, corrección de figuras, apoyo en la corrección de osf_registration (13/09) |
| **Total** | — | **664** | **100%** | |

**Precisión sobre la fase de cierre (14/09 en adelante, mismo corte que usa el informe docente):**
en esta fase concreta solo registran commits Quintero Gende Erick Jahir y Gamarra Araujo Edhu
Xavier; ellos dos se repartieron el CHANGELOG, la corrección de los 12 casos de uso, la matriz de
trazabilidad (externa e interna del ERS) y la regeneración final de los manifiestos de integridad.
Pérez Ruiz Carlos Andrés hizo un trabajo real y verificable de integridad del repositorio hasta el
12/09, pero no tiene commits desde entonces. Crespo Espinoza Kleber Obed y Castro Bajaña Ariel
Omar participaron el 13/09 en la corrección del identificador OSF, un día antes del corte que usa
el informe docente. Por eso, y siguiendo el mismo criterio que aplicó el docente en su evaluación
del 16/09/2026, estos tres integrantes **no forman parte de la fase de cierre del examen
suspenso** y no firman este documento (§4) — sin que esto implique ningún cambio sobre su
participación ya registrada en el resto del historial del proyecto.

## 3. Qué aprendimos

- **La reproducibilidad no es un paso final, es un costo recurrente.** Una parte significativa de
  las sesiones del proyecto se dedicó a hacer que los manifiestos de integridad verificaran limpio
  (BOM, EOL, autorreferencia del hash) y a sincronizar el corpus con el ERS. Si hubiéramos fijado
  desde el inicio una convención de codificación y terminador de línea (`.gitattributes`) y un
  script único de regeneración de checksums, ese tiempo se habría reducido de forma significativa.
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
- **Especificar de más rápido no es especificar bien.** Los primeros flujos alternativos que
  escribimos para los 12 casos de uso pasaban el conteo automático de la guía (`grep -ci "flujo
  alternativo"`), pero cinco de ellos contradecían la propia precondición del caso de uso que
  decían extender, y tres excepciones no tenían poscondición propia. Pasar una verificación
  mecánica no es lo mismo que estar bien especificado: hizo falta una segunda revisión —esta vez
  de contenido, no de conteo— para que el ERS realmente cumpliera IEEE 29148.
- **Un documento firmado por una sola persona en un solo commit no acredita la conformidad de los
  demás.** La primera versión de esta misma retrospectiva se comiteó con las cinco firmas ya
  escritas por una sola persona. Lo corregimos: cada integrante debe registrar su propia
  conformidad con su propio commit (ver §4), no delegarla en quien redacta el documento.
- **La distribución de trabajo por bloques temáticos (evidencias, empírico, integridad) funcionó
  mejor que dividir por "quien tenga tiempo esa semana"**, porque permitió que cada persona
  desarrollara contexto profundo en su área en vez de retrabajar decisiones ya tomadas.

## 4. Firma

Este documento fue elaborado por Quintero Gende Erick Jahir y Gamarra Araujo Edhu Xavier a partir
del historial de commits verificado del repositorio. Firman únicamente estos dos integrantes,
porque son los únicos que registran commits en la fase de cierre del examen suspenso (ver el
alcance declarado al inicio de este documento y la nota de la sección 2); Castro Bajaña Ariel
Omar, Crespo Espinoza Kleber Obed y Pérez Ruiz Carlos Andrés no forman parte de esta fase y por
eso no firman aquí, sin que esto afecte su participación ya registrada en el resto del historial
del proyecto. Cada firmante da fe de que el contenido que le corresponde refleja el desarrollo
real de esta fase **registrando su conformidad con su propio commit** sobre este archivo (una
línea por persona, en un commit separado), no en un commit único hecho por el otro integrante.

| # | Integrante | Firma/Conformidad | 
|---|---|---|---|
| 1 | Gamarra Araujo Edhu Xavier | Edhu Gamarra |
| 2 | Quintero Gende Erick Jahir | Erick Quintero |
