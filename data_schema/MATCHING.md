# Subject matching and comparison data schema

## Purpose

This conceptual schema describes **step 3: matching and checking** the document-local extractions defined in `STRUCTURE.md`.

The pipeline is:

**Original documents → document-local extraction → matching and checking → combined record.**

- **Matching attempts** specify which extraction results are being considered together.
- **Document pairings** assess whether documents concern the same specimen or episode.
- **Matching hypotheses** propose which subjects describe or depict the same underlying finding.
- **Memberships** explain why individual subjects belong to a hypothesis.
- **Comparisons** assess whether particular observations agree, conflict, or cannot be compared.
- **Review questions** expose unresolved decisions and alternatives.

Matching can connect subjects across documents and marks across views within one document. A tumour may be depicted in several panels; several marks do not automatically mean several tumours.

This document defines concepts and relationships, not database tables. Keys and identifiers are intentionally omitted.

## Boundary with extraction and reconciliation

Inputs are the subjects, observations, evidence anchors, and views from specific extraction attempts. Their meanings and availability statuses remain as defined in `STRUCTURE.md`.

Matching does not merge subjects, overwrite observations, or move them between extractions. Its results form a separate layer referencing the original extraction results.

Two questions must remain distinct:

1. **Identity:** could these subjects represent the same underlying finding?
2. **Compatibility:** if they do, how do their observations relate?

A plausible match may contain conflicting observations. Compatible observations alone do not establish identity.

Step 3 produces proposed or reviewed connections, comparisons, and unresolved questions. Selecting authoritative combined values, resolving clinical disagreements, and publishing a database record belong to **step 4: reconciliation**. Accepting a match does not accept every observation attached to its members.

## Matching attempt

One attempt to match a specified set of extraction results.

| Attribute | Description |
| --- | --- |
| Timestamp | When matching was performed. |
| Matcher version | Software, model, or manual process and its version. |
| Schema version | Version of this matching schema used. |
| Comparison rules version | Version of the comparison rules and normalization conventions used. |
| Scope | Documents, extractions, and subject kinds considered; any exclusions. |
| Coverage | What was examined and what remains unchecked or blocked. |
| Supersession explanation | Why this attempt replaces an earlier attempt, when applicable. |

Each input is a particular extraction attempt, not simply the latest results for a document. Normally select one extraction per document. If multiple attempts for the same document are deliberately included, explain their roles and do not treat them as independent source corroboration.

A re-extraction or change to matching assumptions requires a new matching attempt or an explicit recorded revision. Earlier results remain inspectable rather than being silently reused against changed inputs.

An attempt may be incomplete. No hypothesis for a subject does not by itself mean the subject was checked and found unmatched.

## Document pairing

An assessment that two documents concern the same specimen or episode and are eligible for cross-document matching.

| Attribute | Description |
| --- | --- |
| Proposed shared scope | The specimen or episode the documents are thought to concern. |
| Assessment | Supported, uncertain, or contradicted. |
| Basis | Source labels, supplied association, source metadata, or reviewer confirmation. |
| Explanation | Supporting and opposing reasons, including any missing identifiers. |
| Certainty | Qualitative pairing certainty. |
| Review status | Unreviewed, accepted, needs review, or rejected. |

Pairing retains supporting evidence or an explicit record of the supplied association or reviewer decision. Upload order alone is not sufficient evidence.

A hypothesis spanning documents references the relevant pairings. Supported pairings must connect all its documents before the cross-document match can be accepted. Uncertain pairings allow conditional proposals, not established identity. Contradicted or rejected pairings block acceptance until corrected or superseded with a reason.

Pairing documents does not establish that any particular subjects match. Within-document matching does not require a document pairing.

## Matching hypothesis

A proposal that two or more document-local subjects describe or depict **one underlying finding**.

| Attribute | Description |
| --- | --- |
| Label | A descriptive name, such as proposed dominant-focus group. |
| Proposed finding kind | Tumour focus, other finding, or unresolved; not automatically tumour. |
| Rationale | Why the subjects may refer to the same finding. |
| Opposing considerations | Conflicts, competing explanations, or missing information. |
| Assumptions | Conditions on which the proposal depends. |
| Review status | Unreviewed, accepted, needs review, or rejected. |

