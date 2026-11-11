# Brecha de equipamiento digital y pobreza en Guatemala

Proyecto final de Ciencia de Datos de Ingeniería en Informática y Sistemas.

El proyecto analiza la tenencia de computadoras de escritorio, laptops, tablets e impresoras en los hogares de Guatemala según pobreza, área de residencia y departamento.

Integra **Python** para preparación y validación de datos, **R** para análisis estadístico y segmentación, **Quarto** para el informe reproducible y **Power BI** para explorar los resultados.

## Consultar los resultados

- **Informe principal:** abre [Informe_Quarto.html](Informe_Quarto.html) en un navegador después de descargar el repositorio. Incluye narrativa, código, tablas, gráficas, clustering y conclusiones.
- **Fuente del informe:** [Informe_Brecha_Digital.qmd](Informe_Brecha_Digital.qmd).
- **Dashboard editable:** [Brecha_Digital_Guatemala.pbix](powerbi/Brecha_Digital_Guatemala.pbix).
- **Dashboard en PDF:** [Brecha_Digital_Guatemala.pdf](powerbi/Brecha_Digital_Guatemala.pdf).

El informe HTML tiene sus recursos incorporados y puede consultarse sin conexión. GitHub permite descargarlo; para visualizarlo como página, ábrelo localmente en un navegador.

## Preguntas de investigación

1. ¿Cómo varía la tenencia de equipos digitales según la condición de pobreza?
2. ¿Qué diferencias existen entre áreas rurales y urbanas?
3. ¿Cómo se distribuye el equipamiento entre departamentos?
4. ¿Qué departamentos presentan perfiles similares de equipamiento?

## Datos utilizados

La fuente estadística es la **ENCOVI 2023 del Instituto Nacional de Estadística de Guatemala**.

Los archivos utilizados son copias procesadas y difundidas por **OES DataLab / Guate en Datos**, con documentación dentro de los Excel. No corresponden a la base original completa del INE.

| Archivo | Contenido | Granularidad |
|---|---|---|
| `datos/equipamiento_fuente.xlsx` | 548,200 registros de 10,964 hogares y 50 artículos | Un registro por hogar y artículo |
| `datos/resumen_fuente.xlsx` | 7,400 registros de 148 grupos y 50 artículos | Un registro por departamento, área, pobreza y artículo |

Las 548,200 filas no representan hogares independientes: cada hogar aparece una vez por artículo.

El microdato descargado no contiene pobreza, departamento ni factor de expansión. Por ello, las comparaciones socioeconómicas y territoriales se calculan desde el resumen ponderado, sin inventar vínculos entre ambos archivos.

Los Excel fuente se conservan sin modificar en `datos/`. Las URL de descarga se incluyen en la sección de fuentes.

## Metodología

### Preparación con Python

El script `analisis.py`, apoyado por `leer_xlsx.py`:

- Lee los archivos Excel.
- Comprueba claves únicas y consistencia de los denominadores.
- Revisa valores ausentes e inconsistencias.
- Identifica los cuatro equipos digitales.
- Genera tablas CSV, controles de calidad y gráficas.
- Calcula tasas por pobreza, área y departamento.

Python utiliza únicamente su biblioteca estándar.

### Análisis con R

El script `analisis_complementario.R`:

- Reproduce las tasas de tenencia de laptop por área.
- Calcula estadísticas de las tasas de los 22 departamentos.
- Genera gráficos de distribución.
- Calcula correlaciones de Spearman entre equipos.
- Aplica clustering jerárquico con distancia euclidiana y Ward.D2.
- Compara soluciones de dos a cinco grupos mediante silueta promedio.
- Exporta resultados a CSV.

Las variables del clustering se estandarizan. Cada departamento recibe igual peso. Este procedimiento es determinista y no utiliza inicialización aleatoria.

### Integración con Quarto

`Informe_Brecha_Digital.qmd` ejecuta la preparación en Python y el análisis en R para generar `Informe_Quarto.html`.

El informe combina contexto, metodología, código, resultados, interpretación, limitaciones y referencias.

## Decisiones de limpieza y cálculo

- La categoría de pobreza `0` se etiqueta como **Sin clasificar**.
- Los 34 hogares de la muestra sin clasificación de pobreza se conservan en los datos y se excluyen de las comparaciones socioeconómicas.
- Los valores ausentes asociados a no poseer un artículo se conservan como nulos; no se imputan con promedios.
- Se registra una inconsistencia en un artículo no digital: un hogar declara no poseer una plancha eléctrica, pero informa una unidad. El archivo original se conserva y esa cantidad no se incluye en los conteos de unidades de poseedores.
- Las tasas se calculan como la suma de hogares expandidos con un artículo dividida entre la suma de hogares expandidos del mismo conjunto de grupos, multiplicada por 100.
- No se promedian porcentajes departamentales para estimar la tasa nacional.
- No se suman poseedores de distintos equipos para estimar hogares con “algún equipo”, porque un hogar puede poseer varios.
- Los valores atípicos no se eliminan únicamente por aparecer alejados del resto.

