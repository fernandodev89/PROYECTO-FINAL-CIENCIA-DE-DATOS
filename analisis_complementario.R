# Análisis complementario en R
# Ejecutar desde la raíz del proyecto de RStudio.

datos <- read.csv(
  "datos/equipamiento_preparado.csv",
  fileEncoding = "UTF-8-BOM",
  stringsAsFactors = FALSE
)

# Validar estructura y claves
stopifnot(
  nrow(datos) == 7400,
  !anyDuplicated(datos[c("GrupoID", "ArticuloClave")])
)

# Seleccionar laptops y hogares con pobreza clasificada
laptops <- subset(
  datos,
  ArticuloClave == "2-2" & Pobreza != "Sin clasificar"
)

# Sumar conteos expandidos por área
resumen_area <- aggregate(
  cbind(ConArticulo, HogaresExpandido) ~ Area,
  data = laptops,
  FUN = sum
)

resumen_area$TenenciaPct <- with(
  resumen_area,
  100 * ConArticulo / HogaresExpandido
)

print(resumen_area)

# Visualización generada en R
barplot(
  resumen_area$TenenciaPct,
  names.arg = resumen_area$Area,
  col = "#507984",
  main = "Tenencia de laptop por área",
  ylab = "Porcentaje de hogares",
  ylim = c(0, 30)
)

# Tasas por departamento para los cuatro equipos
digital <- subset(
  datos,
  EsEquipoDigital == 1 & Pobreza != "Sin clasificar"
)

tasas_departamento <- aggregate(
  cbind(ConArticulo, HogaresExpandido) ~ Departamento + Articulo,
  data = digital,
  FUN = sum
)

tasas_departamento$TenenciaPct <- with(
  tasas_departamento,
  100 * ConArticulo / HogaresExpandido
)

# Distribución de las 22 tasas departamentales por equipo
estadisticas <- do.call(
  rbind,
  lapply(split(tasas_departamento, tasas_departamento$Articulo),
         function(x) {
           v <- x$TenenciaPct
           data.frame(
             Articulo = x$Articulo[1],
             Departamentos = length(v),
             Minimo = min(v),
             Mediana = median(v),
             Media = mean(v),
             Maximo = max(v),
             Desviacion = sd(v)
           )
         })
)

rownames(estadisticas) <- NULL
print(estadisticas, digits = 4)

write.csv(
  estadisticas,
  "datos/estadisticas_departamentales_R.csv",
  row.names = FALSE
)

margen_anterior <- par(mar = c(5, 12, 4, 2))

boxplot(
  TenenciaPct ~ Articulo,
  data = tasas_departamento,
  horizontal = TRUE,
  las = 1,
  col = "#507984",
  xlab = "Tenencia departamental (%)",
  ylab = "",
  main = "Distribución territorial del equipamiento",
  cex.axis = 0.8
)

par(margen_anterior)

# Una fila por departamento y una columna por equipo
matriz_equipos <- as.matrix(
  xtabs(
    TenenciaPct ~ Departamento + Articulo,
    data = tasas_departamento
  )
)

stopifnot(
  nrow(matriz_equipos) == 22,
  ncol(matriz_equipos) == 4,
  all(is.finite(matriz_equipos))
)

# Correlaciones entre tasas departamentales
correlaciones <- cor(matriz_equipos, method = "spearman")

print(round(correlaciones, 3))

write.csv(
  correlaciones,
  "datos/correlaciones_departamentales_R.csv"
)

# Segmentación exploratoria de los 22 departamentos
# Estandarizar: cada equipo tendrá igual peso en la distancia.
stopifnot(all(apply(matriz_equipos, 2, sd) > 0))
equipos_estandarizados <- scale(matriz_equipos)

distancias <- dist(equipos_estandarizados, method = "euclidean")
modelo_jerarquico <- hclust(distancias, method = "ward.D2")

# Comparar entre 2 y 5 grupos mediante silueta promedio
evaluacion_clusters <- data.frame(
  Grupos = 2:5,
  SiluetaPromedio = sapply(2:5, function(k) {
    grupos <- cutree(modelo_jerarquico, k = k)
    mean(cluster::silhouette(grupos, distancias)[, "sil_width"])
  })
)

print(evaluacion_clusters)

mejor_k <- evaluacion_clusters$Grupos[
  which.max(evaluacion_clusters$SiluetaPromedio)
]

grupos_departamentos <- cutree(modelo_jerarquico, k = mejor_k)

segmentacion <- data.frame(
  Departamento = rownames(matriz_equipos),
  Grupo = unname(grupos_departamentos),
  row.names = NULL
)

segmentacion <- segmentacion[
  order(segmentacion$Grupo, segmentacion$Departamento),
]

print(segmentacion)

# Perfiles: medias departamentales en porcentajes originales
tabla_equipos <- as.data.frame.matrix(matriz_equipos)

stopifnot(
  nrow(tabla_equipos) == length(grupos_departamentos)
)

perfiles_clusters <- aggregate(
  tabla_equipos,
  by = list(Grupo = unname(grupos_departamentos)),
  FUN = mean
)

print(perfiles_clusters, digits = 4)
print(table(grupos_departamentos))

write.csv(
  evaluacion_clusters,
  "datos/evaluacion_clusters_R.csv",
  row.names = FALSE
)

write.csv(
  segmentacion,
  "datos/segmentacion_departamentos_R.csv",
  row.names = FALSE
)

write.csv(
  perfiles_clusters,
  "datos/perfiles_clusters_R.csv",
  row.names = FALSE
)

plot(
  modelo_jerarquico,
  main = "Departamentos según perfil de equipamiento",
  xlab = "",
  sub = paste("Método Ward.D2 — grupos seleccionados:", mejor_k),
  cex = 0.65,
  hang = -1
)

rect.hclust(modelo_jerarquico, k = mejor_k, border = 2:6)