A hypothesis is not the final combined lesion object. It groups references to existing subjects without changing their original identities or observations.

A report focus may be grouped with marks from base, mid, apex, and longitudinal views. A hypothesis may also group marks within a single diagram without a report counterpart.

Subjects may participate in several competing hypotheses while matching is unresolved. Record which proposals are mutually exclusive and why. Do not automatically combine overlapping hypotheses or infer that all their members match transitively.

Accepted hypotheses within one attempt must be mutually consistent. If two accepted groups share a subject, explicitly resolve whether they are one group or whether the subject's scope needs correction. A mark suspected to depict several findings requires a review question or revised extraction, not silent assignment to multiple accepted single-finding groups.

## Hypothesis membership

The inclusion of one subject in one matching hypothesis.

| Attribute | Description |
| --- | --- |
| Role | Report description, diagram depiction, or another source-supported role. |
| Supporting observations | Observations that support including the subject. |
| Opposing observations | Observations that weaken or contradict its inclusion. |
| Rationale | Explanation of the proposed connection. |
| Assumptions | Required orientation, annotation meaning, pairing, or other conditions. |
| Review status | Unreviewed, accepted, needs review, or rejected. |

Each membership retains traceable support through observations, source evidence, or an explicit reviewer explanation. An observation may support several memberships and must not be counted as independent evidence each time it is reused.

A rejected membership remains part of the history but is not an active member. Each viable single-finding hypothesis needs at least two active members; rejected hypotheses may retain their original structure for inspection.

## Matching certainty

Uncertainty about identity, separate from certainty about reading or interpreting source content.

| Attribute | Description |
| --- | --- |
| Overall matching certainty | Confidence that the proposed active members describe one finding. |
| Membership certainty | Confidence in including a particular subject. |
| Explanation | Supporting reasons, limitations, and unresolved alternatives. |

Each hypothesis and membership has its own certainty assessment. Use `unassessed`, `high`, `medium`, or `low` initially. These are qualitative assessments, not calibrated probabilities of clinical truth.

Pairing certainty, extraction certainty, interpretation certainty, matching certainty, comparison outcomes, and human review status remain separate. High matching certainty does not resolve a conflict or imply reviewer acceptance.

## Comparison

One assessment of a specified property across source observations, under stated assumptions.

| Attribute | Description |
| --- | --- |
| Property | Laterality, sector, level, size, grade, or another characteristic being compared. |
| Subject scope | The subjects and anatomical or tissue scope being compared. |
| Input observations | The exact observations examined, including unavailable-status observations. |
| Rule | The comparison method and its version, including any tolerances. |
| Normalization | Unit conversions or terminology mappings used for comparison, without replacing the source values. |
| Assumptions | Required pairing, matching, orientation, scope, or measurement interpretations. |
| Outcome | Agreement, compatible detail, conflict, indeterminate, no counterpart, or not comparable. |
| Explanation | Why the outcome follows and what it does not establish. |
| Review status | Unreviewed, accepted, needs review, or rejected. |

A comparison belongs to a matching attempt and may apply to one hypothesis. Its conclusion remains conditional when that hypothesis or a required assumption is unresolved.

### Outcomes

| Outcome | Meaning |
| --- | --- |
| Agreement | Comparable observations express the same information within the stated rule. |
| Compatible detail | Information is consistent but differs in specificity or coverage; it is not full independent confirmation. |
| Conflict | Comparable observations make incompatible statements under the stated assumptions. |
| Indeterminate | Uncertainty or an unresolved prerequisite prevents a conclusion. |
| No counterpart | The property was checked for the relevant counterpart subject or source, but no corresponding recorded value is available. |
| Not comparable | The inputs do not describe comparable quantities, scopes, systems, or coordinate frames. |

A `no counterpart` result retains why information is unavailable: not reported, unreadable, not assessed, not applicable, or checked without a corresponding observation. It is not a negative finding. If coverage has not been checked, leave the comparison unperformed or record an indeterminate assessment explaining the gap.

### Comparison conditions

