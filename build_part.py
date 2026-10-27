"""Build the provisional Trombone 1 transcription from supplied score pages 1–12.

Run: PYTHONPATH=/workspace/.sheetmusic-tools python build_part.py
"""
from pathlib import Path
from io import BytesIO
import json
import xml.etree.ElementTree as ET
from music21 import stream, note, meter, key, clef, metadata, tempo, dynamics, expressions, articulations, tie, layout, instrument, spanner, bar
import verovio
import cairosvg
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
score = stream.Score()
score.metadata = metadata.Metadata()
score.metadata.title = 'Cicada — Trombone 1'
score.metadata.composer = 'GoodKid'
score.metadata.add('arranger', 'Blake Nellis')
score.metadata.movementName = 'Cicada — Trombone 1 (draft)'
part = stream.Part(id='Trombone1')
part.partName = 'Trombone 1'
part.partAbbreviation = 'Tbn. 1'
part.insert(0, instrument.Trombone())

def whole(p): return [(p, 4)]
def halves(p): return [(p, 2), (p, 2)]
def quarters(p): return [(p, 1)] * 4
def hits(p): return [(p, 1.5), ('r', .5), (p, 1.5), ('r', .5)]

# Measure numbering follows the full score, including its opening pickup.
data = {i: [('r', 4)] for i in range(1, 114)}
data[1] = [('C3', 1/3), ('D3', 1/3), ('E-3', 1/3)]
data[2] = [('F3', .5), ('D4', .5), ('E-4', 3)]
for i,p in {4:'B-3',5:'C4',6:'E-4',8:'B-3',9:'C4',19:'B-3',20:'C4',21:'E-4',23:'B-3',24:'C4',26:'B-3',27:'C4',28:'D4',29:'E-4',30:'B-3',31:'C4',32:'C4',33:'D4',36:'E-4',37:'E-4',40:'E-4',51:'B-3',52:'C4',53:'E-4',55:'B-3',56:'C4',58:'B-3',59:'C4',60:'D4',61:'E-4',62:'B-3',63:'C4',64:'C4',65:'D4',68:'E-4',69:'E-4',72:'E-4',74:'E-4',75:'E-4',78:'D4',79:'D4',82:'E-4',83:'E-4'}.items(): data[i]=whole(p)
for i in [3,7,18,22,50,54]: data[i]=halves('D4')
for i in [25,57]: data[i]=[('E-4',2),('E-4',.5),('E-4',.5),('E-4',.5),('E-4',.5)]
for i in [34,38,66,70]: data[i]=hits('C4')
for i in [35,39,67,71]: data[i]=quarters('B-3')
for i in [41,73]: data[i]=[('E-4',2),('r',2)]
for i in [76,80,84]: data[i]=[('G4',1),('G4',1.5),('G4',1),('G4',.5)]
for i in [77,81,85]: data[i]=[('G4',.5),('F4',1),('F4',1.5),('F4',1)]
data[78]=data[79]=whole('E-4')
for i,p in {86:'E-4',87:'E-4',92:'B-3',93:'D4',94:'E-4',95:'D4',96:'B-3',97:'D4',104:'E-4',105:'E-4',106:'E-4',107:'E-4',110:'E-4',111:'E-4'}.items(): data[i]=whole(p)
data[88]=halves('G3')
data[95]=whole('E-4')
data[89]=halves('B-3')
for i in [98,102]: data[i]=hits('E-4')
for i in [99,103]: data[i]=quarters('D4')
data[100]=[('E-4',.5),('E-4',.5),('D4',1),('C4',.5),('C4',.5),('B-3',1)]
data[101]=[('B-3',.5)]*4+[('C4',.5),('B-3',.5),('B-3',1)]
for i in [108,112]: data[i]=[('G4',1),('G4',1.5),('G4',1),('G4',.5)]
data[109]=[('G4',.5),('F4',1),('F4',1.5),('F4',1)]
data[113]=[('G4',2)]+[('G4',.5)]*4

