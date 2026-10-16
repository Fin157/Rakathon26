# Image pipeline: getting sectors and notes out of the drawing

Summary of `Other/research/` (checked 2026-10-16). Nothing here has been run on our scans yet, apart from one small HSV probe. All scores quoted are vendor numbers, not measurements on these drawings.

## Bottom line

Compute sector overlap with classical CV. Use a vision model only to label marks (outline, arrow, text) and to read handwriting. Three independent research passes reached this conclusion separately.

The reason: the printed template is identical on every sheet, and the 41 sector polygons already exist ([ctsit/imagemap](https://github.com/ctsit/imagemap), `maps/pirads_v2.1.html`, Apache-2.0). Once a scan is aligned to the template, overlap is pixel arithmetic. No VLM has published results on thin, faint, hand-drawn outlines crossing printed lines, and their boxes and points are too coarse for this.

## Main path: classical CV, CPU only, about 11 h for one person

| Step | Method | When it fails | h |
|---|---|---|---:|
| 1. Reference | Clean template + 41 ctsit polygons. Build the ctsit key → REDCap code table (`pzpl_mid_rs` etc.). Key 41 is "External urethral sphincter" in ctsit, "urethra" in REDCap. Check it. | Labels don't line up: fix by hand once. | 0.75 |
| 2. Align | ORB features + RANSAC homography for the whole page, SIFT if ORB gets too few matches, small ECC refinement. Then check residuals per view (base, mid, apex). | Few or clustered inliers, doubled printed lines: doctor clicks 4 landmarks. | 1.75 |
| 3. Ink | Difference from the aligned blank template + chroma in HSV/Lab. Use lightness for pencil. Tune per scan. | Faint yellow, or pencil on top of printed lines: flag for review. | 1.5 |
| 4. Group strokes | Remove template lines, close small gaps, connected components. Classify as outline / arrow-size / text / uncertain by shape (closure, elongation, skeleton branches). | Open arc, or outline merged with text: send the crop to review, don't force-fill it. | 2.0 |
| 5. Score | Per mark and sector: area overlap (filled mark) and stroke contact (open arcs), plus distance to the nearest sector line. | Mark straddles a line: list every sector it touches, flag it. No threshold without clinician labels. | 1.0 |
| 6. VLM check (optional) | See below. | Disagreement with CV becomes a review flag, never an overwrite. | 0.75 |
| 7. Review screen | Original scan, overlay, numbered sectors, scores. Doctor accepts or edits. | Export is blocked until alignment, grouping and side are resolved. | 3.0 |

Code to copy from: [Bishara et al. body-map pipeline](https://github.com/ambishara/body_maps_ijerph) (MIT). It aligns scans of a paper body map to a blank one with ORB + RANSAC, removes the template lines and extracts the marks. That is our steps 2 to 4. It was built for shaded black-pen marks, so the ink step needs changing for our coloured thin strokes.

Skip for now: LoFTR, RoMa, MASt3R and VGGT (GPU-heavy, no advantage on a flat printed form), SAM 2/3 (official repos need CUDA, not built for hand-drawn outlines). XFeat + LightGlue is the one learned matcher worth trying on CPU if ORB fails.

## Where a vision model fits

Feed it one axial view at a time, after alignment. Draw the 41 sectors on the crop with large numbers, and show the CV mask next to the original. Ask it to:

- label each mark as outline, arrow/size line, text or non-tumour note,
- read the handwriting,
- name the numbered sectors the mark touches, with a reason.

Numbered overlays are called Set-of-Mark prompting ([paper](https://arxiv.org/abs/2310.11441)). They improve how well models locate regions in general, but nobody has tested them on drawings like ours. Running the same question several times and checking for disagreement is a cheap uncertainty signal. Disagreement goes to review.

### Cloud (needs an OK before any scan is sent)

| Model ID | Why | Cost per sheet |
|---|---|---|
| `gemini-3.8-flash` | Only general API with documented box and polygon-mask output (0 to 1000 normalised). | ~$0.001 to 0.002 |
| `perceptron-mk1.5` | Native point, box and polygon output. | not published |
| `claude-opus-5-5` | Best published chart-reading score among these (Chartography 89%). Coordinates only via prompt. | ~$0.02 |

All three are reachable here through OpenRouter. In every case we compute overlap from the returned polygon ourselves, and the model never decides side.

### Local

- CPU: `qwen3.5:4b-q4_K_M` via Ollama for "outline or arrow?" on crops. CPU speed is unmeasured.
- 24 to 48 GB GPU: Qwen3.6-27B Q4 (~17 GB), Moondream 3.1 (point, box and SVG-path segmentation, ~10.5 GB, custom license).

## Handwriting ("22 mm", "zánět", P/L)

- [TuzkaOCR](https://github.com/moravianlibrary/TuzkaOCR) (Moravian Library): Czech handwriting recogniser, small ONNX models, runs on CPU. The code is Apache-2.0 but the model files are CC BY-NC-SA, which is fine for a demo. Give it tight crops.
- Any of the VLMs above as a second reader.
- Handwritten sizes are notes, never field values. If one conflicts with the report (7 mm vs 5 mm), the doctor decides.

## Ruled out

- Reve: image generation and editing only, no reading or annotation API.
- DeepSeek-OCR / OCR-2, PaddleOCR-VL, Mistral OCR, Azure, Google Document AI: fine for printed text, but they return text boxes, not hand-drawn marks.
- AWS Textract: no Czech.

## Known traps on our sheets

- Ink colour means nothing. Red, pink, faint yellow and pencil, often mixed.
- Side comes from the report. Axial views had patient right on the viewer's left on all 5 sheets checked. The coronal view is sometimes mirrored.
- Text and drawing can disagree on front versus back (case 14). That is a doctor question, not a bug.
- Report and drawing are the two sides of one sheet, so the drawing's ink shows through on report scans.
- HSV probe on 3 sheets: the ink in the mark regions had a median saturation of 0 to 2. A fixed global hue/saturation threshold will miss faint marks, so step 3 needs the template difference.

## First 2 hours

1. Align 5 sheets (1, 7, 14, 27, 33) and overlay the ctsit polygons. Check by eye.
2. Ink mask + overlap on the same 5 sheets. Check side, level and zone against the reports.
3. If you OK it, send the same 5 axial crops with numbered overlays to `gemini-3.8-flash` and compare with step 2.
