# Cicada — Trombone 1

Provisional transcription from all twelve supplied full-score screenshots.
Music by GoodKid; arrangement credited to Blake Nellis in the source.

- `output/Cicada-Trombone-1-draft.pdf`: printable standalone Trombone 1 part.
- `output/Cicada-Trombone-1-draft.musicxml`: editable notation for MuseScore and other notation software.
- `transcription.json`: measure-by-measure pitch and duration reference (quarter-note units).
- `build_part.py`: reproducible notation and PDF generation.

Coverage: source measures 1–113, including the opening pickup and final barline. Bass clef,
concert pitch, two flats, 4/4, quarter note = 176. Only Trombone 1 is included.
This is a provisional visual transcription, not an extracted original part.
The opening pickup and first full bar (m. 1–2) are uncertain at the screenshot
resolution and require a close-up; pickup notes are colored red. All pitches,
rhythms, ties, and dynamics should receive a source comparison before performance.
All twelve supplied pages are represented, including the ending.
Consecutive full-bar rests are combined into numbered multimeasure rests
(m. 10–17: 8 bars; m. 42–49: 8 bars; m. 90–91: 2 bars), retaining source measure numbers.

Generate in the existing checkout (no additional worktree needed):

```sh
cd /workspace/Sheetmusic
PYTHONPATH=/workspace/.sheetmusic-tools python build_part.py
```

Dependencies: music21, verovio, cairosvg, and pypdf. They are development tools,
not needed to open or print the resulting PDF or import the MusicXML.

## Separate melody arrangement

`output/Cicada-Trombone-Melody-draft.pdf` and its MusicXML counterpart contain
a separate main-melody adaptation for trombone, in bass clef and the same concert
key. The flute's printed melody is lowered two octaves. Optional flute octave
extensions are not applied. During the flute's unpitched vocal cues (m. 76–77,
80–81, 84–85), a marked Trombone 1 fill is used, lowered one octave from the
original brass part. Consecutive whole-bar rests use multimeasure notation.

This is a provisional manual transcription from screenshots. Pitches, rhythms,
ornaments, and phrase connections need comparison with a clearer source before
performance; it is not a verified note-for-note extraction. The original
Trombone 1 part remains separate and unchanged.

Regenerate using `PYTHONPATH=/workspace/.sheetmusic-tools python build_melody.py`.
`melody-transcription.json` retains both the source-register notes and the
transposed notes for review. The two-octave lowering is consistent throughout
the flute-derived material, with no key change.

## Premier Inn — Euphonium melody

- [Printable euphonium PDF](output/Premier-Inn-Euphonium-Melody.pdf)
- [Editable MusicXML](output/Premier-Inn-Euphonium-Melody.musicxml)
- [MuseScore project (.mscz)](output/Premier-Inn-Euphonium-Melody.mscz)

Separate arrangement of **Premier Inn** by **Good Kid**, based on the upper
melody of the supplied piano arrangement credited to **Yoyo1235**. It covers
all 157 source measures, including the one-beat pickup. Piano chords and the
left-hand accompaniment are omitted.

The melody is lowered **one octave** for **concert-pitch bass-clef euphonium**.
The printed key is **D-flat major**, equivalent to the source's C-sharp major;
this respelling changes no sounding pitches. Range: **B-flat2–A-flat4**.
Tempo: quarter note = 180. Source melody ties and the two grace notes are
retained; the four full-bar rests at m. 154–157 form one multimeasure rest.
Dynamics follow the main sections of the piano arrangement. This is an
extracted upper-voice adaptation, rather than a transcription of all piano voices.

The PDF's vector notehead positions, flags, beams and clef changes are decoded
by `extract_premier.py`. Its `premier-extraction.json` output retains the
source coordinates, pitches, durations and tie matches for inspection.
`build_euphonium.py` uses that data to regenerate the notation; it does not
need the original PDF. `euphonium-transcription.json` records the resulting
concert pitches. The supplied PDF is kept in ignored local `sources/` and
is not included in the GitHub upload.

```sh
cd /workspace/Sheetmusic
PYTHONPATH=/workspace/.sheetmusic-tools python build_euphonium.py
```

Validation checks every measure's length, every note's one-octave transposition,
the enharmonic key, all matched ties, the rest count and the PDF page count.
The layout and representative passages have been visually checked against the
source PDF. A full performance proofread is still recommended.