## Principales resultados

En las comparaciones que excluyen hogares sin clasificación de pobreza:

- La tenencia de laptop es **23.34 %** en hogares no pobres y **0.77 %** en hogares en pobreza extrema: una diferencia de **22.57 puntos porcentuales**.
- La tenencia de laptop es **21.11 %** en áreas urbanas y **4.89 %** en áreas rurales.
- La mayor correlación de Spearman entre tasas departamentales corresponde a computadoras de escritorio e impresoras: **0.836**.
- Entre las soluciones de clustering evaluadas, dos grupos presentan la mayor silueta promedio: **0.698**.
- Guatemala y Sacatepéquez forman el grupo con mayores tasas promedio en los cuatro equipos; los otros 20 departamentos integran el segundo perfil territorial.

Los números asignados a los grupos son identificadores, no categorías oficiales ni niveles de pobreza.

## Requisitos

Para reproducir el informe:

- Python 3.10 o posterior.
- R.
- Quarto.
- Paquetes de R: `knitr`, `rmarkdown`, `reticulate` y `cluster`.
- RStudio, recomendado para abrir el proyecto y renderizar el informe.

Para editar el dashboard:

- Power BI Desktop en Windows.

En macOS pueden ejecutarse Python, R y Quarto, y consultarse el HTML y el PDF. En este proyecto se utilizó una máquina virtual de Windows para Power BI Desktop.

## Reproducir el informe completo

1. Clona el repositorio o descárgalo mediante **Code → Download ZIP** y descomprímelo.
2. Abre el archivo `.Rproj` de la raíz del proyecto en RStudio.
3. Instala los paquetes desde la pestaña **Console**:

```r
install.packages(
  c("knitr", "rmarkdown", "reticulate", "cluster"),
  repos = "https://cloud.r-project.org"
)
```

4. Comprueba que Python esté disponible. Desde la pestaña **Terminal**:

**macOS:**

```bash
python3 --version
```

**Windows:**

```powershell
python --version
```

5. Abre `Informe_Brecha_Digital.qmd`.
6. Presiona **Render**.

El documento ejecutará Python y R y generará **`Informe_Quarto.html`**.

Mantén los scripts en la raíz del proyecto y los Excel fuente dentro de `datos/`. El procesamiento utiliza rutas relativas.

### Renderizar desde una terminal

Si Quarto está disponible en el PATH, también puedes ejecutar desde la raíz:

```bash
quarto render Informe_Brecha_Digital.qmd
```

Si el comando no se reconoce, utiliza el botón **Render** de RStudio.

### Seleccionar Python manualmente

El informe busca primero `python3` y después `python`. Si selecciona una instalación incorrecta, ajusta la llamada a `reticulate::use_python()` del bloque `configurar-python` con la ruta del intérprete disponible en tu computadora.

Ese ajuste es local y debe documentarse si se modifica el archivo.

## Ejecutar los scripts por separado

Desde una terminal situada en la raíz del proyecto:

**macOS:**

```bash
python3 analisis.py
Rscript analisis_complementario.R
```

**Windows:**

```powershell
python analisis.py
Rscript analisis_complementario.R
```

Ejecuta Python antes que R: el análisis complementario utiliza los CSV preparados por Python.

Estos comandos requieren que Python y Rscript estén disponibles en el PATH. En RStudio también puedes abrir `analisis_complementario.R` y pulsar **Source**, después de ejecutar la preparación en Python.

`analisis.py` todavía genera `Informe_Brecha_Digital.html`, correspondiente al informe auxiliar anterior. **El informe principal de entrega es `Informe_Quarto.html`, generado desde Quarto.**

## Estructura del repositorio

```text
/
├── README.md
├── archivo del proyecto .Rproj
├── analisis.py
├── leer_xlsx.py
├── analisis_complementario.R
├── Informe_Brecha_Digital.qmd
├── Informe_Quarto.html
├── GUIA_POWER_BI.md
├── VERIFICACION.txt
├── datos/
│   ├── equipamiento_fuente.xlsx
│   ├── resumen_fuente.xlsx
│   └── tablas preparadas y resultados CSV
├── graficas/
│   └── gráficas generadas por Python
└── powerbi/
    ├── Brecha_Digital_Guatemala.pbix
    ├── Brecha_Digital_Guatemala.pdf
    └── consultas Power Query y medidas DAX
```

`VERIFICACION.txt` registra controles del procesamiento Python; no sustituye la comprobación del dashboard o del renderizado de Quarto.

## Dashboard en Power BI

El dashboard contiene tres páginas:

1. **Pobreza y tecnología:** compara la tenencia de cuatro equipos según pobreza, con filtros de departamento y área.
2. **Comparación territorial:** presenta la tenencia de laptop por departamento y área, con filtro de pobreza.
3. **Hallazgos y metodología:** resume resultados, preparación, limitaciones y propuesta de ingeniería.