- **Location:** compare anatomical interpretations, not raw page positions. Retain level, side, zone, sector, and extent separately where needed.
- **Orientation:** unresolved patient-side mapping makes a laterality comparison indeterminate. Do not assume image-left means patient-right.
- **Size:** compare compatible measurements with retained units, approximation, ranges, and axes. A reported diameter is not automatically equivalent to each component of three-dimensional measurements.
- **Geometry:** unregistered views do not support meaningful spatial overlap. Schematic pixels are not physical measurements without supported calibration.
- **Percentages:** retain the denominator and tissue scope; differing denominators are not automatically comparable.
- **Grade and classifications:** preserve the system and edition. Any mapping must be explicit and versioned.
- **Missing information:** a diagram without a grade value does not contradict a report's grade.

No universal numeric tolerance or clinical equivalence rule is prescribed here. Any such rule must be defined, versioned, and explained before use.

## Assumptions and dependency tracking

Pairings, hypotheses, memberships, and comparisons retain the source observations and decisions on which they depend.

For example, a comparison may depend on an orientation observation about a diagram view. If that orientation is rejected or superseded, the dependent comparison requires reassessment; it must not remain silently accepted.

A cross-source inference belongs to this matching layer, not retrospectively to the original document extraction. If the report is used to assign otherwise unknown diagram laterality, that assignment must not then count as independent diagram evidence confirming the report's laterality.

Dependencies must not contain cycles. Evidence reused through several derivations remains the same evidence, not additional corroboration.

## Review question

An unresolved decision needed to assess pairing, identity, compatibility, or matching coverage.

| Attribute | Description |
| --- | --- |
| Topic | Pairing, mark meaning, grouping, orientation, conflicting property, unmatched subject, or another issue. |
| Question | The decision a reviewer needs to make. |
| Context | Relevant subjects, observations, evidence, pairings, hypotheses, memberships, or comparisons. |
| Alternatives | Competing explanations or proposed actions, including leaving the matter unresolved. |
| Impact | What cannot be accepted or compared until this is addressed. |
| Status | Open, resolved, or deferred. |
| Decision record | Reviewer, timestamp, decision, and explanation when addressed. |

Resolving a question records what was decided and why; it does not delete opposing source observations. Deferral preserves uncertainty. A decision that changes extraction content requires a traceable extraction correction and reassessment of affected matching results.

A subject may legitimately remain unmatched: there may be no counterpart, the source may depict a non-tumour finding, or the evidence may be insufficient. Record the assessment when checked; do not force every subject into a group.

## Relationships and cardinality

Minimum counts allow incomplete matching attempts. Cardinalities are expressed in words rather than arrow styles.

| Relationship | Cardinality |
| --- | --- |
| Matching attempt uses extractions | Each attempt uses one or more specified extractions; an extraction may be used by zero or more attempts. |
| Matching attempt assesses pairings | One attempt has zero or more document pairings; each pairing belongs to exactly one attempt. |
| Pairing relates documents | Each pairing relates exactly two distinct documents represented in the attempt; a document may participate in zero or more pairings. |
| Matching attempt proposes hypotheses | One attempt has zero or more hypotheses; each hypothesis belongs to exactly one attempt. |
| Hypothesis uses pairings | A hypothesis references zero or more pairings from its attempt; a pairing may support zero or more hypotheses. Cross-document hypotheses require connecting pairings. |
| Hypothesis has memberships | Each hypothesis records two or more memberships; each membership belongs to exactly one hypothesis. Viable hypotheses require at least two active members. |
| Membership includes subject | Each membership references exactly one subject from an input extraction; a subject may occur in zero or more hypotheses, at most once per hypothesis. |
| Hypothesis competes with hypothesis | A hypothesis may have zero or more competing hypotheses within the same attempt; each competing relationship records its reason and whether the proposals are mutually exclusive. |
| Hypothesis has matching certainty | Each hypothesis has exactly one matching certainty assessment, which may be unassessed. |
| Membership has matching certainty | Each membership has exactly one matching certainty assessment, which may be unassessed. |
| Matching attempt produces comparisons | One attempt has zero or more comparisons; each comparison belongs to exactly one attempt. |
| Hypothesis has comparisons | One hypothesis has zero or more comparisons; a comparison concerns zero or one hypothesis within its attempt. |
| Comparison examines observations | Each comparison references one or more input observations; an observation may be used by zero or more comparisons. Agreement, compatible detail, and conflict require comparable recorded inputs from at least two subjects. |
| Matching result uses source support | Each pairing, membership, or comparison may reference zero or more evidence anchors and observations; each anchor or observation may support zero or more matching results. An explicit rationale is always retained. |
| Matching attempt raises questions | One attempt has zero or more review questions; each question belongs to exactly one attempt. |
| Review question concerns matching context | Each question references one or more relevant source or matching components; a component may be referenced by zero or more questions. |
| Matching attempt supersedes attempt | An attempt supersedes zero or one earlier attempt; an earlier attempt may have zero or more successors. Supersession must not contain cycles. |

