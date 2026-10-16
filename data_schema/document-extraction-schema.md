# Document extraction data schema

## Purpose

This conceptual schema describes information extracted from **one document at a time**, such as a pathology report or an annotated diagram.

- **Subjects** are the things described or depicted.
- **Observations** record what information is available or unavailable about those subjects.
- **Evidence** anchors observations to the original text or image.
- **Views** describe individual diagram panels and their spatial context.

Cross-document matching and reconciliation happen later. A tumour described in a report and a mark in a diagram remain separate subjects during extraction.

This document defines concepts and relationships, not database tables. Keys and identifiers are intentionally omitted.

## Document

The original source material, retained unchanged for inspection.

| Attribute | Description |
| --- | --- |
| Kind | Text report, diagram, or mixed document. |
| Language | Language or languages used. |
| Original source | Reference to the original file or scan. |

## Extraction

One attempt to interpret a document. Multiple extractions may exist after software updates or review.

| Attribute | Description |
| --- | --- |
| Timestamp | When extraction was performed. |
| Extractor version | Software, model, or manual process and its version. |
| Schema version | Version of this schema used. |

Subjects, observations, evidence anchors, and views belong to a particular extraction. Results from separate attempts must not be silently mixed.

## Subject

Something described or depicted in a document.

| Attribute | Description |
| --- | --- |
| Kind | Specimen, tumour focus, other finding, tissue sample, diagram mark, or diagram view. |
| Label | Original label or extractor-assigned description. |
| Identification basis | Explicit in the source or proposed by the extractor. |

Subjects may contain other subjects. For example, a prostate specimen may contain several reported tumour foci.

A **diagram view is a specialized subject** so that its interpreted attributes, such as orientation, can have observations, evidence, and uncertainty.

A diagram mark is not automatically a tumour. Separate marks initially remain separate subjects even if they might represent multiple depictions of one lesion.

## Observation

One statement about one property of one subject.

| Attribute | Description |
| --- | --- |
| Property | Characteristic being described, such as laterality, dimensions, grade, or margin status. |
| Status | Recorded, not reported, unreadable, not assessed, or not applicable. |
| Basis | Explicit, normalized, inferred, or calculated. |
| Review status | Unreviewed, accepted, needs review, or rejected. |

An observation has at most one typed value. Observations describing unavailable information have no value.

### Status

| Status | Meaning |
| --- | --- |
| Recorded | A value was extracted or derived. This includes explicit negative findings. |
| Not reported | The document was checked for this property but does not state it. |
| Unreadable | Relevant source content exists but cannot be read reliably. |
| Not assessed | The source explicitly indicates that the characteristic was not assessed. |
| Not applicable | The property does not apply; retain the reason or supporting evidence. |

The absence of an observation record does not mean that a property was checked and found unreported.

### Basis

| Basis | Meaning |
| --- | --- |
| Explicit | Directly transcribed from the source. |
| Normalized | Standardized without intentionally adding meaning. |
| Inferred | An interpretation not directly stated in the source. |
| Calculated | Computed from other observations. |

Inferred and calculated observations retain their supporting observations where applicable. Recorded values must be traceable to source evidence, directly or through their derivations.

## Value

Typed content attached to an observation.

| Type | Content |
| --- | --- |
| Coded | Controlled term and original wording where available. |
| Quantity | Number and unit, with optional approximation or range. |
| Dimensions | Ordered measurements, units, and anatomical axes when known. |
| Percentage | Percentage, approximation or range, and denominator or tissue scope. |
| Location | Laterality, anatomical level, zone, sector, or extent; unknown components are allowed. |
| Presence | Present, absent, or indeterminate. |
| Classification | Coding system, edition, original code, and optional normalized code. |
| Geometry | Point, polyline, polygon, or mask with an explicit coordinate frame. |
| Text | Descriptive content not represented by another type. |

Preserve original wording when normalization might hide ambiguity. Do not invent anatomical axes for dimensions or a denominator for percentages.

## Certainty

Uncertainty associated with an observation.

| Attribute | Description |
| --- | --- |
| Extraction certainty | Confidence that the source was read or captured correctly. |
| Interpretation certainty | Confidence that its meaning was interpreted correctly. |
| Explanation | Reason for uncertainty or review. |

Use `unassessed`, `high`, `medium`, or `low` initially. These are qualitative assessments, not calibrated probabilities of clinical truth.

## Evidence

An anchor into the original document that allows a reviewer to inspect the support for a subject or observation.

| Attribute | Description |
| --- | --- |
| Medium | Text or image. |
| Page | Source page. |
| Original quotation | Original-language text, when applicable. |
| Text offsets | Position in a specified extracted text layer, when available. |
| Image region | Bounding box, polygon, or other region, when available. |
| Coordinate convention | Origin, units, and axis directions for image regions. |

One evidence region may support several observations. One observation may need several evidence regions.

A `not reported` observation does not require a quotation explicitly stating the omission; it records the extraction's assessment of document coverage.

## Diagram view

A distinct panel, such as a base, mid, or apex cross-section. A view is both a spatial context and a specialized subject.

| Attribute | Description |
| --- | --- |
| Panel label | Visible label or extractor-assigned description. |
| View type | Cross-sectional, longitudinal, schematic, or unknown. |
| Anatomical level | Base, mid, apex, unspecified, or another supported level. |
| Panel region | Location of the panel on the page. |
| Coordinate convention | How positions within the panel are expressed. |

