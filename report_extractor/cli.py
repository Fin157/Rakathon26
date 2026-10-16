from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

from .extractors import ExternalExtractorDisabled, FixtureExtractor
from .ingest import IngestionError, build_text_layer
from .models import ExtractionProposal
from .pipeline import run_extraction
from .render import render_text_layer_preview


def _unique_output_dir(output_root: str | Path, prefix: str) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output = Path(output_root).expanduser() / f"{prefix}-{timestamp}-{uuid.uuid4().hex[:8]}"
    output.mkdir(parents=True, exist_ok=False)
    return output


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="report-extractor",
        description="Offline report text ingestion and fixture-backed review output.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser(
        "ingest", help="Create a versioned immutable text layer from text/JPEG/PNG."
    )
    ingest.add_argument("--input", required=True, type=Path)
    ingest.add_argument("--output-dir", type=Path, default=Path("Other/output"))

    commands.add_parser(
        "schema", help="Print the versioned Pydantic extraction-response JSON Schema."
    )

    run = commands.add_parser(
        "run", help="Validate an explicitly selected fixture or disabled external mode."
    )
    run.add_argument("--input", required=True, type=Path)
    run.add_argument("--mode", choices=("fixture", "external"), required=True)
    run.add_argument("--fixture-file", type=Path)
    run.add_argument("--output-dir", type=Path, default=Path("Other/output"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "schema":
        print(json.dumps(ExtractionProposal.model_json_schema(), ensure_ascii=False, indent=2))
        return 0
    try:
        text_layer = build_text_layer(args.input)
        if args.command == "ingest":
            output = _unique_output_dir(args.output_dir, "text-layer")
            (output / "text-layer.json").write_text(
                json.dumps(
                    text_layer.model_dump(mode="json"),
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (output / "page-1-text.txt").write_text(text_layer.text, encoding="utf-8")
            (output / "review.html").write_text(
                render_text_layer_preview(text_layer), encoding="utf-8"
            )
            print(f"Saved immutable page-1 text layer and local review under {output}")
            return 0
        if args.mode == "fixture":
            if args.fixture_file is None:
                raise IngestionError(
                    "Fixture mode requires --fixture-file and exact source-text hash match."
                )
            extractor = FixtureExtractor(args.fixture_file)
        else:
            extractor = ExternalExtractorDisabled()
        output = run_extraction(text_layer, extractor, args.output_dir)
        print(f"Mode: {extractor.mode}; local review output: {output}")
        return 0
    except (IngestionError, OSError, ValueError, RuntimeError) as exc:
        print(f"report-extractor: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
