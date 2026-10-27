"""Create a separate, provisional main-melody arrangement for trombone.

Source: flute line in the supplied screenshots, lowered two octaves.
Unpitched vocal sections use a lower-octave Trombone 1 fill, explicitly marked.
Run with PYTHONPATH=/workspace/.sheetmusic-tools python build_melody.py.
"""
from pathlib import Path
from io import BytesIO
import json
from music21 import stream, note, meter, key, clef, metadata, expressions, dynamics, instrument, spanner, bar, tie, pitch
import verovio
import cairosvg
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
source={}

def setbar(i, pitches, lengths):
    assert len(pitches.split())==len(lengths), i
    source[i]=list(zip(pitches.split(), lengths))

def repeat(target, original): source[target]=list(source[original])
def whole(i,p): setbar(i,p,[4])
def rest(i): whole(i,'r')
def eight(i,p): setbar(i,p,[.5]*8)

setbar(1,'r',[1])
setbar(2,'E-5 G5 B-5 G5 D5',[1,1,.5,1,.5])
setbar(3,'D5 G5 B-5 C6 D6 C6 B-5',[.5,.5,.5,.5,1,.5,.5])
setbar(4,'F5 B-5 D6 B-5 F5',[1,1,.5,1,.5])
setbar(5,'F5 B-5 C6 B-5 G5',[.5,1.5,1,.5,.5])
setbar(6,'E-6 D6 C6 B-5 F5',[1,1,.5,1,.5])
setbar(7,'F5 B-5 C6 C6 B-5 G5',[.5,1.5,.5,.5,.5,.5])
setbar(8,'F6 F6 F6 G6 F6 E-6',[1,1,.5,.5,.5,.5])
whole(9,'F6')
eight(10,'B4 F5 B-5 F5 B4 F5 B-5 F5')
eight(11,'D5 G5 B-5 G5 D5 G5 B-5 G5')
eight(12,'G5 B-5 D6 B-5 G5 B-5 D6 B-5')
eight(13,'D5 G5 B-5 G5 D5 F5 D5 D5')
repeat(14,12); repeat(15,11); repeat(16,12)
setbar(17,'C6 C6 C6 C6',[1]*4)
setbar(18,'D6 C6 A5 C6 A5',[1,1,.5,1,.5])
setbar(19,'A5 A5 G6 F6 E-6 D6',[.5,1.5,.5,.5,.5,.5])
setbar(20,'C6 B-5 G5 B-5 F5',[1,1,.5,1,.5])
setbar(21,'F5 F5 F5',[3,.5,.5])
repeat(22,20); repeat(23,19)
setbar(24,'C6 B-5 A5 B-5 C6',[1,1,1,.5,.5])
whole(25,'D6')
setbar(26,'G5 F5 F5 F5',[1,1.5,1,.5])
setbar(27,'F5 F5 F5 F5 F5',[.5,1,1,.5,1])
repeat(28,26); repeat(29,27); repeat(30,26); repeat(31,27)
setbar(32,'r F5 F5 F5 G5 B-5',[1,.5,.5,.5,.5,1])
whole(33,'B-5')
setbar(34,'F5 F5 E-5 D5 D5 C5',[.5,.5,1,.5,.5,1])
setbar(35,'C5 C5 C5 C5 D5 C5 C5',[.5,.5,.5,.5,.5,.5,1])
whole(36,'C5'); rest(37); repeat(38,34); repeat(39,35)
whole(40,'B-5'); setbar(41,'B-5 r',[2,2])
setbar(42,'C6 r C6 r r C6 r C6',[.5,.5,.5,.5,.5,.5,.5,.5])
setbar(43,'r C6 r C6 C6 C6 C6 C6',[.5,.5,.5,.5,.5,.5,.5,.5])
repeat(44,42); repeat(45,43); repeat(46,42); repeat(47,43)
setbar(48,'C6 r C6 r C6 r C6 r',[.5]*8)
setbar(49,'B-5 B-5 B-5 B-5',[1.5,1.5,.5,.5])
repeat(50,20); repeat(51,19); repeat(52,20); repeat(53,21)
repeat(54,20); repeat(55,19); repeat(56,24); repeat(57,25)
repeat(58,26); repeat(59,27); repeat(60,26); repeat(61,27)
repeat(62,26); repeat(63,27); repeat(64,32); repeat(65,33)
repeat(66,34); repeat(67,35); whole(68,'C5'); rest(69)
repeat(70,34); repeat(71,35); whole(72,'C5')
setbar(73,'C5 r',[2,2]); rest(74); rest(75)
# Flute notes in these bars are spoken, unpitched cues. Use a marked brass fill.
fills=[76,77,80,81,84,85]
tbn=json.loads((ROOT/'transcription.json').read_text())
for i in fills:
    source[i]=[(pitch.Pitch(p).transpose(12).nameWithOctave if p!='r' else p,d) for p,d in tbn[str(i)]]
