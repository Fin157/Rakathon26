# AGENTS.md

ProstaPaper: draft a REDCap registry record from a scanned Czech prostatectomy report and a hand-annotated PI-RADS drawing, then let a doctor review it. Read `TASK.md` for the challenge, the data and the target fields before starting any task.

This is a 24-hour hackathon. A working end-to-end slice beats a polished partial one.

## Patient data

- Scans live in `Other/`, which is git-ignored. Keep every scan, report, extracted text, model output on real cases and token out of git. New data or output folders go in `.gitignore` before the first write.
- Send a scan or extracted text to an external model or service only when the user has said so in the current session. Local processing is always fine.
- Python that reads files from `Other/` runs with `-I`. Scripts live outside `Other/`.

## Extraction rules

These hold for every extractor, text or image.

- Every proposed value carries evidence, either a quoted text span or an image crop and coordinates, and a basis of `explicit` or `inferred`. Use `absent` for missing findings.
- Show inferred suggestions separately from explicit findings, with their evidence and reasoning. A doctor must confirm them before export.
- A REDCap default is not evidence. Missing findings stay empty.
- When text and drawing disagree, keep both values and raise an issue for the doctor. Neither source overwrites the other.
- A drawing mark alone never creates a lesion. Unmatched marks become review issues.
- Side comes from the report text (vpravo/vlevo, pravý/levý, P/L lalok). Mark position and handwritten P/L letters are supporting evidence; any disagreement raises an issue. In axial views patient right is usually on the viewer's left, but the coronal view is sometimes drawn mirrored.
- Ink colour means nothing fixed. Treat every non-template stroke as a candidate mark, whatever its colour.

## Working agreement

- Inspect the files, data and command output before claiming anything about them. Say what you verified and label guesses.
- Carry authorized work through implementation and verification. Ask again only when new information changes the scope or requires a separate decision.
- Measure model accuracy on our scans, never on vendor benchmarks. A probe on three sheets is a probe; say so.
- Python 3.12 with `uv`. Add dependencies with `uv add`.
- Research notes go in `research/<topic>.md`: recommendation first, then details, then dated primary sources.
- Write plainly and directly. Cut praise, filler, repeated explanations and unnecessary process narration.
- Change only what the task needs. Commit only when asked.
