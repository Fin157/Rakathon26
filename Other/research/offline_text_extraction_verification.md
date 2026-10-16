# Offline text-report extraction verification

## Scope and repository snapshot

- The feature branch starts directly from `review_dev` at `9052d960d7eefc194cc0252de763e8088254ef83`; this is a new feature branch, not a change to `review_dev`.
- The current base contains the existing static `review-demo`, but no Python extraction package, dependency manifest, or test suite. This implementation adds only the offline text-report slice.
- The prior test-data commit `ac320e2a0e4113222a65dc86bc628f4359ecd3bd` is not present in the shallow local object database, so a historical file-by-file comparison to that commit could not be made. Current inspection found 37 case directories, each with `report.jpg` and `drawing.jpg`, and a manifest marked `data_scope: artificial` and `review_status: not_reviewed`. It is not semantic ground truth.
- Only the three `report.jpg` paths below were used for the OCR probe. No `drawing.jpg` was opened by OCR, and no report output is committed.

## Reproducible local commands

From the repository root, after the setup in `README.md`:

```sh
python -m unittest discover -s tests -v
python -m report_extractor schema
python -m report_extractor run \
  --input fixtures/synthetic_report.txt \
  --mode fixture \
  --fixture-file fixtures/synthetic_response.json \
  --output-dir Other/output/fixture-demo
```

For a local OCR probe:

```sh
python -m report_extractor ingest \
  --input Other/preprocessed/batch-22d4f91f-fa1e-4cad-99f5-73b8245808b4/0359bf00-2223-4fd3-8bda-7aa3cc695382/report.jpg \
  --output-dir Other/output/ocr-probe
python -m report_extractor ingest \
  --input Other/preprocessed/batch-22d4f91f-fa1e-4cad-99f5-73b8245808b4/1105712e-8d9e-42bc-b161-4446601c1978/report.jpg \
  --output-dir Other/output/ocr-probe
python -m report_extractor ingest \
  --input Other/preprocessed/batch-22d4f91f-fa1e-4cad-99f5-73b8245808b4/16609ad4-7a01-40b4-a065-ae9e5b0edc4d/report.jpg \
  --output-dir Other/output/ocr-probe
```

Each command creates a unique subdirectory containing `text-layer.json`, `page-1-text.txt`, and local `review.html`. The existing `.gitignore` rule for `Other/output/` was checked before these writes; generated text, scans embedded in HTML, and source-linked outputs remain ignored.

External extraction is deliberately disabled. This command exits with status 2 and makes no network request:

```sh
python -m report_extractor run \
  --input fixtures/synthetic_report.txt \
  --mode external \
  --output-dir Other/output/disabled
```

## Local OCR probe

The runtime was Python 3.12.3, Pydantic 2.14.1, Tesseract 5.3.4, and Czech trained-data package `tesseract-ocr-ces` 1:4.1.0-2. Tesseract's installed language list included `ces`. The pipeline invokes Tesseract locally with `-l ces` and limits its OpenMP thread count to one by default.

An initial attempt to run all three OCR processes concurrently exceeded the 180-second per-image timeout. After constraining Tesseract to one thread per process, all three local OCR runs completed. This establishes a usable local probe path in this environment, not why the first run timed out.

| Case ID | Input path (from repository root) | Image size | Extracted text chars | OCR words | Words with OCR confidence |
|---|---|---:|---:|---:|---:|
| `0359bf00-2223-4fd3-8bda-7aa3cc695382` | `Other/preprocessed/batch-22d4f91f-fa1e-4cad-99f5-73b8245808b4/0359bf00-2223-4fd3-8bda-7aa3cc695382/report.jpg` | 2456 × 2903 | 1797 | 252 | 252 |
| `1105712e-8d9e-42bc-b161-4446601c1978` | `Other/preprocessed/batch-22d4f91f-fa1e-4cad-99f5-73b8245808b4/1105712e-8d9e-42bc-b161-4446601c1978/report.jpg` | 2454 × 2863 | 1838 | 240 | 240 |
| `16609ad4-7a01-40b4-a065-ae9e5b0edc4d` | `Other/preprocessed/batch-22d4f91f-fa1e-4cad-99f5-73b8245808b4/16609ad4-7a01-40b4-a065-ae9e5b0edc4d/report.jpg` | 2453 × 2845 | 1843 | 255 | 255 |

All three text layers were non-empty, page 1, had source-image word boxes, and had Tesseract confidence values for every returned word. A simple automatic check found the expected report headings in each text layer. This checks only that OCR returned plausible structure; it is not an accuracy measurement.

The `0359bf00` original scan was visually inspected, and its local OCR text was spot-checked against the visible page. The main page structure was captured, but character-level recognition errors were visible. The other two scans were checked automatically for non-empty text, word/coordinate/confidence counts, and headings; they were not visually compared. No reference transcripts or annotations were made.

OCR confidence is a reading signal only, not a calibrated medical confidence. These three sheets are a probe, not a benchmark or semantic extraction result. The manifest is not ground truth. No model calls, external processing, or semantic outputs were made for these three reports.

## Offline integration results and remaining work

- Twelve `unittest` tests pass. They cover the synthetic Czech/plain-text fixture and JSON/HTML flow; multi-focus and specimen/focus scope; explicit negative, not reported, unreadable, not assessed, not applicable, and unchecked coverage; conflicting values; unresolved attribution; dimensions without invented axes; invalid status/value combinations; missing, mismatched, and dangling evidence/references; dependency quarantine and cycles; late subject invalidation and dependent-reference quarantine; safe lone-surrogate serialization; HTML escaping; fixture hash binding; and disabled external mode.
- The synthetic fixture demo produced schema-aligned JSON and a local static HTML page with fixture labeling, quotations, coverage, uncertainty, and quarantine sections. The output contains no remote scripts, fonts, analytics, or requests.
- The end-to-end synthetic demo is plumbing verification only. No live model/provider integration, model extraction accuracy, medical accuracy, or clinical validity has been established.
- A future provider-neutral adapter, live extraction, and accuracy review with appropriate ground truth remain unverified and outside this milestone.
