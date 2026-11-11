import zipfile,xml.etree.ElementTree as E,csv,collections
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def read(path,sheet=1):
 z=zipfile.ZipFile(path);ss=[]
 if 'xl/sharedStrings.xml' in z.namelist():ss=[''.join(e.itertext()) for e in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',N)]
 root=E.fromstring(z.read('xl/worksheets/sheet%d.xml'%sheet));header=None
 for row in root.findall('m:sheetData/m:row',N):
  vals={}
  for c in row:
   ref=''.join(x for x in c.attrib['r'] if x.isalpha());i=0
   for ch in ref:i=i*26+ord(ch)-64
   v=c.find('m:v',N);v=v.text if v is not None else ''.join(c.itertext());vals[i-1]=ss[int(v)] if c.get('t')=='s' else v
  if header is None:header=[vals.get(i,'') for i in range(max(vals)+1)]
  else:yield {k:vals.get(i,'') for i,k in enumerate(header)}