El modelo relaciona `Grupos[GrupoID]` con `Equipamiento[GrupoID]` mediante una relación de uno a varios y filtro en una sola dirección, desde Grupos hacia Equipamiento.

### Abrir y actualizar el dashboard

1. Abre `powerbi/Brecha_Digital_Guatemala.pbix` en Power BI Desktop.
2. Para actualizar los datos, entra a **Transformar datos → Configuración de origen de datos**.
3. Selecciona cada origen Excel y pulsa **Cambiar origen**.
4. Busca el archivo correspondiente dentro de `datos/`.
5. Aplica los cambios y pulsa **Actualizar**.

Las rutas de los Excel guardadas en el `.pbix` pueden corresponder a la computadora donde se creó el dashboard. Deben ajustarse al actualizarlo en otra máquina.

## Alcance y limitaciones

- El estudio mide posesión de equipos, no acceso a internet, habilidades digitales ni rendimiento académico.
- Los resultados corresponden a 2023.
- Se utilizan archivos derivados difundidos por OES DataLab.
- Los conteos expandidos publicados presentan redondeo.
- No se dispone del diseño muestral completo para calcular intervalos que incorporen toda la incertidumbre de la encuesta.
- Las correlaciones son departamentales: no permiten inferir posesión conjunta de equipos en los mismos hogares.
- Las medias de tasas departamentales dan igual peso a cada departamento y no equivalen a tasas nacionales de hogares.
- El clustering es exploratorio. Su silueta mide separación interna, no precisión predictiva ni estabilidad.
- El grupo de 20 departamentos conserva diferencias internas importantes.
- Las asociaciones observadas no demuestran causalidad.

## Propuesta de ingeniería

Se propone evaluar un programa de reacondicionamiento y préstamo de computadoras, acompañado de centros comunitarios con software libre y capacitación.

Los resultados pueden orientar un diagnóstico local, pero la selección de beneficiarios y ubicaciones requiere información adicional sobre demanda, infraestructura y conectividad.

Un piloto permitiría registrar disponibilidad y fallas de equipos, personas beneficiadas, frecuencia de uso, costo por beneficiario y participación en la capacitación.

## Integrantes y contribuciones

| Integrante | Participación | Tareas realizadas |
|---|---:|---|
| Fernando Contreras | 60 % | Preparación y validación de datos con Python; construcción del dashboard en Power BI; integración del informe reproducible en Quarto y revisión general de resultados. |
| Joshua Ascoli | 40 % | Análisis complementario en R; estadísticas descriptivas, correlaciones y clustering; apoyo en la interpretación de hallazgos, documentación y preparación de la exposición. |

## Declaración de autoría y contribución

Fernando Contreras y Joshua Ascoli asumen la responsabilidad del
trabajo presentado, de acuerdo con las contribuciones declaradas.
Ambos participan en la revisión de los resultados y en su defensa oral.

Se utilizó asistencia de inteligencia artificial como apoyo en código,
documentación y orientación técnica. Las fuentes de datos utilizadas
se identifican en el informe y en este repositorio.

### Declaración de autoría y contribución

Las personas indicadas asumen la responsabilidad del trabajo presentado y de la revisión e interpretación de sus resultados. Los datos y las fuentes externas se identifican en el informe y en este repositorio.

Se utilizó asistencia de inteligencia artificial para apoyar la elaboración de código, documentación y orientación técnica. Esta asistencia no sustituye la responsabilidad de los integrantes de comprender, verificar y defender el trabajo.

## Presentación oral

La defensa se apoya en el informe Quarto y el dashboard de Power BI, con una duración prevista de 15 a 20 minutos.

El recorrido comprende el problema, los datos, la preparación, los principales hallazgos, la segmentación territorial, la demostración del dashboard y las conclusiones.

## Fuentes y condiciones de uso

- [INE Guatemala: pobreza y ENCOVI](https://www.ine.gob.gt/pobreza-menu/)
- [INE: guía para el uso de las bases ENCOVI 2023](https://www.ine.gob.gt/wp-content/uploads/2024/11/Guia-para-el-uso-de-bases-de-datos_v_final.pdf)
- [OES DataLab / Guate en Datos](https://guateendatos.org.gt/oes-datalab/)
- [Archivo de microdatos de equipamiento](https://guateendatos.org.gt/wp-content/uploads/encovi2023-equipamiento.xlsx?v=10226383)
- [Archivo de resumen de equipamiento](https://guateendatos.org.gt/wp-content/uploads/encovi2023-equipamiento-resumen.xlsx?v=367801)
- [Repositorio de referencia inicial para la estructura A–E](https://github.com/juanjluarca/data-science)

La licencia específica y las condiciones de redistribución de los archivos derivados de OES DataLab **siguen pendientes de verificación**. No se atribuye a estos datos una licencia abierta sin confirmación. La disponibilidad pública no equivale por sí sola a autorización de redistribución.

Cualquier licencia que se incorpore para el código del proyecto deberá distinguirse de las condiciones aplicables a los datos de terceros.