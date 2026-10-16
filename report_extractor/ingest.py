from __future__ import annotations

import csv
import hashlib
import io
import os
import shutil
import subprocess
from pathlib import Path

from .models import (
    ExtractionMethod,
    InputKind,
    TextLayer,
    WordBox,
)


class IngestionError(RuntimeError):
    pass


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _layer_id(source_hash: str, text_hash: str, method: str, tool_version: str) -> str:
    identity = f"{source_hash}:{text_hash}:{method}:{tool_version}".encode("utf-8")
    return "tl-" + hashlib.sha256(identity).hexdigest()[:24]


def _tesseract_version(executable: str) -> str:
    result = subprocess.run(
        [executable, "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.splitlines()[0].removeprefix("tesseract ").strip()


def _ocr_image(path: Path) -> tuple[str, tuple[WordBox, ...], int, int, str]:
    executable = shutil.which("tesseract")
    if executable is None:
        raise IngestionError(
            "Tesseract is not installed. Install Tesseract and Czech language data."
        )
    try:
        environment = os.environ.copy()
        environment.setdefault("OMP_THREAD_LIMIT", "1")
        version = _tesseract_version(executable)
        languages = subprocess.run(
            [executable, "--list-langs"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
            env=environment,
        ).stdout.splitlines()
        if "ces" not in languages:
            raise IngestionError(
                "Tesseract language data 'ces' is unavailable; no OCR was run."
            )
        result = subprocess.run(
            [executable, str(path), "stdout", "-l", "ces", "tsv"],
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
            env=environment,
        )
    except subprocess.TimeoutExpired as exc:
        raise IngestionError("Tesseract timed out; no text layer was saved.") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or "Tesseract returned a non-zero status."
        raise IngestionError(f"OCR failed: {detail}") from exc

    reader = csv.DictReader(io.StringIO(result.stdout), delimiter="\t")
    text_parts: list[str] = []
    words: list[WordBox] = []
    previous_line: tuple[str, str, str, str] | None = None
    image_width = image_height = 0
    text_length = 0
    for row in reader:
        if row["level"] == "1":
            image_width = int(row["width"])
            image_height = int(row["height"])
        if row["level"] != "5" or not row["text"].strip():
            continue
        line = (row["page_num"], row["block_num"], row["par_num"], row["line_num"])
        separator = "\n" if previous_line is not None and line != previous_line else (
            " " if previous_line is not None else ""
        )
        text_parts.append(separator)
        text_length += len(separator)
        start_offset = text_length
        word_text = row["text"]
        text_parts.append(word_text)
        text_length += len(word_text)
        confidence = float(row["conf"])
        words.append(
            WordBox(
                text=word_text,
                start_offset=start_offset,
                end_offset=start_offset + len(word_text),
                x=int(row["left"]),
                y=int(row["top"]),
                width=int(row["width"]),
                height=int(row["height"]),
                confidence=confidence if confidence >= 0 else None,
            )
        )
        previous_line = line

    if not image_width or not image_height:
        raise IngestionError("Tesseract did not return page dimensions.")
    return "".join(text_parts), tuple(words), image_width, image_height, version


def build_text_layer(source: str | Path) -> TextLayer:
    path = Path(source).expanduser()
    if not path.is_file():
        raise IngestionError(f"Input file does not exist: {path}")
    raw = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix in {".txt", ".text"}:
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise IngestionError("Plain-text input must be UTF-8.") from exc
        source_hash = _sha256(raw)
        text_hash = _sha256(text.encode("utf-8"))
        tool_version = "1"
        return TextLayer(
            id=_layer_id(
                source_hash, text_hash, ExtractionMethod.PLAIN_TEXT.value, tool_version
            ),
            source_path=str(path.resolve()),
            source_sha256=source_hash,
            text_sha256=text_hash,
            input_kind=InputKind.TEXT,
            extraction_method=ExtractionMethod.PLAIN_TEXT,
            tool="UTF-8 decoder",
            tool_version=tool_version,
            text=text,
        )
    if suffix not in {".jpg", ".jpeg", ".png"}:
        raise IngestionError("Supported input formats are UTF-8 text, JPEG, and PNG.")
    if suffix == ".png" and not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise IngestionError("The .png input does not have a PNG signature.")
    if suffix in {".jpg", ".jpeg"} and not raw.startswith(b"\xff\xd8"):
        raise IngestionError("The JPEG input does not have a JPEG signature.")

    text, words, width, height, version = _ocr_image(path)
    source_hash = _sha256(raw)
    text_hash = _sha256(text.encode("utf-8"))
    return TextLayer(
        id=_layer_id(
            source_hash, text_hash, ExtractionMethod.TESSERACT.value, version
        ),
        source_path=str(path.resolve()),
        source_sha256=source_hash,
        text_sha256=text_hash,
        input_kind=InputKind.IMAGE,
        extraction_method=ExtractionMethod.TESSERACT,
        tool="Tesseract",
        tool_version=version,
        language="ces",
        text=text,
        words=words,
        image_width=width,
        image_height=height,
    )
