"""Build a private, offline comparison page for an existing JPG batch."""

import argparse
from html import escape
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def build_review(batch: Path, private: Path) -> tuple[Path, int]:
    batch = batch.resolve()
    manifest = json.loads((batch / "manifest.json").read_text())
    mapping = json.loads((private / "dictionary.json").read_text())
    by_case = {entry["case_id"]: (identifier, entry) for identifier, entry in mapping.items()}
    sections = []
    for case_id, paths in manifest["cases"].items():
        identifier, entry = by_case[case_id]
        sources = {source["role"]: source for source in entry["sources"]}
        rows = []
        for role in ("report", "drawing"):
            source = Path(sources[role]["source"]).resolve()
            redacted = (batch / paths[role]).resolve()
            if not redacted.is_relative_to(batch) or not source.is_file() or not redacted.is_file():
                raise ValueError("Missing image or invalid batch path.")
            cells = []
            for label, path in (("Original", source), ("Redacted", redacted)):
                uri = escape(path.as_uri(), quote=True)
                cells.append(
                    f'<td><a href="{uri}">{label}: open full size</a>'
                    f'<br><img loading="lazy" src="{uri}" alt="{label} {role}"></td>'
                )
            rows.append(
                f'<tr><th colspan="2">{role.title()} '
                f'(export rotation: {int(sources[role]["rotation"])} degrees clockwise)</th></tr>'
                f'<tr>{"".join(cells)}</tr>'
            )
        sections.append(
            f"<section><h2>{escape(identifier)}</h2>"
            f"<p>Case ID: <code>{escape(case_id)}</code></p><table>"
            f'{"".join(rows)}</table></section>'
        )
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy"
 content="default-src 'none'; img-src file:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>PRIVATE: original and redacted scan comparison</title>
<style>
body { font: 16px sans-serif; margin: 24px; }
section { border-top: 3px solid #555; margin-top: 40px; }
table { width: 100%; table-layout: fixed; }
td { width: 50%; vertical-align: top; }
th { text-align: left; padding-top: 16px; }
img { width: 100%; height: auto; }
code { overflow-wrap: anywhere; }
</style></head><body>
<h1>PRIVATE: local comparison only</h1>
<p>Do not upload this page or the private dictionary. Only share the redacted batch.</p>
<p>Original IDs and random case IDs below provide the back-matching.
Use browser Find to locate either ID. Check both documents, black masks,
rotation and preserved annotations. Originals are shown in their original orientation.</p>
<p>This page does not record approval or change the batch's unreviewed status.</p>
"""
    output = private / f"review-{batch.name}.html"
    if output.is_symlink():
        raise ValueError("Review output must not be a symbolic link.")
    with output.open("w", encoding="utf-8") as stream:
        os.chmod(output, 0o600)
        stream.write(page + "".join(sections) + "</body></html>\n")
    return output, len(sections)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()
    private = HERE / ".preprocess-private"
    try:
        ignored = subprocess.run(
            ["git", "-C", str(HERE), "check-ignore", "-q", str(private) + "/"],
            capture_output=True, check=False,
        )
        tracked = subprocess.run(
            ["git", "-C", str(HERE), "ls-files", "--", str(private)],
            capture_output=True, check=False,
        )
        if ignored.returncode or tracked.returncode or tracked.stdout or private.is_symlink():
            raise ValueError("Private folder must be ignored and untracked.")
        page, count = build_review(args.batch, private)
        print(f"Local comparison page for {count} pairs: {page}")
    except (OSError, ValueError, KeyError):
        print("Cannot build review page. Check the local batch, private mapping and source files.",
              file=sys.stderr)
        sys.exit(2)
