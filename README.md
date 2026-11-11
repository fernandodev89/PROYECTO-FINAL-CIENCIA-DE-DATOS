# Brecha de equipamiento digital y pobreza en Guatemala

Tema elegido para el proyecto de Ciencia de Datos de estudiantes de Ingeniería en Informática y Sistemas.

Abre Informe_Brecha_Digital.html en un navegador. Contiene el desarrollo A–E, seis gráficas, hallazgos y una propuesta de ingeniería. Funciona sin conexión y puedes imprimirlo o guardarlo como PDF.

La fuente estadística es ENCOVI 2023 del INE. Los archivos descargados son copias procesadas y difundidas por OES DataLab / Guate en Datos, con diccionario dentro de cada Excel. No son la base completa original del INE. La guía oficial confirma la estructura y el método de expansión. El portal directo de bases del INE bloqueó la descarga automática; se deja constancia de la fuente alternativa utilizada.

## Qué contiene

- Dos archivos Excel fuente conservados: microdato de equipamiento y resumen ponderado.
- 548,200 observaciones hogar–artículo de 10,964 hogares y 50 artículos; no son hogares independientes.
- 7,400 celdas de resumen por departamento, área, pobreza y artículo.
- CSV preparados, revisión de nulos y una inconsistencia observada, tasas ponderadas y gráficas.
- Consultas Power Query para realizar la preparación dentro de Power BI y medidas DAX.

## Reproducir el análisis

Se requiere **Python 3.10 o posterior**. No es necesario instalar paquetes adicionales.

1. Descarga y descomprime el repositorio.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Ejecuta el comando correspondiente:

**En macOS:**

```bash
python3 analisis.py
```

**En Windows:**

```powershell
python analisis.py
```

Mantén `leer_xlsx.py` junto a `analisis.py` y los dos archivos Excel fuente dentro de la carpeta `datos/`.

Al finalizar, abre `Informe_Brecha_Digital.html` en un navegador para consultar el informe.

## Alcance

El tema mide tenencia de equipos. No mide conexión a internet, habilidades digitales ni desempeño académico. Las preguntas principales son la relación de pobreza con laptops, computadoras de escritorio, tablets e impresoras y las diferencias entre áreas y departamentos. Es un análisis descriptivo y exploratorio, sin inferencias causales.

No se puede unir el microdato a pobreza o territorio porque el archivo descargado carece de esas columnas. El resumen ponderado sí contiene esos cruces. No se inventan claves ni se duplican denominadores entre equipos. Las tasas se recalculan desde los conteos expandidos publicados, que tienen redondeo.

Los hogares con pobreza 0 se etiquetan Sin clasificar. Las comparaciones de pobreza los excluyen y el resto de los archivos los conserva. Los vacíos que derivan de no poseer un artículo no se imputan con promedios.

## Dashboard en Power BI

La carpeta `powerbi/` incluye:

- `Brecha_Digital_Guatemala.pbix`: dashboard editable.
- `Brecha_Digital_Guatemala.pdf`: versión exportada para consultar.
- Consultas Power Query y medidas DAX utilizadas.

El dashboard contiene tres páginas:

1. **Pobreza y tecnología:** compara la tenencia de cuatro equipos
   según pobreza y permite filtrar por departamento y área.
2. **Comparación territorial:** presenta la tenencia de laptop
   por departamento y área, con filtro por pobreza.
3. **Hallazgos y metodología:** resume resultados, tratamiento
   de datos, limitaciones y una propuesta de ingeniería.

### Abrir y actualizar el dashboard

Para editar el archivo `.pbix`, utiliza Power BI Desktop en Windows.
En Mac puedes consultar el PDF y el informe HTML.

Para actualizar los datos en otra computadora:

1. Descarga y descomprime el repositorio completo.
2. Abre `powerbi/Brecha_Digital_Guatemala.pbix`.
3. En **Transformar datos → Configuración de origen de datos**,
   selecciona cada archivo Excel y pulsa **Cambiar origen**.
4. Selecciona el Excel correspondiente dentro de `datos/`.
5. Aplica los cambios y pulsa **Actualizar**.

Las rutas guardadas pueden corresponder a la computadora donde
se creó el dashboard.

## Fuentes

- https://www.ine.gob.gt/pobreza-menu/
- https://www.ine.gob.gt/wp-content/uploads/2024/11/Guia-para-el-uso-de-bases-de-datos_v_final.pdf
- https://guateendatos.org.gt/oes-datalab/
- Archivo de microdatos: https://guateendatos.org.gt/wp-content/uploads/encovi2023-equipamiento.xlsx?v=10226383
- Archivo de resumen: https://guateendatos.org.gt/wp-content/uploads/encovi2023-equipamiento-resumen.xlsx?v=367801
- Estructura de referencia A–E: https://github.com/juanjluarca/data-science
