# Rakathon26

ProstaPaper prepares prostatectomy report scans and annotated PI-RADS drawings
for downstream extraction. The wider challenge is to draft a REDCap registry
record for a doctor to review; see [TASK.md](TASK.md).

## Current component: local preprocessing

The current MVP is one JPG-only script: local Tesseract reads Rakathon IDs,
pairs reports and drawings, masks detected IDs, and writes two JPGs per random
case ID. The original-ID dictionary stays local. It does not interpret medical
findings, populate REDCap, or upload anything.

```text
Local JPG folder
  -> local OCR and ID matching
  -> rotation and black pixel masks
  -> random-case-id/report.jpg + drawing.jpg + manifest.json
```

## Run the artificial-data MVP

```sh
cd preprocess
uv sync --python 3.12
uv run python -I preprocess.py ../Other/data --artificial-data
```

Output is explicitly **unreviewed and artificial-data-only**, not guaranteed
anonymous. Uncertain pairs are skipped. Share only the generated batch folder,
never the private dictionary. Originals are untouched. UI, PDFs, database,
exception handling screens, and medical extraction are outside this MVP.

See the [preprocessing guide](preprocess/README.md) for setup, commands, review
limitations, storage boundaries and the small synthetic checks. Use only synthetic data when sharing
screenshots, demonstrating the UI remotely, or asking an assistant to inspect it.

## Libraries and implementation

| Tool/library | Role |
| --- | --- |
| Python 3.12 and uv | Runtime, dependency management and local environments |
| Pillow | Image loading, colour-preserving preparation and opaque pixel masks |
| Tesseract | Local OCR executable, installed separately from Python packages |
| Python standard library | JSON dictionary/manifest, random UUIDs, and file handling |
| Python `unittest` | Five focused synthetic checks |

The sole Python dependency, Pillow, is declared in [preprocess/pyproject.toml](preprocess/pyproject.toml)
and resolved in [preprocess/uv.lock](preprocess/uv.lock). No hosted OCR or LLM is
part of this preprocessing pipeline. OCR proposes identifiers and document roles;
it is not validated Czech medical transcription.

## macOS, Linux and Windows

Homebrew is only the Mac installation method for Tesseract, not an application
dependency for collaborators on other operating systems.

| Platform | Tesseract installation |
| --- | --- |
| macOS | `brew install tesseract` |
| Debian/Ubuntu Linux | `sudo apt install tesseract-ocr` |
| Windows | Use an installer linked from the [Tesseract installation guide](https://tesseract-ocr.github.io/tessdoc/Installation.html) and add its binary directory to `PATH` |

Check installed language data with `tesseract --list-langs`.
The current script uses `eng` and has no language-selection flag.
Align engine versions and language-data versions across collaborators:
the Python lockfile does not pin the external OCR engine or its language packs.

Each collaborator creates their own Python 3.12 environment with `uv sync`.
Do not copy or commit virtual environments. Git is required to check that
output folders are ignored. The script has only been run here on macOS;
Windows and Linux support have not been certified.

## Privacy and external LLMs

**Removing Rakathon IDs is pseudonymisation, not proof of anonymity and not
permission to upload.** For this project, treat the reports, drawings, previews,
OCR evidence, mappings and derived medical results as sensitive patient data
unless the hospital has documented a different assessment.

External processing can be lawful, but only under an approved arrangement for
the exact purpose, dataset and provider. A no-training setting, EU hosting,
patient consent or a reviewer clicking approve is not sufficient on its own.
Until the responsible institution approves that arrangement, keep real cases
local and use synthetic data for external experiments.

Read the [legal and LLM data-sharing assessment](Other/research/legal-llm-data-sharing.md)
for the GDPR/Czech-law background, provider checklist, uncertainties and dated
primary sources. This is engineering guidance for institutional legal review,
not a legal opinion or an upload authorisation.

The supplied artificial hackathon scans in `Other/` are intentionally Git-tracked;
see `TASK.md`. This does not authorise publishing identifiable production records.
Ignore rules do not remove tracked files or old history.

## Verification limits

Five synthetic checks cover identifier parsing, drawing classification, redaction
pixels, stable pair exports and private comparison-page links. A local run on the
80 supplied artificial scans produced 37 pairs; all 37 agreed with corresponding
filename numbers. This does not establish complete identifier removal or anonymity.
Rotation experiments and investigation of the six excluded images remain follow-up
work. Windows/Linux execution has not been validated.
