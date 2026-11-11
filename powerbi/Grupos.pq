let
    Origen = Equipamiento,
    Columnas = Table.SelectColumns(Origen,{"GrupoID","Departamento","Area","Pobreza","HogaresMuestra","HogaresExpandido"}),
    Grupos = Table.Distinct(Columnas)
in
    Grupos
