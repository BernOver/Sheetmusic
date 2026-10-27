"""Extract the upper piano line from the user-supplied vector PDF.

Reads actual SMuFL noteheads, flags, stems, beams and staff coordinates rather
than performing image OCR. The source PDF is kept local and is not published.
"""
from pathlib import Path
from collections import defaultdict
import json
import fitz

ROOT=Path(__file__).resolve().parent
PDF=ROOT/'sources/premier-inn-good-kid.pdf'
HEADS={'\ue0a4':1,'\ue0a3':2,'\ue0a2':4}
RESTS={'\ue4e3':4,'\ue4e4':2,'\ue4e5':1,'\ue4e6':.5}
FLAGS={'\ue240','\ue241'}

def glyphs(page):
    return [{'c':c['c'],'x':c['origin'][0],'y':c['origin'][1],'size':s['size']}
            for b in page.get_text('rawdict')['blocks'] if 'lines' in b
            for l in b['lines'] for s in l['spans'] for c in s['chars']]

def lines(drawings):
    return [(it[1],it[2],d) for d in drawings for it in d['items'] if it[0]=='l']

def staves(drawings):
    ys=defaultdict(float)
    for a,b,d in lines(drawings):
        if abs(a.y-b.y)<.02 and abs(a.x-b.x)>30 and .4<(d['width'] or 0)<.7:
            ys[round(a.y,2)]+=abs(a.x-b.x)
    candidates=sorted(y for y,w in ys.items() if w>200)
    groups=[]
    for y in candidates:
        if any(abs(y-g[0])<21 for g in groups): continue
        group=[next((a for a in candidates if abs(a-(y+i*4.96))<.04),None) for i in range(5)]
        if all(a is not None for a in group): groups.append(group)
    assert len(groups)%2==0
    return groups