rest(78); rest(79); rest(82); rest(83); rest(86); rest(87)
setbar(88,'G5 A5',[2,2]); setbar(89,'B-5 C6',[2,2]); rest(90); rest(91)
setbar(92,'F6 E-6 E-6 D6',[1,1.5,1,.5])
setbar(93,'D6 E-6 D6 E-6 D6',[.5,1,.5,1,1])
repeat(94,92); repeat(95,93); repeat(96,32); repeat(97,33)
repeat(98,34); repeat(99,35); whole(100,'C5'); rest(101)
repeat(102,34); repeat(103,35); whole(104,'G5'); whole(105,'G5')
setbar(106,'B-5 B-5 B-5 G5 F5',[1,1,.5,1,.5])
setbar(107,'F5 E-5 E-5 E-5 F5 G5',[.5,1,1,.5,.5,.5])
setbar(108,'A5 A5 B-5 A5 G5 A5',[1,1,.5,.5,.5,.5])
whole(109,'G5'); repeat(110,106); repeat(111,107); repeat(112,108)
setbar(113,'G5 G5 G5 G5 G5',[2,.5,.5,.5,.5])

assert set(source)==set(range(1,114))
score=stream.Score()
score.metadata=metadata.Metadata()
score.metadata.title='Cicada — Melody for Trombone (draft)'
score.metadata.movementName=score.metadata.title
score.metadata.composer='GoodKid'
score.metadata.add('arranger','Blake Nellis; trombone adaptation from screenshots')
part=stream.Part(id='TromboneMelody')
part.partName='Trombone melody'; part.partAbbreviation='Tbn.'
part.insert(0,instrument.Trombone())
measures={}
transposed={}
for i in range(1,114):
    events=source[i]
    assert abs(sum(d for _,d in events)-(1 if i==1 else 4))<1e-6, (i,events)
    m=stream.Measure(number=i)
    if i==1:
        m.insert(0,clef.BassClef()); m.insert(0,key.KeySignature(-2)); m.insert(0,meter.TimeSignature('4/4'))
        m.insert(0,expressions.TextExpression('DRAFT — screenshot transcription; verify against source'))
    if i==2:
        m.insert(0,expressions.TextExpression('Quarter note = 176; flute line down two octaves'))
    if i in [76,80,84]: m.insert(0,expressions.TextExpression('Tbn. 1 fill (under vocal cue)'))
    if i in [2,18,26,42,50,58,74,88,90,92,106,113]:
        dyn={2:'f',18:'f',26:'f',42:'mf',50:'f',58:'f',74:'mf',88:'mp',90:'f',92:'ff',106:'f',113:'ff'}[i]
        m.insert(0,dynamics.Dynamic(dyn))
    converted=[]
    for p,d in events:
        n=note.Rest(quarterLength=d) if p=='r' else note.Note(p,quarterLength=d).transpose(-24)
        m.append(n)
        converted.append((n.nameWithOctave if n.isNote else 'r',d))
    transposed[i]=converted
    if i==1: m.padAsAnacrusis()
    part.append(m); measures[i]=m

# Ties only where the same pitch visibly carries into the following bar.
for a,b in [(2,3),(4,5),(6,7),(18,19),(20,21),(22,23),(26,27),(28,29),(30,31),(32,33),(35,36),(39,40),(40,41),(50,51),(52,53),(54,55),(58,59),(60,61),(62,63),(64,65),(67,68),(71,72),(72,73),(76,77),(80,81),(84,85),(92,93),(94,95),(96,97),(99,100),(103,104),(104,105),(106,107),(108,109),(110,111),(112,113)]:
    an=measures[a].notes[-1]; bn=measures[b].notes[0]
    if an.pitch==bn.pitch:
        an.tie=tie.Tie('continue' if an.tie and an.tie.type=='stop' else 'start')
        bn.tie=tie.Tie('stop')

run=[]
for i in range(1,115):
    if source.get(i)==[('r',4)]: run.append(i)
    else:
        if len(run)>1: part.insert(0,spanner.MultiMeasureRest(*(measures[n].notesAndRests[0] for n in run)))
        run=[]
measures[113].rightBarline=bar.Barline('final')
score.append(part)
xml=OUT/'Cicada-Trombone-Melody-draft.musicxml'
score.write('musicxml',fp=xml)
(ROOT/'melody-transcription.json').write_text(json.dumps({'source':'Flute concert pitch; Tbn. 1 fills under unpitched vocal cues','transpose_semitones':-24,'source_measures':source,'trombone_measures':transposed},indent=2))
tk=verovio.toolkit()
tk.setOptions({'pageWidth':2100,'pageHeight':2970,'scale':40,'adjustPageHeight':False,'breaks':'auto','header':'auto','footer':'auto','mnumInterval':5,'spacingSystem':15})
assert tk.loadFile(str(xml))
writer=PdfWriter()
for i in range(1,tk.getPageCount()+1):
    svg=tk.renderToSVG(i)
    (OUT/f'Cicada-Trombone-Melody-page-{i}.svg').write_text(svg)
    writer.add_page(PdfReader(BytesIO(cairosvg.svg2pdf(bytestring=svg.encode()))).pages[0])
with (OUT/'Cicada-Trombone-Melody-draft.pdf').open('wb') as f: writer.write(f)
pitches=[n.pitch.midi for n in part.recurse().notes]
print(f'Melody: {len(measures)} measures, {tk.getPageCount()} pages; range {pitch.Pitch(min(pitches))}–{pitch.Pitch(max(pitches))}.')
