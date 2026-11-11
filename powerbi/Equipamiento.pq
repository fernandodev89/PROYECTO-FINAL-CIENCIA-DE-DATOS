let
    Ruta = "C:\Proyecto_Brecha_Digital_Guatemala\datos\resumen_fuente.xlsx",
    Libro = Excel.Workbook(File.Contents(Ruta), null, true),
    Datos = Libro{[Item="Datos",Kind="Sheet"]}[Data],
    Encabezados = Table.PromoteHeaders(Datos, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {
        {"Departamento",type text},{"Area",type text},{"Pobreza",type text},
        {"Seccion",Int64.Type},{"ArticuloID",Int64.Type},{"Articulo",type text},
        {"HogaresMuestra",Int64.Type},{"HogaresExpandido",type number},
        {"ConArticulo",type number},{"UnidadesTotales",type number},
        {"ValorMedianoQ",type number},{"AntiguedadMediaAnios",type number},{"TenenciaPct",type number}
    }, "en-US"),
    Pobreza = Table.ReplaceValue(Tipos,"0","Sin clasificar",Replacer.ReplaceValue,{"Pobreza"}),
    Grupo = Table.AddColumn(Pobreza,"GrupoID", each [Departamento]&"|"&[Area]&"|"&[Pobreza],type text),
    ArticuloClave = Table.AddColumn(Grupo,"ArticuloClave", each Text.From([Seccion])&"-"&Text.From([ArticuloID]),type text),
    Digital = Table.AddColumn(ArticuloClave,"EsEquipoDigital",each if [Seccion]=2 and List.Contains({1,2,3,4},[ArticuloID]) then 1 else 0,Int64.Type),
    Tasa = Table.AddColumn(Digital,"TasaRecalculada",each if [HogaresExpandido]>0 then [ConArticulo]/[HogaresExpandido] else null,type number)
in
    Tasa
