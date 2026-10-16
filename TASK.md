# ProstaPaper: the challenge

Rakathon 2026, Masaryk Memorial Cancer Institute (MOÚ), Brno. 24-hour build.

## Problem

After a radical prostatectomy the pathologist produces two paper artefacts per patient:

1. A typed Czech pathology report. It holds the macroscopic and microscopic findings, a conclusion ("Závěr") and a classification line with TNM stage, lymphatic and vascular invasion, margin status and grade group.
2. A printed PI-RADS v2.1 prostate drawing with hand-drawn outlines of each tumour focus, handwritten sizes and notes.

Someone currently retypes both into the COMPARE registry in REDCap (project 64, REDCap 17.3.7). We build a tool that drafts the record from the two scans and lets a doctor confirm or fix it quickly.

## Data in this repo

`Other/` is git-ignored and holds the sample set.

| Path | Content |
|---|---|
| `Other/data/scan_text/Scan_0001.jpg` … `Scan_0040.jpg` | 300 dpi scans of printed Czech reports. Mostly the microscopic finding, conclusion and classification. Reverse-side show-through. |
| `Other/data/schema/Schema_0001.jpg` … `Schema_0040.jpg` | 300 dpi scans of the annotated drawing. |
| `Other/slides-with-info.pptx` | **Wrong deck.** It describes TriaLink, a clinical-trial matching challenge, not ProstaPaper. Ask the organisers for the ProstaPaper slides. |

Report and drawing share an ID printed on the page. File numbers appear to match the ID, but that has only been spot-checked.

## What the drawings look like

- The printed template is the same on every sheet: coronal and sagittal views on the left; seminal vesicles, then axial Base, Mid and Apex slices on the right, with zone labels and dashed sector lines.
- Ink colour varies by sheet and means nothing fixed. We have seen red, pink, faint yellow and black pencil, often several on one sheet.
- Marks include closed outlines, open arcs, tiny circles, double-traced loops, size arrows, handwritten notes including inflammation, and side letters P/L.
- In the axial views patient right is on the viewer's left on every sheet checked so far (5). The coronal view is sometimes drawn mirrored. The report text decides side.
- Drawing and text can disagree on front/back. These become questions for the doctor.
- Report and drawing are the two sides of one sheet. The red "show-through" on report scans is the drawing's ink, mirrored.
- Some marks are not tumour (inflammation notes).

## Target

The REDCap instruments that matter are `surgery_c61` (one per surgery) and the repeating `surgery_c61_resected_lesion` (one per focus). The image-relevant field is `sur_prostate_regions`, a 41-choice checkbox of PI-RADS sectors per lesion. Most other fields (pT, R, L, V, Gleason, ISUP, invasion flags, sizes) come from the text.

Several required fields (surgery date, surgery type, lymphadenectomy) were absent from every report checked so far. The tool must ask for them.

## Our plan, in order

1. **Internal schema.** One record model covering everything worth mining from the text and the drawing, with per-field evidence and a basis (`explicit`, `inferred`, `absent`).
2. **Extraction.** Text first: regex for the classification line, LLM for per-focus details. Drawing second: sector proposals per focus and handwritten notes.
3. **REDCap mapping.** Internal schema to a validated REDCap import CSV. API import only once rights are confirmed.
4. **Doctor GUI.** Side-by-side scans, draft record, a clickable sector map, and a queue of uncertainties and text/drawing conflicts for the doctor to resolve.

Constraints: no training data, no labels, no time to fine-tune. Off-the-shelf models and classical CV only. Whether anonymised scans may go to a cloud model is a separate decision for the team and organisers.

## Further reading

- `PROSTAPAPER_PLAN.md`: the detailed plan from the first planning session (written for 48 h; trim to 24 h).
- `research/`: model and method research for reading the drawings.
