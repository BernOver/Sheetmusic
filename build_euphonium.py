"""Arrange the extracted Premier Inn upper melody for concert-pitch euphonium.

Run with PYTHONPATH=/workspace/.sheetmusic-tools python build_euphonium.py.
The checked-in extraction JSON permits regeneration without the private PDF.
"""
from pathlib import Path
from io import BytesIO
import json
from music21 import stream, note, clef, key, meter, instrument, metadata, expressions, dynamics, tie, spanner, bar, pitch
import verovio
import cairosvg
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
OUT.mkdir(exist_ok=True)
data=json.loads((ROOT/'premier-extraction.json').read_text())
score=stream.Score()
score.metadata=metadata.Metadata()
score.metadata.title='Premier Inn — Euphonium'
score.metadata.movementName=score.metadata.title
score.metadata.composer='Good Kid'
score.metadata.add('arranger','Piano arrangement: Yoyo1235; euphonium melody adaptation')
part=stream.Part(id='EuphoniumMelody')
part.partName='Euphonium'; part.partAbbreviation='Euph.'
part.insert(0,instrument.Instrument(instrumentName='Euphonium'))
measures={}
output_data=[]
flat_names=['C','D-','D','E-','E','F','G-','G','A-','A','B-','B']
dyns={1:'ff',4:'f',36:'ff',54:'f',62:'f',86:'ff',102:'f',116:'f',118:'ff',126:'ff',150:'mf'}
for record in data:
    number=record['measure']
    m=stream.Measure(number=number)
    if number==1:
        m.insert(0,clef.BassClef()); m.insert(0,key.KeySignature(-5)); m.insert(0,meter.TimeSignature('4/4'))
        m.insert(0,expressions.TextExpression('Good Kid • melody from piano arrangement by Yoyo1235'))
    if number==2:
        m.insert(0,expressions.TextExpression('Quarter note = 180'))
    if number==4:
        m.insert(0,expressions.TextExpression('Concert pitch • upper melody down one octave'))
    if number in dyns: m.insert(0,dynamics.Dynamic(dyns[number]))
    row={'measure':number,'events':[]}
    for e in record['events']:
        if e['pitch']=='r': n=note.Rest(quarterLength=e['duration'])
        else:
            midi=pitch.Pitch(e['pitch']).midi-12
            n=note.Note(flat_names[midi%12]+str(midi//12-1),quarterLength=e['duration'] or .5)
            if e['duration']==0: n=n.getGrace()
            if e.get('tie_in') or e.get('tie_out'):
                n.tie=tie.Tie('continue' if e.get('tie_in') and e.get('tie_out') else 'stop' if e.get('tie_in') else 'start')
        m.append(n)
        row['events'].append({'pitch':n.nameWithOctave if n.isNote else 'r','duration':e['duration'],'tie':n.tie.type if n.tie else None})
    assert abs(float(m.duration.quarterLength)-(1 if number==1 else 4))<1e-8, number
    if number==1: m.padAsAnacrusis()
    part.append(m); measures[number]=m
    output_data.append(row)
run=[]
for number in range(1,len(data)+2):
    m=measures.get(number)
    if m is not None and len(m.notesAndRests)==1 and m.notesAndRests[0].isRest and m.duration.quarterLength==4: run.append(number)
    else:
        if len(run)>1:
            grouped=spanner.MultiMeasureRest(*(measures[i].notesAndRests[0] for i in run))
            grouped.useSymbols=False
            part.insert(0,grouped)
        run=[]
measures[len(data)].rightBarline=bar.Barline('final')
score.append(part)
xml=OUT/'Premier-Inn-Euphonium-Melody.musicxml'
score.write('musicxml',fp=xml)
(ROOT/'euphonium-transcription.json').write_text(json.dumps({'title':'Premier Inn','concert_key':'D-flat major (enharmonic C-sharp major)','source':'Upper melody in supplied piano PDF','transpose_semitones':-12,'measures':output_data},indent=2))
tk=verovio.toolkit()
tk.setOptions({'pageWidth':2100,'pageHeight':2970,'scale':40,'adjustPageHeight':False,'breaks':'auto','header':'auto','footer':'auto','mnumInterval':5,'spacingSystem':15})
assert tk.loadFile(str(xml))
writer=PdfWriter()
for number in range(1,tk.getPageCount()+1):
    svg=tk.renderToSVG(number)
    (OUT/f'Premier-Inn-Euphonium-Melody-page-{number}.svg').write_text(svg)
    writer.add_page(PdfReader(BytesIO(cairosvg.svg2pdf(bytestring=svg.encode()))).pages[0])
with (OUT/'Premier-Inn-Euphonium-Melody.pdf').open('wb') as f: writer.write(f)
notes=list(part.recurse().notes)
print(f'Built {len(data)} measures, {tk.getPageCount()} pages; {len(notes)} melody notes.')
print('Range:',min(n.pitch for n in notes).nameWithOctave,'to',max(n.pitch for n in notes).nameWithOctave)
print('Tied notes:',sum(bool(n.tie) for n in notes))
