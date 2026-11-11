# Power BI: brecha de equipamiento digital y pobreza

## Carga y limpieza dentro de Power Query

Extrae el ZIP. En Power BI Desktop crea una Consulta en blanco. Abre Editor avanzado y pega powerbi/Equipamiento.pq. Cambia Ruta por la ubicación de datos/resumen_fuente.xlsx. Nombra la consulta Equipamiento.

Esta consulta importa el Excel, promueve encabezados, aplica tipos, recodifica pobreza 0 como Sin clasificar y crea claves y una tasa recalculada. Mantiene los valores desconocidos de valor y antigüedad como null. La limpieza se podrá mostrar dentro de Power Query durante la exposición.

Crea otra consulta llamada Grupos con powerbi/Grupos.pq. Cierra y aplica. Relaciona Grupos[GrupoID], lado 1, con Equipamiento[GrupoID], lado muchos, filtro en una sola dirección desde Grupos. Cada grupo tiene 50 artículos. No sumes los hogares repetidos entre artículos.

Crea las medidas de Medidas_DAX.txt una por una. Tenencia del artículo: porcentaje con dos decimales. Brecha de laptop pp: decimal con dos decimales, en puntos porcentuales.

## Página 1: pobreza y acceso a equipos

- Tarjeta Hogares de muestra: 10,964 sin filtros.
- Barras: eje Equipamiento[Articulo], leyenda Grupos[Pobreza], valor Tenencia del artículo. Filtra EsEquipoDigital=1 y excluye Sin clasificar.
- Segmentador Grupos[Area].
- Segmentador Grupos[Departamento].
- Texto: ENCOVI 2023, resumen ponderado difundido por OES DataLab.

## Página 2: territorio

- Filtro de página ArticuloClave=2-2 (laptop).
- Barras por Grupos[Departamento] y Tenencia del artículo.
- Barras por Grupos[Area] y Tenencia del artículo.
- Tarjeta Brecha de laptop pp. No uses pobreza como eje para esta tarjeta: compara los dos grupos fijos dentro de los demás filtros.
- Tooltip: Hogares de muestra y Hogares con artículo. Interpreta con cautela grupos de muestra pequeños.

Usa las columnas de ubicación y pobreza de Grupos para que las tarjetas y los visuales compartan filtros.

## Página 3: calidad y propuesta de ingeniería

- Importa calidad_resumen.csv y calidad_microdatos.csv como tablas independientes.
- Explica nulos estructurales: si no posee un artículo, su cantidad, valor y antigüedad pueden no aplicar.
- Tabla con grupos Sin clasificar.
- Cuadro de texto: propuesta de laboratorios compartidos y aplicaciones educativas de bajo consumo.

## Verificación

- Grupos: 148 claves únicas, muestra total 10,964.
- Equipamiento: 7,400 filas; 50 artículos por grupo.
- Compara tasas con resultados_pobreza.csv, resultados_area.csv y resultados_departamento.csv, que excluyen Sin clasificar.
- Una tasa nacional debe ser suma de numeradores / suma de denominadores para UN artículo. Evita AVERAGE(TenenciaPct).
- Si se seleccionan varios artículos, las medidas de tenencia y hogares con artículo quedan vacías deliberadamente: no se sabe cuántos hogares tienen al menos uno a partir del resumen.
- El microdato no tiene departamento, pobreza ni ponderador. No lo relaciones al resumen por un ID inventado. Tampoco mezcles una tasa muestral sin ponderar con una estimación expandida.

Guarda el archivo como Brecha_Digital_Guatemala.pbix. Este paquete no incluye un .pbix generado ni validado en Power BI Desktop. Las consultas M y las medidas DAX requieren esa comprobación final.