def extract():
    output=[]; measure_number=1
    for pn,page in enumerate(fitz.open(PDF),1):
        chars=glyphs(page); drawings=page.get_drawings(); ls=lines(drawings)
        groups=staves(drawings)
        for si in range(0,len(groups),2):
            upper,lower=groups[si:si+2]
            cutoff=(upper[-1]+lower[0])/2
            cs=[c for c in chars if upper[0]-16<c['y']<cutoff]
            verticals=[]
            for a,b,d in ls:
                if 30<a.x<580 and abs(a.x-b.x)<.02 and min(a.y,b.y)<upper[0]+.5 and max(a.y,b.y)>lower[0]-.5:
                    verticals.append(a.x)
            bounds=[]
            for x in sorted(verticals):
                if not bounds or x-bounds[-1]>2: bounds.append(x)
            assert len(bounds)>1,(pn,si,bounds)
            # Initial left barline sits before the clef/key; every subsequent
            # barline is a genuine measure boundary.
            for bi,(left,right) in enumerate(zip(bounds,bounds[1:])):
                if right-left<5: continue # final double barline
                mc=[c for c in cs if left+.6<c['x']<right-.6]
                clefs=sorted((c for c in cs if c['c'] in ['\ue050','\ue062'] and c['x']<right),key=lambda c:c['x'])
                first_clef=next((c for c in cs if c['c'] in ['\ue050','\ue062']),None)
                clef=clefs[-1]['c'] if clefs else first_clef['c']
                clef_changes=[c for c in mc if c['c'] in ['\ue050','\ue062']]
                heads=[c for c in mc if c['c'] in HEADS]
                clusters=[]
                for h in sorted(heads,key=lambda c:(c['x'],c['y'])):
                    if clusters and abs(clusters[-1][0]['x']-h['x'])<.6: clusters[-1].append(h)
                    else: clusters.append([h])
                events=[]
                for cluster in clusters:
                    h=min(cluster,key=lambda c:c['y']); x=h['x']; y=h['y']
                    hclefs=sorted((c for c in cs if c['c'] in ['\ue050','\ue062'] and c['x']<x),key=lambda c:c['x'])
                    hc=hclefs[-1]['c'] if hclefs else clef
                    # Diatonic pitch: bottom line E4 for treble, G2 for bass.
                    base=4*7+2 if hc=='\ue050' else 2*7+4
                    step=base+round((upper[-1]-y)/2.48)
                    letter='CDEFGAB'[step%7]; octave=step//7
                    accidental=1 # Seven sharps in the supplied piano score.
                    accs=[c for c in mc if c['c'] in ['\ue261','\ue262','\ue260'] and abs(c['y']-y)<.4 and 0<x-c['x']<16]
                    if accs:
                        accidental={'\ue261':0,'\ue262':1,'\ue260':-1}[max(accs,key=lambda c:c['x'])['c']]
                    duration=HEADS[h['c']]
                    stems=[]
                    for a,b,d in ls:
                        if abs(a.x-b.x)<.02 and abs(a.y-b.y)>9 and abs((d['width'] or 0)-.496)<.04:
                            if min(abs(a.x-(x+.248)),abs(a.x-(x+5.7)))<.7 and min(a.y,b.y)-1<y<max(a.y,b.y)+1:
                                stems.append((a,b,d))
                    stem=min(stems,key=lambda s:min(abs(s[0].y-y),abs(s[1].y-y))) if stems else None
                    if h['c']=='\ue0a4':
                        flagged=any(stem and abs(c['x']-stem[0].x)<.4 and c['c'] in FLAGS and min(stem[0].y,stem[1].y)-2<c['y']<max(stem[0].y,stem[1].y)+2 for c in chars)
                        beamed=False
                        if stem:
                            a,b,_=stem
                            end=max([a,b],key=lambda p:p.y) if abs(a.x-(x+.248))<.7 else min([a,b],key=lambda p:p.y)
                            for d in drawings:
                                if d['type']=='f' and d['fill'] and all(it[0]=='l' for it in d['items']):
                                    r=d['rect']
                                    if r.x0-1<end.x<r.x1+1 and r.y0-1<end.y<r.y1+1 and r.width>8 and r.height<20: beamed=True
                        if flagged or beamed: duration=.5
                    dotted=any(c['c']=='\ue1e7' and 5<x and 0<c['x']-x<12 and abs(c['y']-y)<3 for c in mc)
                    if dotted: duration*=1.5
                    if h['size']<18: duration=0 # small, slashed grace note
                    events.append({'x':round(x,3),'y':round(y,3),'pitch':letter+('#' if accidental==1 else '-' if accidental==-1 else '')+str(octave),'duration':duration,'glyph':hex(ord(h['c'])),'stem':bool(stem),'dot':dotted})
                for c in mc:
                    if c['c'] in RESTS:
                        events.append({'x':round(c['x'],3),'y':round(c['y'],3),'pitch':'r','duration':RESTS[c['c']],'glyph':hex(ord(c['c']))})
                events.sort(key=lambda c:c['x'])
                if events and events[0]['duration']==4 and events[0]['pitch']!='r': events=events[:1]
                output.append({'measure':measure_number,'page':pn,'system':si//2+1,'bounds':[round(left,3),round(right,3)],'staff':upper,'events':events})
                measure_number+=1
    # Match visible tie curves only between consecutive equal melody pitches.
    curves={}
    for pn,page in enumerate(fitz.open(PDF),1):
        curves[pn]=[d['items'][0] for d in page.get_drawings() if d['items'] and d['items'][0][0]=='c']
    all_events=[(m,e) for m in output for e in m['events'] if e['duration']>0]
    for (m,a),(n,b) in zip(all_events,all_events[1:]):
        if a['pitch']=='r' or a['pitch']!=b['pitch']: continue
        if (m['page'],m['system'])==(n['page'],n['system']):
            matched=any(1<c[1].x-a['x']<9 and -2<c[4].x-b['x']<9 and 2<abs(c[1].y-a['y'])<5.5 and 2<abs(c[4].y-b['y'])<5.5 for c in curves[m['page']])
        else:
            outgoing=any(1<c[1].x-a['x']<9 and abs(c[4].x-m['bounds'][1])<3 and 2<abs(c[1].y-a['y'])<5.5 for c in curves[m['page']])
            incoming=any(-12<c[1].x-b['x']<0 and -2<c[4].x-b['x']<9 and 2<abs(c[4].y-b['y'])<5.5 for c in curves[n['page']])
            matched=outgoing and incoming
        if matched:
            a['tie_out']=True; b['tie_in']=True
    (ROOT/'premier-extraction.json').write_text(json.dumps(output,indent=2))
    print('Measures extracted:',len(output))
    print('Mismatched durations:')
    for m in output:
        total=sum(e['duration'] for e in m['events'])
        expected=1 if m['measure']==1 else 4
        if total!=expected: print(m['measure'],m['page'],total,[(e['pitch'],e['duration']) for e in m['events']])
    return output

if __name__=='__main__': extract()
