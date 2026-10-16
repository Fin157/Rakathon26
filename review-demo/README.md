# Review workspace — static proof of concept

A dependency-free, synthetic-data demonstration of the review concept discussed for ProstaPaper. This is a UI prototype, not a clinical tool or an extraction pipeline.

## Open it

Check out `review_dev`, then open `review-demo/index.html` in a modern browser. No build, package installation, account, API key, network connection, or server is required. Alternatively, serve the repository with any local static web server and open `/review-demo/`.

GitHub's file viewer shows source code; download or clone the files to view the interactive page. This change does not configure GitHub Pages or deploy anything.

## Try the review flow

1. Select L1 or L2 on either schematic or in the lesion tabs. The report excerpt and aggregate selection follow each other. Use **Show report evidence** to scroll to the source text.
2. Inspect L1's blocking location conflict: the dummy report says anterior while the dummy drawing suggests posterior. Both candidates are shown on the clean diagram until a decision is made.
3. Choose **Review competing interpretations**, select a location, and enter a reviewer name and reason. The aggregate diagram and property assessment update; the source drawing and report stay unchanged. Keeping it unresolved keeps approval blocked.
4. Inspect and optionally acknowledge the two non-blocking issues. Acknowledgement retains their unresolved meaning. M1 never becomes a third lesion.
5. Approve the summary with explicit acknowledgement of remaining limitations, or refuse it with a reason. Final decisions lock issue editing; **Reopen review** records a superseding review action before editing resumes.
6. Use **Save draft**, refresh, or **Reset demo**. Decisions normally persist in browser localStorage. When storage is unavailable (including some file-URL configurations), the page keeps working in memory and warns that persistence is unavailable.

## What is real and what is mocked

- The two-pane layout, selectable SVG marks, grade legend, evidence navigation, issue filters, zoom controls, decision dialogs, approval guard, decision history and local persistence are implemented.
- The report and scanned-paper-style diagram are intentionally invented fixtures, labelled synthetic throughout. No scans or patient data are used, and no external assets are requested.
- Anatomical drawings are illustrative categorical schematics, **not the validated 41-sector PI-RADS map**, not calibrated contours, and not a physical or 3D reconstruction. Laterality is assigned from the dummy report; it is not independently corroborated by the dummy drawing.
- Grade colours illustrate GG1–GG5; fixture lesions use GG1 and GG3. Labels and outline styles also convey meaning. Grade is kept separate from conflict severity. No grading calculation or clinical inference runs.
- All decision state is browser-local. There is no extraction, matching service, authentication, secure audit store, multi-user workflow, export, or database connection. Reviewer names are free text, not authenticated identities. Do not enter real patient information.
- Reopening preserves the previous final decision in history, but this demo does not implement production immutable revision management.

## Files

- `index.html`: accessible page structure and native review dialog.
- `styles.css`: responsive two-pane workspace and visual states.
- `app.js`: dummy fixtures, SVG drawing, review state and local persistence.

## Manual acceptance checks

- Open the page offline and confirm all content is visible without external requests.
- Use mouse and keyboard (Tab, Enter/Space, Escape) to select marks, inspect issues and operate dialogs.
- Verify approval is blocked until the L1 location conflict has a selected interpretation; keeping it unresolved must not unblock approval.
- Verify choosing anterior moves only the clean L1 sector depictions, not the source outlines. Choosing posterior retains source counterevidence in the decision history.
- Verify acknowledgement does not change L2's provisional match or turn M1 into a lesion.
- Verify a reviewer name, reason, and approval acknowledgement are required. Refusal must require a reason too.
- Verify final decisions disable issue editing and reopening preserves history.
- Save, reload, and reset; repeat with browser storage disabled.
- Check a narrow mobile viewport, scrolling and source zoom, focus indicators and non-colour status labels.

These are acceptance checks for the prototype, not a claim that browser automation or clinical validation has been performed.
