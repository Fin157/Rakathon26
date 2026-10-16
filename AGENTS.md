# AGENTS.md

ProstaPaper: draft a REDCap registry record from a scanned Czech prostatectomy report and a hand-annotated PI-RADS drawing, then let a doctor review it. Read `TASK.md` before starting any task. It covers the challenge, the data and the target fields.

This is a 24-hour hackathon. A working end-to-end slice beats a polished partial one.

## Patient data

- Scans live in `Other/`, which is git-ignored. Keep scans, reports, extracted text, model output on real cases and tokens out of git. Add a new data or output folder to `.gitignore` before the first write.
- Send a scan or extracted text to an external model or service only when the user has said so in the current session. Local processing is fine.

## Extraction rules

- Every proposed value carries evidence, either a quoted text span or an image crop with coordinates, and a basis of `explicit` or `inferred`. Missing findings get `absent`.
- Show inferred suggestions apart from explicit findings, with their evidence and reasoning. A doctor confirms them before export.
- When text and drawing disagree, keep both values and raise an issue for the doctor. Neither source overwrites the other.
- A drawing mark alone never creates a lesion. Unmatched marks become review issues.
- The report text decides side (vpravo/vlevo, pravý/levý, P/L lalok). Mark position and handwritten P/L letters are supporting evidence, and any disagreement raises an issue. In axial views patient right is usually on the viewer's left. The coronal view is sometimes drawn mirrored.
- Ink colour has no fixed meaning. Every non-template stroke is a candidate mark, whatever its colour.

## Working agreement

- Inspect the files, data and command output before claiming anything about them. Say what you verified and label guesses.
- Carry authorized work through implementation and verification. Ask again only when new information changes the scope or needs a separate decision.
- Measure model accuracy on our scans, not on vendor benchmarks. A run on three sheets is a probe, so call it one.
- Write plainly. Cut praise, filler, repeated explanations and process narration.
- Change only what the task needs. Commit only when asked.