dynamic_marks={1:'ff',2:'f',9:'fp',18:'mf',25:'fp',26:'f',50:'mf',57:'fp',58:'f',74:'mf',90:'f',92:'ff',106:'f'}
measures={}
for i, events in data.items():
    m=stream.Measure(number=i)
    if i==1:
        m.insert(0,clef.BassClef()); m.insert(0,key.KeySignature(-2)); m.insert(0,meter.TimeSignature('4/4'))
        m.insert(0, expressions.TextExpression('DRAFT — opening m. 1–2 needs source verification'))
    if i==2:
        mark=tempo.MetronomeMark(number=176)
        mark.style.hideObjectOnPrint=True
        m.insert(0,mark)
        m.insert(0,expressions.TextExpression('Quarter note = 176'))
    if i in dynamic_marks: m.insert(0,dynamics.Dynamic(dynamic_marks[i]))
    for p,d in events:
        n=note.Rest(quarterLength=d) if p=='r' else note.Note(p,quarterLength=d)
        if i==1: n.style.color='#b03030'
        if i in [34,35,38,39,66,67,70,71,98,99,102,103] and p!='r': n.articulations.append(articulations.Accent())
        if i in [25,57] and m.duration.quarterLength>=2: n.articulations.append(articulations.Accent())
        if i==113: n.articulations.append(articulations.StrongAccent() if m.duration.quarterLength>=2 else articulations.Accent())
        m.append(n)
    if i==1: m.padAsAnacrusis()
    part.append(m); measures[i]=m

for a,b in [(36,37),(40,41),(68,69),(72,73),(74,75),(78,79),(82,83),(86,87),(94,95),(104,105),(106,107),(110,111)]:
    measures[a].notes[-1].tie=tie.Tie('start'); measures[b].notes[0].tie=tie.Tie('stop')
for a,b in [(76,77),(80,81),(84,85),(108,109),(112,113)]:
    measures[a].notes[-1].tie=tie.Tie('start'); measures[b].notes[0].tie=tie.Tie('stop')
for i in [9,25,57]:
    part.insert(0,dynamics.Crescendo(measures[i].notes[0],measures[i].notes[-1]))
part.insert(0,dynamics.Crescendo(measures[88].notes[0],measures[89].notes[-1]))
part.insert(0,dynamics.Crescendo(measures[113].notes[1],measures[113].notes[-1]))
measures[113].insert(3.9,dynamics.Dynamic('ff'))
measures[113].rightBarline=bar.Barline('final')
score.append(part)
for i,m in measures.items():
    assert abs(float(m.duration.quarterLength)-(1 if i==1 else 4))<1e-6, (i,m.duration)
xml_path=OUT/'Cicada-Trombone-1-draft.musicxml'
score.write('musicxml',fp=xml_path)
# Keep measure numbers visible, including stretches of rests.
tree=ET.parse(xml_path)
for measure in tree.findall('.//part/measure'):
    pr=measure.find('print')
    if pr is None: pr=ET.SubElement(measure,'print')
    ET.SubElement(pr,'measure-numbering').text='measure'
tree.write(xml_path,encoding='utf-8',xml_declaration=True)
tk=verovio.toolkit()
tk.setOptions({'pageWidth':2100,'pageHeight':2970,'scale':40,'adjustPageHeight':False,'breaks':'auto','header':'auto','footer':'auto','mnumInterval':1,'spacingSystem':14})
assert tk.loadFile(str(xml_path))
writer=PdfWriter()
for page in range(1,tk.getPageCount()+1):
    svg=tk.renderToSVG(page)
    (OUT/f'Cicada-Trombone-1-page-{page}.svg').write_text(svg)
    pdf=cairosvg.svg2pdf(bytestring=svg.encode())
    writer.add_page(PdfReader(BytesIO(pdf)).pages[0])
with (OUT/'Cicada-Trombone-1-draft.pdf').open('wb') as f: writer.write(f)
(ROOT/'transcription.json').write_text(json.dumps({str(k):v for k,v in data.items()},indent=2))
print(f'Built {len(data)} measures, {tk.getPageCount()} PDF pages; one Trombone 1 part only.')