All referenced subjects, observations, views, and evidence must belong to the attempt's declared input extractions. Matching results and review decisions retain their own provenance without becoming document-local observations.

## Interpretation rules

1. **Establish document association.** Do not treat unrelated documents as a matched source set merely because they were supplied together.
2. **Keep source subjects intact.** A matching group references subjects; it does not merge, rename, or move them.
3. **Separate identity from compatibility.** A conflict does not automatically disprove identity, and agreement alone does not prove it.
4. **Allow repeated depictions.** One finding may have several marks across views. Do not infer lesion count from mark count.
5. **Allow alternatives and unmatched subjects.** Do not force a one-to-one assignment or silently combine competing groups.
6. **Keep meaning and appearance separate.** Similar ink colour or shape alone does not establish tumour meaning or identity.
7. **Preserve scope and comparability.** Respect anatomical level, measurement context, coordinate frame, percentage denominator, and classification edition.
8. **Missing is not disagreement.** Unavailable information and unchecked coverage must remain distinguishable from explicit negative findings.
9. **Expose assumptions.** Conditional matches and comparisons remain conditional until their prerequisites are supported and reviewed.
10. **Avoid circular confirmation.** A value inferred from another source is not independent corroboration of that source.
11. **Keep support and revisions traceable.** Record inputs, methods, reasons, decisions, and dependencies; reassess results when their inputs change.
12. **Do not reconcile prematurely.** Matching acceptance does not choose authoritative property values or remove source conflicts.

## Worked examples

These examples illustrate matching structure, not independently verified clinical interpretation or completed matching of the sample scans.

### One report focus and several diagram marks

| Component | Example |
| --- | --- |
| Inputs | One report extraction and one diagram extraction, with supported document pairing. |
| Report subject | Dominant tumour focus described in a posterolateral peripheral region. |
| Diagram subjects | Separate marks in the base, mid, and apex panels. |
| Hypothesis | The report focus and these three marks represent one underlying finding. |
| Membership support | Location observations, view-level observations, relevant source text, and image regions. |
| Location comparison | Compatible detail, conditional on supported sector interpretation and orientation where laterality is involved. |
| Matching certainty | Initially unassessed; accepting compatible location does not itself confirm identity. |
| Review question | Do all three marks depict this focus, or should one belong to another group? |

The four source subjects remain separate. Grouping them does not create four tumours or finalize a combined lesion record.

### A plausible match with a conflict

| Component | Example |
| --- | --- |
| Hypothesis | A report focus and a diagram mark may describe the same finding. |
| Compared observations | The report says anterior; the diagram interpretation says posterior. |
| Preconditions | Shared specimen, relevant view orientation, and comparable anatomical scope are supported. |
| Outcome | Conflict. |
| Review question | Is the disagreement in the source material, its extraction, the diagram interpretation, or the proposed match? |
| Retained result | Both observations, their evidence, the matching proposal, and the unresolved conflict. |

The matcher does not silently choose a source or reject the match simply to remove the disagreement.

### Missing or non-comparable information

| Situation | Comparison result |
| --- | --- |
| The report supplies grade; the diagram was checked and supplies no grade value. | No counterpart, with the diagram's unavailable-information assessment retained. |
| The report supplies dimensions in millimetres; the diagram supplies only uncalibrated outline geometry. | Not comparable for physical size. |
| The report supplies laterality; diagram orientation is unresolved. | Indeterminate for laterality. |
| The diagram side is assigned using the report's laterality. | Retain the conditional cross-source assignment; do not report independent laterality agreement. |

At the end of step 3, the output is a traceable set of matching hypotheses, comparison outcomes, alternatives, and review questions. A later reconciliation step can use these results to construct a reviewed combined record without altering what each original source said.
