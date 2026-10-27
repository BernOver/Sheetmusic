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
