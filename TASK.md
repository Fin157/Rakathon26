# ProstaPaper

Rakathon 2026, MOÚ Brno, 24 hours.

For each radical prostatectomy the pathologist leaves a typed Czech report and a hand-annotated PI-RADS v2.1 drawing. Someone retypes both into the COMPARE registry (REDCap 17.3.7, project 64). We draft that record from the two scans, and a doctor confirms or fixes it.

## Local-only folders

These are git-ignored, so a fresh clone does not have them.

- `Other/data/scan_text/Scan_00NN.jpg`: report scans, 300 dpi, NN = 01 to 40.
- `Other/data/schema/Schema_00NN.jpg`: drawing scans with the same NN.
- `Other/research/`: model and method research for reading the drawings.
- `labels/weak_labels.md`: side, level and zone per focus for 5 cases, read from the reports.
- `Other/slides-with-info.pptx` is the wrong deck (TriaLink, a different challenge).

## Report

The report covers the microscopic finding, the conclusion ("Závěr") and a classification line with pT, L, V, R and grade group. Surgery date, surgery type and lymphadenectomy were missing from every report checked, so the doctor has to enter them.

## Drawing

- Same printed template on every sheet. Coronal and sagittal views on the left. Seminal vesicles, then axial Base, Mid and Apex on the right, with zone labels and dashed sector lines.
- Ink colour has no fixed meaning: red, pink, faint yellow, pencil, often mixed.
- Marks: closed outlines, open arcs, small circles, size arrows, handwritten sizes and notes, P/L letters. Some marks are not tumour, for example "zánět" (inflammation).
- Side comes from the report. In axial views patient right is on the viewer's left on all 5 sheets checked. The coronal view is sometimes mirrored.
- Text and drawing can disagree, for example front versus back. The doctor resolves it.
- Report and drawing are the two sides of one sheet. Red marks showing through on report scans are the drawing's ink.

## Target fields

Two instruments: `surgery_c61`, one per surgery, and the repeating `surgery_c61_resected_lesion`, one per focus. The drawing feeds `sur_prostate_regions`, a 41-choice sector checkbox per lesion. Everything else comes from the text.

## Plan

1. Internal schema covering everything we can get from text and drawing, with evidence and basis (`explicit`, `inferred`, `absent`) per field.
2. Extraction. Text first. Drawing second, for sectors per focus and handwritten notes.
3. Mapping to a REDCap import CSV.
4. Doctor GUI: both scans, the draft record, a clickable sector map, and a queue of uncertainties and conflicts.

No training data or labels, so we use only off-the-shelf models and classical CV.
