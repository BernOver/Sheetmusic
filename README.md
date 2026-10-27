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
Rests remain individually numbered to simplify checking against the full score.

Generate in the existing checkout (no additional worktree needed):

```sh
cd /workspace/Sheetmusic
PYTHONPATH=/workspace/.sheetmusic-tools python build_part.py
```

Dependencies: music21, verovio, cairosvg, and pypdf. They are development tools,
not needed to open or print the resulting PDF or import the MusicXML.
