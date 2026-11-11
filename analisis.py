from pathlib import Path
from collections import defaultdict,Counter
import csv,json,math,html,statistics as st
from leer_xlsx import read
B=Path(__file__).resolve().parent;D=B/'datos';G=B/'graficas';G.mkdir(exist_ok=True)
def out(name,rows,fields=None):
 rows=list(rows)
 with (D/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
rows=list(read(D/'resumen_fuente.xlsx'))
missing={c:sum(r[c]=='' for r in rows) for c in rows[0]}
num=['Seccion','ArticuloID','HogaresMuestra','HogaresExpandido','ConArticulo','UnidadesTotales','ValorMedianoQ','AntiguedadMediaAnios','TenenciaPct']
clean=[];groups={};articles={};seen=set();maxdiff=0
for raw in rows:
 r=raw.copy()
 for c in num:r[c]=float(r[c]) if r[c]!='' else None
 for c in ['Seccion','ArticuloID','HogaresMuestra']:r[c]=int(r[c])
 r['Pobreza']='Sin clasificar' if r['Pobreza']=='0' else r['Pobreza']
 r['GrupoID']=r['Departamento']+'|'+r['Area']+'|'+r['Pobreza']
 r['ArticuloClave']=f"{r['Seccion']}-{r['ArticuloID']}"
 r['EsEquipoDigital']=int(r['Seccion']==2 and r['ArticuloID'] in [1,2,3,4])
 r['TasaRecalculada']=r['ConArticulo']/r['HogaresExpandido']
 maxdiff=max(maxdiff,abs(r['TasaRecalculada']*100-r['TenenciaPct']))
 key=(r['GrupoID'],r['ArticuloClave']);assert key not in seen;seen.add(key)
 assert 0<=r['ConArticulo']<=r['HogaresExpandido'];assert r['HogaresExpandido']>0
 g={c:r[c] for c in ['GrupoID','Departamento','Area','Pobreza','HogaresMuestra','HogaresExpandido']}
 assert r['GrupoID'] not in groups or groups[r['GrupoID']]==g
 groups[r['GrupoID']]=g
 articles[r['ArticuloClave']]={c:r[c] for c in ['ArticuloClave','Articulo','EsEquipoDigital']}
 clean.append(r)
out('equipamiento_preparado.csv',clean);out('grupos_hogares.csv',groups.values());out('articulos.csv',articles.values())
out('calidad_resumen.csv',[dict(Variable=c,Ausentes=n) for c,n in missing.items()])
valid=[r for r in clean if r['Pobreza']!='Sin clasificar'];digital=[r for r in valid if r['EsEquipoDigital']]
def aggregate(keys,data):
 d=defaultdict(list)
 for r in data:d[tuple(r[k] for k in keys)].append(r)
 result=[]
 for key,rs in d.items():
  denominator=sum(r['HogaresExpandido'] for r in rs);numerator=sum(r['ConArticulo'] for r in rs)
  result.append(dict(zip(keys,key),HogaresBase=denominator,HogaresConEquipo=numerator,TenenciaPct=100*numerator/denominator,Muestra=sum(r['HogaresMuestra'] for r in rs)))
 return result
poverty=aggregate(['Articulo','Pobreza'],digital);area=aggregate(['Articulo','Area'],digital);dept=aggregate(['Articulo','Departamento'],digital)
out('resultados_pobreza.csv',poverty);out('resultados_area.csv',area);out('resultados_departamento.csv',dept)
# El microdato descargado no incluye pobreza, departamento ni factor: se usa solo para calidad y muestra.
count=0;households=set();microkeys=set();nullmicro=Counter();owned=Counter();ownedn=Counter();bad=[]
for r in read(D/'equipamiento_fuente.xlsx'):
 count+=1;households.add(r['Hogar']);k=(r['Hogar'],r['Seccion'],r['ArticuloID']);assert k not in microkeys;microkeys.add(k)
 for c,v in r.items():
  if v=='':nullmicro[c]+=1
 if r['Posee']=='No':
  for c in ['Cantidad','AntiguedadAnios','Condicion','ValorVenta']:
   if r[c]!='':bad.append((count,c))
 elif r['Posee']=='Si':
  owned[(r['Seccion'],r['ArticuloID'])]+=1
  if r['Cantidad']!='':ownedn[(r['Seccion'],r['ArticuloID'])]+=float(r['Cantidad'])
 else:bad.append((count,'Posee'))
assert count==len(households)*len(articles)
out('inconsistencias_microdato.csv',[dict(FilaMicrodato=f,Variable=c,Motivo='No posee, pero hay valor informado') for f,c in bad])
out('calidad_microdatos.csv',[dict(Variable=c,Ausentes=n) for c,n in nullmicro.items()])
out('tenencia_muestra_sin_ponderar.csv',[dict(ArticuloClave=f'{s}-{i}',Articulo=articles[f'{s}-{i}']['Articulo'],HogaresMuestra=len(households),ConEquipoMuestra=n,TasaMuestra=n/len(households)) for (s,i),n in owned.items()])
# Nulos estructurales no son falta de respuesta: cantidad/valor solo se pregunta a quienes poseen.
metrics=dict(Microdatos=count,HogaresMuestra=len(households),Articulos=len(articles),FilasResumen=len(clean),Grupos=len(groups),HogaresSinClasificacion=sum(g['HogaresMuestra'] for g in groups.values() if g['Pobreza']=='Sin clasificar'),FilasPobrezaClasificada=len(valid),MaxDiferenciaTasasPuntosPorcentuales=maxdiff)
(D/'indicadores.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
# Gráficas vectoriales con escalas comunes para porcentajes.
esc=lambda v:html.escape(str(v));fig={}
def bars(name,title,labels,values):
 h=100+len(labels)*34
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 {h}"><rect width="950" height="{h}" fill="white"/><g font-family="Arial" fill="#183647"><text x="20" y="30" font-size="19" font-weight="bold">{esc(title)}</text><text x="20" y="53" font-size="12">Porcentaje de hogares · estimación a partir del resumen ponderado ENCOVI 2023 / OES</text>'
 for i,(label,v) in enumerate(zip(labels,values)):
  y=75+34*i;s+=f'<text x="325" y="{y+17}" text-anchor="end" font-size="12">{esc(label)}</text><rect x="340" y="{y}" width="{v*5:.3f}" height="23" rx="2" fill="#227d9a"/><text x="{350+v*5}" y="{y+17}" font-size="12">{v:.2f}%</text>'
 s+='</g></svg>';fig[name]=s;(G/(name+'.svg')).write_text(s)
order={'Pobre extremo':0,'Pobre no extremo':1,'No pobre':2}
for article in ['Computadora laptop','Computadora de escritorio','Tablet','Impresora']:
 p=sorted([r for r in poverty if r['Articulo']==article],key=lambda r:order[r['Pobreza']]);bars(article.replace(' ','_'),article+' según pobreza',[r['Pobreza'] for r in p],[r['TenenciaPct'] for r in p])
a=sorted([r for r in area if r['Articulo']=='Computadora laptop'],key=lambda r:r['Area']);bars('laptop_area','Laptop: diferencia urbana y rural',[r['Area'] for r in a],[r['TenenciaPct'] for r in a])
d=sorted([r for r in dept if r['Articulo']=='Computadora laptop'],key=lambda r:r['TenenciaPct'],reverse=True);bars('laptop_departamento','Tenencia de laptop por departamento',[r['Departamento'] for r in d],[r['TenenciaPct'] for r in d])
lookup={(r['Articulo'],r['Pobreza']):r['TenenciaPct'] for r in poverty}
laptop_gap=lookup['Computadora laptop','No pobre']-lookup['Computadora laptop','Pobre extremo']
fmt=lambda v:f'{v:,.2f}' if isinstance(v,float) else str(v)
def table(rs):
 cols=list(rs[0]);return '<div class="table"><table><tr>'+''.join('<th>'+esc(c)+'</th>' for c in cols)+'</tr>'+''.join('<tr>'+''.join('<td>'+esc(fmt(r[c]))+'</td>' for c in cols)+'</tr>' for r in rs)+'</table></div>'
body=f'''<header><p>INGENIERÍA EN INFORMÁTICA Y SISTEMAS</p><h1>Brecha de equipamiento digital<br>y pobreza en Guatemala</h1><p>Análisis exploratorio de ENCOVI 2023 · hogares, territorio y acceso a equipos</p></header>
<section><h2>Objetivo y pregunta</h2><p>¿Cómo varía la tenencia de computadoras, laptops, tablets e impresoras según la condición de pobreza y el área de residencia de los hogares guatemaltecos? El análisis busca orientar propuestas de ingeniería para ampliar el acceso a herramientas digitales.</p><p>Se usa una publicación derivada de ENCOVI 2023 del INE, distribuida por OES DataLab / Guate en Datos. Se descargaron dos archivos: microdatos de equipamiento y un resumen ponderado por departamento, área, pobreza y artículo. La guía del INE respalda la estructura de hogares, los factores y la existencia de hogares sin clasificación. No se obtuvo la base original completa del INE desde su portal, que bloqueó la descarga automática; se conservan las copias OES sin modificarlas y se identifica esta procedencia.</p></section>
<section><h2>A. Exploración inicial</h2><p>El microdato tiene <b>{count:,} filas</b>: {len(households):,} hogares por 50 artículos. Las filas son pares hogar–artículo, no 548,200 hogares independientes. El resumen tiene {len(clean):,} filas y 13 columnas de origen, distribuidas en {len(groups)} grupos. Incluye computadoras, tablets, impresoras y otros bienes del hogar.</p><p>El archivo micro no contiene pobreza, ubicación ni factor de expansión. Por eso no se le asignan esas variables inventando un cruce: sus resultados de calidad se analizan aparte. Las comparaciones sobre pobreza se calculan desde el resumen ya ponderado. Una fila del resumen es un grupo territorial y socioeconómico para un artículo.</p></section>
<section><h2>B. Limpieza y validación</h2><p>Se verificaron claves únicas en ambos archivos, 50 artículos por hogar y denominadores consistentes en el resumen. La categoría de pobreza 0 se recodificó como “Sin clasificar”; corresponde a {metrics['HogaresSinClasificacion']} hogares de la muestra. No se confunde con no pobre. Se mantiene en la base y se excluye explícitamente de los cruces por pobreza.</p><p>En el microdato, Cantidad, AntiguedadAnios, Condicion y ValorVenta están vacíos para quienes no poseen el artículo. Son ausencias estructurales, no deben rellenarse con un promedio ni provocar la eliminación del hogar. Los textos originales se conservan.</p><p>Se detectó una contradicción en el microdato: hogar 378, sección 3, artículo 3, declara no poseer plancha eléctrica pero informa cantidad 1. Se conserva en el archivo fuente, se registra en inconsistencias_microdato.csv y no se usa esa cantidad en los conteos de unidades de poseedores. No afecta el resumen de laptops, tablets e impresoras. La coherencia no se presupone: se comprueba.</p><p>En el resumen hay {missing['ValorMedianoQ']:,} valores ausentes de valor mediano y {missing['AntiguedadMediaAnios']:,} de antigüedad. No se rellenan para calcular tenencia, que usa otras columnas. Se recalcula la tasa como ConArticulo / HogaresExpandido. La diferencia máxima frente a la tasa publicada es {maxdiff:.5f} puntos porcentuales, compatible con redondeos.</p>{table([dict(Variable=c,Ausentes=n) for c,n in missing.items()])}</section>
<section><h2>C. Análisis descriptivo</h2><p>Las tasas se calculan sumando hogares expandidos con un equipo y dividiendo entre hogares expandidos del mismo conjunto de celdas, siempre para un solo artículo. No se promedian porcentajes departamentales sin ponderar y no se suman denominadores repetidos entre equipos para reportar hogares únicos.</p>{fig['Computadora_laptop']}{fig['Computadora_de_escritorio']}{fig['Tablet']}{fig['Impresora']}{fig['laptop_area']}</section>
<section><h2>D. Diagnóstico y hallazgos</h2><p>La tenencia estimada de laptop es {lookup['Computadora laptop','Pobre extremo']:.2f}% en hogares pobres extremos, {lookup['Computadora laptop','Pobre no extremo']:.2f}% en pobres no extremos y {lookup['Computadora laptop','No pobre']:.2f}% en no pobres. La diferencia entre no pobres y pobres extremos es <b>{laptop_gap:.2f} puntos porcentuales</b>.</p>{fig['laptop_departamento']}<p>Esta asociación describe desigualdad en equipamiento. No demuestra que comprar una computadora elimine pobreza, ni que todos los hogares sin computadora carezcan de internet. Tampoco mide habilidades digitales, velocidad de conexión o disponibilidad de dispositivos dentro de escuelas.</p><p>Los cruces por departamento se presentan de forma exploratoria. Las celdas pequeñas pueden ser imprecisas; el archivo de resumen no permite reconstruir intervalos que incorporen el diseño muestral completo. Un ranking no demuestra diferencias estadísticamente significativas entre departamentos.</p></section>
<section><h2>E. Aplicación para ingeniería y conclusión</h2><p>Para estudiantes de ingeniería, el proyecto relaciona datos con decisiones de diseño: aplicaciones educativas ligeras, materiales descargables, funcionamiento sin conexión y laboratorios compartidos. Los resultados sirven para identificar grupos que conviene estudiar con mayor detalle antes de implementar una solución.</p><p>Una propuesta concreta es un laboratorio universitario o comunitario con préstamo de equipos y recursos educativos locales. Su necesidad, ubicación y presupuesto deben validarse con información de infraestructura, demanda y acceso real; la encuesta no sustituye ese diagnóstico.</p><p>La conclusión es que el acceso a equipos digitales se distribuye de manera desigual según pobreza y territorio en los datos de 2023. La ingeniería puede contribuir diseñando herramientas y servicios ajustados a esas condiciones. La propuesta debe evitar asumir que todos los usuarios poseen laptop, conexión permanente o los mismos recursos.</p><p>Limitaciones: información de 2023, copias procesadas por OES, conteos expandidos redondeados y ausencia de vínculo individual entre los dos archivos descargados. No se agregan tasas de distintas fuentes o años como si describieran los mismos hogares. No se calculan cifras de internet a partir de tener computadora.</p></section>
<section><h2>Fuentes y reproducción</h2><ul><li><a href="https://www.ine.gob.gt/pobreza-menu/">INE: ENCOVI</a></li><li><a href="https://www.ine.gob.gt/wp-content/uploads/2024/11/Guia-para-el-uso-de-bases-de-datos_v_final.pdf">INE: guía de bases ENCOVI 2023</a></li><li><a href="https://guateendatos.org.gt/oes-datalab/">OES DataLab: archivos descargados de equipamiento y resumen</a></li></ul><p>Ejecutar python analisis.py con Python 3.10 o superior, sin librerías adicionales. Los Excel fuente se mantienen en datos/. El script genera CSV, gráficas SVG, controles e informe. Las consultas y medidas de Power BI se entregan preparadas, pendientes de ejecución en Power BI Desktop.</p></section>'''
css='body{margin:0;background:#edf3f6;color:#203b4a;font:16px/1.65 Arial}main{max-width:1080px;margin:auto;background:white;padding:48px}h1{font-size:37px;line-height:1.2}header{border-bottom:5px solid #227d9a;padding-bottom:20px}h2{color:#227d9a;margin-top:40px}svg{width:100%;height:auto;margin:18px 0;border:1px solid #e5edf0}.table{overflow:auto}table{border-collapse:collapse;width:100%;font-size:13px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}th{background:#e5f1f6}@media print{main{padding:0}svg,table{break-inside:avoid}}'
(B/'Informe_Brecha_Digital.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>Brecha digital y pobreza en Guatemala</title><style>'+css+'</style><main>'+body+'</main></html>',encoding='utf-8')
(B/'VERIFICACION.txt').write_text('Claves, rangos, denominadores y cobertura de artículos verificados.\n'+json.dumps(metrics,ensure_ascii=False,indent=2)+'\nNo se ejecutó Power BI Desktop.\n')
print(json.dumps(metrics,ensure_ascii=False));print(poverty)
