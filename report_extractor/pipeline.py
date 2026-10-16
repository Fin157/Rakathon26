from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from . import __version__
from .extractors import OUTPUT_CONTRACT_VERSION, PROMPT_VERSION, Extractor
from .models import SCHEMA_VERSION, TextLayer
from .render import render_html
from .validation import QuarantinedItem, ValidationResult, validate_payload


class DocumentMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str
    kind: str = "text_report"
    language: str = "cs"
    source_path: str
    source_sha256: str


class ExtractionMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str
    document_id: str
    source_text_layer_id: str
    created_at: datetime
    extractor_version: str
    schema_version: str
    prompt_version: str
    output_contract_version: str
    mode: str
    complete: bool
    evidence: list[dict[str, Any]]
    subjects: list[dict[str, Any]]
    coverage: list[dict[str, Any]]
    observations: list[dict[str, Any]]
    issues: list[dict[str, Any]]


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n"


def run_extraction(
    text_layer: TextLayer,
    extractor: Extractor,
    output_root: str | Path,
) -> Path:
    raw_payload = extractor.extract(text_layer)
    result = validate_payload(raw_payload, text_layer)
    document = DocumentMetadata(
        id=str(uuid.uuid4()),
        source_path=text_layer.source_path,
        source_sha256=text_layer.source_sha256,
    )
    extraction = ExtractionMetadata(
        id=str(uuid.uuid4()),
        document_id=document.id,
        source_text_layer_id=text_layer.id,
        created_at=datetime.now(UTC),
        extractor_version=f"report-extractor/{__version__}",
        schema_version=SCHEMA_VERSION,
        prompt_version=PROMPT_VERSION,
        output_contract_version=OUTPUT_CONTRACT_VERSION,
        mode=extractor.mode,
        complete=result.complete,
        evidence=[item.model_dump(mode="json") for item in result.evidence],
        subjects=[item.model_dump(mode="json") for item in result.subjects],
        coverage=[item.model_dump(mode="json") for item in result.coverage],
        observations=[item.model_dump(mode="json") for item in result.observations],
        issues=[item.model_dump(mode="json") for item in result.issues],
    )
    quarantine = [
        {
            "item_type": item.item_type,
            "item_id": item.item_id,
            "raw": item.raw,
            "reasons": item.reasons,
        }
        for item in result.quarantine
    ]
    bundle = {
        "document": document.model_dump(mode="json"),
        "text_layer": text_layer.model_dump(mode="json"),
        "extraction": extraction.model_dump(mode="json"),
        "quarantine": quarantine,
        "validation_errors": result.errors,
    }
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = Path(output_root).expanduser() / f"{timestamp}-{uuid.uuid4().hex[:8]}"
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "text-layer.json").write_text(
        _json_dump(text_layer.model_dump(mode="json")), encoding="utf-8"
    )
    (run_dir / "result.json").write_text(_json_dump(bundle), encoding="utf-8")
    (run_dir / "review.html").write_text(
        render_html(
            document.model_dump(mode="json"),
            text_layer,
            extraction.model_dump(mode="json"),
            result,
        ),
        encoding="utf-8",
    )
    return run_dir