Interpreted attributes, including anatomical level and orientation, require supporting observations and evidence rather than being unquestioned metadata.

Distinguish:

1. **Page position:** where the panel or mark appears in the document.
2. **Anatomical position:** where a mark is interpreted to lie within the organ.

Image coordinates are not physical measurements. Image-left is not automatically patient-right.

## Relationships and cardinality

Minimum counts allow incomplete extractions. Cardinalities are expressed in words rather than arrow styles.

| Relationship | Cardinality |
| --- | --- |
| Document has extractions | One document has zero or more extractions; each extraction concerns exactly one document. |
| Extraction identifies subjects | One extraction has zero or more subjects; each subject belongs to exactly one extraction. |
| Extraction produces observations | One extraction has zero or more observations; each observation belongs to exactly one extraction. |
| Extraction captures evidence | One extraction has zero or more evidence anchors; each anchor belongs to exactly one extraction. |
| Extraction identifies views | One extraction has zero or more views; each view belongs to exactly one extraction as a subject. |
| Subject contains subjects | A subject has zero or more children; a child has at most one parent in this containment hierarchy. |
| Subject has observations | A subject has zero or more observations; each observation describes exactly one subject. |
| Subject is identified using evidence | Each subject has one or more evidence anchors; an anchor may identify zero or more subjects. |
| Observation records a value | An observation has zero or one value; each value belongs to exactly one observation. |
| Observation has certainty | Each observation has exactly one certainty assessment, which may be unassessed. |
| Observation is supported by evidence | An observation has zero or more direct evidence anchors; each anchor may support zero or more observations. |
| Observation derives from observations | An observation may derive from zero or more other observations and support zero or more derived observations. |
| View provides evidence context | A view provides context for zero or more evidence anchors; an anchor has at most one immediate view context. |
| Geometry uses view coordinates | A geometry value may use one view's coordinate frame; a view may be referenced by many geometry values. Page-based geometry instead declares its page coordinate frame. |

## Example property catalogue

These are candidate properties, not mandatory fields on every subject.

| Category | Example properties |
| --- | --- |
| Specimen | Organ, procedure, dimensions, weight. |
| Lesion identity | Reported label, dominant status, reported lesion count. |
| Location | Laterality, apex/mid/base, zone, sector, longitudinal extent. |
| Size | Dimensions, diameter, maximum dimension, approximation. |
| Histology | Tumour type, invasive status, described architecture. |
| Grade | Gleason patterns, total score, Grade Group, pattern percentages. |
| Extent | Percentage involved and its denominator. |
| Invasion and extension | Separately reported invasion or extension findings. |
| Margins | Overall status, site-specific status, involved length if stated. |
| Other findings | Finding type, location, description. |
| Classification | Code, system, edition, original wording. |
| Tissue samples | Block labels and anatomical descriptions. |
| Diagram marks | Colour, style, geometry, handwriting, proposed meaning. |
| Diagram views | Panel type, anatomical level, orientation, calibration status. |

## Interpretation rules

1. **Absent is not missing.** An explicit negative is a recorded presence value of `absent`. An unmentioned property uses `not reported` with no value.
2. **Keep scope attached.** A specimen-level statement must not silently become a lesion-level statement. Percentages retain their denominator.
3. **Separate appearance from meaning.** Visible mark geometry and its proposed anatomical meaning are separate observations.
4. **Separate page and anatomical positions.** Orientation must be supported rather than assumed.
5. **Do not invent physical scale.** Schematic pixels are not millimetres without supported calibration. Handwritten dimensions do not automatically calibrate a drawing.
6. **Preserve conflicts.** Different source statements remain separate observations rather than overwriting each other.
7. **Keep derivations traceable.** Retain supporting observations and evidence. Derivation chains must not contain cycles.
8. **Keep extraction attempts separate.** Review or re-extraction must not silently mix results from different attempts.
9. **Keep documents independent.** Matching subjects between documents and resolving disagreement belong to later processing.

## Worked examples

These examples illustrate extraction structure, not independently verified clinical interpretation.

### Text report

| Component | Example |
| --- | --- |
| Subject | Dominant tumour focus described in the report. |
| Observation property | Tumour dimensions. |
| Value | Approximately 11 × 15 × 8 mm; anatomical axes unspecified. |
| Status | Recorded. |
| Basis | Normalized from the original wording. |
| Evidence | Original quotation containing the dimensions and its page location. |
| Certainty | Extraction and interpretation assessed separately; initially unassessed. |

### Diagram

| Component | Example |
| --- | --- |
| Subject | Pink outline in the base panel. |
| Observation property | Anatomical sector. |
| Value | Proposed posterolateral peripheral region, labelled `PZpl`. |
| Status | Recorded. |
| Basis | Inferred from the mark's position relative to printed labels and boundaries. |
| Evidence | Image region containing the outline, label, and sector boundaries. |
| View | Base cross-section. |
| Certainty | Initially unassessed; visible geometry and anatomical interpretation may have different certainty. |

The visible outline geometry is stored as another observation, separate from its anatomical interpretation.

At the end of extraction, the report focus and diagram mark remain separate subjects. A later matching step may propose that they describe the same lesion without changing the original observations.
