from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "1.0.0"
OFFSET_CONVENTION = (
    "Python Unicode code-point offsets into the immutable text layer; "
    "half-open [start_offset, end_offset)."
)
COORDINATE_CONVENTION = (
    "Source-image pixels; origin at upper-left; x increases rightward and "
    "y increases downward; width and height are pixel lengths."
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class InputKind(StrEnum):
    TEXT = "text"
    IMAGE = "image"


class ExtractionMethod(StrEnum):
    PLAIN_TEXT = "plain_text"
    TESSERACT = "tesseract"


class WordBox(StrictModel):
    text: str
    start_offset: int = Field(ge=0)
    end_offset: int = Field(gt=0)
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    confidence: float | None = Field(default=None, ge=0, le=100)


class TextLayer(StrictModel):
    id: str
    source_path: str
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    input_kind: InputKind
    extraction_method: ExtractionMethod
    tool: str
    tool_version: str
    language: str | None = None
    page: Literal[1] = 1
    text: str
    words: tuple[WordBox, ...] = ()
    image_width: int | None = Field(default=None, gt=0)
    image_height: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def method_matches_input(self) -> TextLayer:
        if self.input_kind == InputKind.TEXT:
            if self.extraction_method != ExtractionMethod.PLAIN_TEXT:
                raise ValueError("plain-text input must use the plain_text method")
            if self.words or self.image_width or self.image_height:
                raise ValueError("plain-text input cannot claim scan coordinates")
        else:
            if self.extraction_method != ExtractionMethod.TESSERACT:
                raise ValueError("image input must use the tesseract method")
            if self.image_width is None or self.image_height is None:
                raise ValueError("image dimensions are required for OCR")
            if any(
                word.x + word.width > self.image_width
                or word.y + word.height > self.image_height
                or word.end_offset > len(self.text)
                or self.text[word.start_offset : word.end_offset] != word.text
                for word in self.words
            ):
                raise ValueError("OCR word coordinates or offsets exceed the source")
        return self


class SubjectKind(StrEnum):
    SPECIMEN = "specimen"
    TUMOUR_FOCUS = "tumour_focus"
    OTHER_FINDING = "other_finding"
    TISSUE_SAMPLE = "tissue_sample"


class Basis(StrEnum):
    EXPLICIT = "explicit"
    NORMALIZED = "normalized"
    INFERRED = "inferred"
    CALCULATED = "calculated"


class PrototypeBasis(StrEnum):
    EXPLICIT = "explicit"
    NORMALIZED = "normalized"


class ReviewStatus(StrEnum):
    UNREVIEWED = "unreviewed"
    ACCEPTED = "accepted"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"


class AvailabilityStatus(StrEnum):
    RECORDED = "recorded"
    NOT_REPORTED = "not reported"
    UNREADABLE = "unreadable"
    NOT_ASSESSED = "not assessed"
    NOT_APPLICABLE = "not applicable"


class CertaintyLevel(StrEnum):
    UNASSESSED = "unassessed"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ObservationProperty(StrEnum):
    GLEASON_PATTERNS = "gleason_patterns"
    GLEASON_SCORE = "gleason_score"
    GRADE_GROUP = "grade_group"
    CLASSIFICATION_PT = "classification_pt"
    CLASSIFICATION_L = "classification_l"
    CLASSIFICATION_V = "classification_v"
    CLASSIFICATION_R = "classification_r"
    DIMENSIONS = "dimensions"
    TEXTUAL_LOCATION = "textual_location"
    PRESENCE = "presence"


class ImageRegion(StrictModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    coordinate_convention: Literal[COORDINATE_CONVENTION] = COORDINATE_CONVENTION


class Evidence(StrictModel):
    id: str
    text_layer_id: str
    page: Literal[1] = 1
    quotation: str
    start_offset: int = Field(ge=0)
    end_offset: int = Field(gt=0)
    offset_convention: Literal[OFFSET_CONVENTION] = OFFSET_CONVENTION
    image_region: ImageRegion | None = None


class Subject(StrictModel):
    id: str
    kind: SubjectKind
    label: str
    identification_basis: Literal["explicit", "proposed"]
    parent_id: str | None = None
    evidence_ids: tuple[str, ...] = Field(min_length=1)


class Certainty(StrictModel):
    extraction: CertaintyLevel = CertaintyLevel.UNASSESSED
    interpretation: CertaintyLevel = CertaintyLevel.UNASSESSED
    explanation: str | None = None


class CodedValue(StrictModel):
    type: Literal["coded"]
    code: str
    original_wording: str | None = None


class GleasonPatternsValue(StrictModel):
    type: Literal["gleason_patterns"]
    primary_pattern: int = Field(ge=1, le=5)
    secondary_pattern: int = Field(ge=1, le=5)
    original_wording: str


class GleasonScoreValue(StrictModel):
    type: Literal["gleason_score"]
    primary_pattern: int = Field(ge=1, le=5)
    secondary_pattern: int = Field(ge=1, le=5)
    total: int = Field(ge=2, le=10)
    original_wording: str

    @model_validator(mode="after")
    def total_matches_patterns(self) -> GleasonScoreValue:
        if self.total != self.primary_pattern + self.secondary_pattern:
            raise ValueError("Gleason total must equal the two stated patterns")
        return self


class ClassificationValue(StrictModel):
    type: Literal["classification"]
    original_code: str
    classification_system: str | None = None
    edition: str | None = None
    normalized_code: str | None = None


class Measurement(StrictModel):
    value: float = Field(gt=0)
    unit: str
    axis: str | None = None
    approximate: bool = False


class DimensionsValue(StrictModel):
    type: Literal["dimensions"]
    measurements: tuple[Measurement, ...] = Field(min_length=1)
    original_wording: str


class LocationValue(StrictModel):
    type: Literal["location"]
    description: str
    original_wording: str


class PresenceValue(StrictModel):
    type: Literal["presence"]
    value: Literal["present", "absent", "indeterminate"]
    original_wording: str


ObservationValue = Annotated[
    Union[
        CodedValue,
        GleasonPatternsValue,
        GleasonScoreValue,
        ClassificationValue,
        DimensionsValue,
        LocationValue,
        PresenceValue,
    ],
    Field(discriminator="type"),
]

PROPERTY_VALUE_TYPES: dict[ObservationProperty, set[str]] = {
    ObservationProperty.GLEASON_PATTERNS: {"gleason_patterns"},
    ObservationProperty.GLEASON_SCORE: {"gleason_score"},
    ObservationProperty.GRADE_GROUP: {"coded"},
    ObservationProperty.CLASSIFICATION_PT: {"classification"},
    ObservationProperty.CLASSIFICATION_L: {"classification"},
    ObservationProperty.CLASSIFICATION_V: {"classification"},
    ObservationProperty.CLASSIFICATION_R: {"classification"},
    ObservationProperty.DIMENSIONS: {"dimensions"},
    ObservationProperty.TEXTUAL_LOCATION: {"location"},
    ObservationProperty.PRESENCE: {"presence"},
}


class Observation(StrictModel):
    id: str
    subject_id: str
    property: ObservationProperty
    status: AvailabilityStatus
    basis: PrototypeBasis
    value: ObservationValue | None = None
    evidence_ids: tuple[str, ...] = ()
    derived_from: tuple[str, ...] = ()
    review_status: Literal["unreviewed"] = "unreviewed"
    certainty: Certainty = Certainty()
    unavailable_reason: str | None = None

    @model_validator(mode="after")
    def enforce_value_and_scope(self) -> Observation:
        if self.derived_from:
            raise ValueError("derived observations are outside this prototype")
        if self.status == AvailabilityStatus.RECORDED:
            if self.value is None:
                raise ValueError("recorded observations require a value")
            if not self.evidence_ids:
                raise ValueError("recorded observations require direct evidence")
            if self.value.type not in PROPERTY_VALUE_TYPES[self.property]:
                raise ValueError("value type does not match the observation property")
        elif self.value is not None:
            raise ValueError("unavailable observations cannot contain a value")
        if self.status == AvailabilityStatus.NOT_REPORTED and (
            self.evidence_ids or not self.unavailable_reason
        ):
            raise ValueError(
                "not reported requires a coverage-backed reason, not a quotation"
            )
        if self.status in {
            AvailabilityStatus.UNREADABLE,
            AvailabilityStatus.NOT_ASSESSED,
            AvailabilityStatus.NOT_APPLICABLE,
        } and (not self.evidence_ids or not self.unavailable_reason):
            raise ValueError(
                "this unavailable status requires source evidence and a reason"
            )
        return self


class CoverageCheck(StrictModel):
    id: str
    subject_id: str
    property: ObservationProperty
    checked: bool
    source_complete: bool
    rationale: str


class ExtractionIssue(StrictModel):
    id: str
    kind: Literal["unresolved_attribution"]
    summary: str
    evidence_ids: tuple[str, ...] = Field(min_length=1)
    alternative_subject_ids: tuple[str, ...] = Field(min_length=1)


class ExtractionProposal(StrictModel):
    source_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    evidence: tuple[Evidence, ...]
    subjects: tuple[Subject, ...]
    coverage: tuple[CoverageCheck, ...]
    observations: tuple[Observation, ...]
    issues: tuple[ExtractionIssue, ...]
