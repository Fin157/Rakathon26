# Combined interpretation and assessment data schema

## Purpose

This conceptual schema describes **step 4: assessing our combined understanding** after the matching and comparisons described in `MATCHING.md`.

The pipeline is:

**Original documents → document-local extraction → matching and checking → combined interpretation and assessment.**

- **Assessment revisions** capture our interpretation of a specified set of extraction and matching results.
- **Finding interpretations** describe what we currently think the source subjects represent together.
- **Property assessments** describe what we conclude about each characteristic, with alternatives and limitations.
- **Support contributions** explain how particular observations support, oppose, or qualify a conclusion.
- **Certainty assessments** explain how strongly we hold that interpretation and why.
- **Review decisions** record human judgments without erasing the underlying evidence or disagreements.

This is our best current reading of the supplied documents, not an independently established clinical truth. It can remain incomplete, conditional, or conflicted.

This document defines concepts and relationships, not database tables. Keys and identifiers are intentionally omitted. Database mapping, registry fields, export formats, and publication requirements are outside its scope.

## Boundary with earlier steps

`STRUCTURE.md` records what each document says. `MATCHING.md` records which subjects might represent the same finding and how their observations compare. This step records **what we currently make of those results**.

For example:

- Extraction: the report describes a focus; the diagram contains several marks.
- Matching: the focus and those marks may describe one finding, with compatible location observations.
- Assessment: we provisionally interpret them as one finding, accept some characteristics, and leave other characteristics unresolved.

This assessment does not merge or alter document-local subjects. It references matching hypotheses, comparisons, observations, and their evidence. It does not silently change a matching decision either: a revised grouping is returned to step 3 and referenced in a subsequent assessment revision.

The earlier document's description of step 4 as reconciliation or a combined record means a **reviewable combined interpretation here**, not an export-ready record. Deciding to retain uncertainty is a valid result; resolving every disagreement is not required.

## Assessment revision

One recorded interpretation of specified inputs at a particular time.

| Attribute | Description |
| --- | --- |
| Timestamp | When the assessment was made. |
| Assessor and version | Software, model, or person responsible, including process version where applicable. |
| Schema version | Version of this assessment schema used. |
| Assessment method | Rules and conventions used, with versions where applicable. |
| Scope | Documents, specimen or episode, findings, and properties considered. |
| Coverage | What was assessed, what was excluded, and what remains unchecked. |
| Summary | Plain-language account of the current interpretation and its main limitations. |
| Review status | Unreviewed, accepted, needs review, or rejected. |
| Supersession explanation | Why this revision replaces an earlier one, when applicable. |

A revision references a specified matching attempt and the exact extraction inputs used by that attempt. It does not resolve references dynamically to the latest available results.

A changed extraction, pairing, grouping, orientation, comparison, or reviewer judgment may require a new revision. Earlier revisions remain inspectable. Acceptance applies to the stated interpretation and limitations; it does not mean that all properties are known or clinically proven.

## Finding interpretation

Our current interpretation of one possible underlying finding, or of a specimen-level or tissue-sample subject that must remain at its original scope.

| Attribute | Description |
| --- | --- |
| Label | Descriptive name for the interpretation. |
| Proposed kind | Tumour focus, other finding, specimen, tissue sample, or unresolved. |
| Identity disposition | Adopted, provisional, unresolved, or not adopted. |
| Rationale | Why this interpretation is being used or retained as an alternative. |
| Conditions | Required pairing, grouping, mark meaning, orientation, or other assumptions. |
| Review status | Unreviewed, accepted, needs review, or rejected. |

A finding interpretation references either one matching hypothesis or one unmatched source subject. A single-source finding remains eligible for assessment; absence of a counterpart does not invalidate it.

For a matched interpretation, the participating subjects are inherited from the specified hypothesis and memberships, not independently regrouped here. An uncertain document pairing makes cross-document conclusions conditional; a contradicted pairing cannot support an adopted cross-document interpretation.

Competing hypotheses remain separate interpretations with explicit alternative relationships. Mutually exclusive interpretations must not both be adopted in the same revision. Provisional alternatives must not be counted as separate established lesions.

Specimen-level findings remain specimen-level. A specimen margin observation, for example, is not silently copied to each lesion.

## Property assessment

Our current conclusion about one property of one finding interpretation.

| Attribute | Description |
| --- | --- |
| Property | Characteristic assessed, such as location, dimensions, grade, or extent. |
| Scope | Relevant anatomy, tissue, measurement context, or denominator. |
| Disposition | Adopted, provisional, unresolved, unavailable, or not applicable. |
| Proposed value | Zero or one typed value using the types in `STRUCTURE.md`. |
| Basis | Retained source value, normalized agreement, compatible synthesis, or reasoned selection or inference. |
| Rationale | Why this conclusion is held, including opposing information and limitations. |
| Conditions | Assumptions on which the conclusion depends. |
| Review status | Unreviewed, accepted, needs review, or rejected. |

### Disposition

| Disposition | Meaning |
| --- | --- |
| Adopted | The value is the interpretation currently used for this property, with its stated limitations. |
| Provisional | A value is proposed but important uncertainty or a prerequisite remains. |
| Unresolved | No single value is selected; competing candidates or insufficient support remain. |
| Unavailable | The property was assessed but no usable conclusion is available from the supplied material. |
| Not applicable | The property does not apply to this interpretation; retain the reason. |

Adopted and provisional assessments have exactly one proposed typed value. Unresolved, unavailable, and not-applicable assessments have no selected value; they can retain candidate interpretations separately.

These dispositions do not replace extraction availability statuses. An unavailable assessment retains whether its inputs were not reported, unreadable, not assessed, or unusable for another stated reason. No property assessment means only that no assessment is recorded, not that the property was checked.

A property assessment may be adopted by an automated process while still unreviewed. Human review status and the assessor's disposition are separate. Similarly, a reviewer may accept an unresolved assessment as an accurate representation of the evidence.

### Combining information

Compatible synthesis may combine complementary information only when the matching, scope, and assumptions support it. Every component remains attributable to its source.

For example, a report may supply dimensions while a diagram adds anatomical sector detail. This can enrich the interpretation without implying that the diagram independently confirms the dimensions.

Do not average conflicting measurements, take the union of contradictory locations, invent axes, or infer a physical scale merely to obtain one value. A more precise-looking value is not automatically better supported. There is no blanket rule that either text or diagram always wins.

## Candidate interpretation

An alternative value considered for one property assessment.

| Attribute | Description |
| --- | --- |
| Candidate value | One typed value, preserving its original scope and uncertainty. |
| Basis | Source-derived value or explicitly reasoned inference. |
| Rationale | Why the candidate is plausible and what argues against it. |
| Disposition | Preferred, possible, or not adopted. |
| Conditions | Assumptions required for this candidate. |

Candidates retain supporting and opposing inputs. A preferred candidate does not become an adopted value unless the property assessment explicitly selects it. An unresolved assessment may retain several candidates, or none when the evidence is too limited to propose a value.

## Support contribution

The role of an input in a finding interpretation, property assessment, or candidate interpretation.

| Attribute | Description |
| --- | --- |
| Input | A specified observation, evidence anchor, pairing, hypothesis, membership, comparison, or prior review decision. |
| Role | Supports, opposes, contextualizes, or establishes a prerequisite. |
| Explanation | How this input affects the conclusion. |
| Dependency | Other inputs or decisions required to use this contribution. |
| Independence limitation | Reused evidence, shared derivation, or cross-source inference that prevents independent corroboration. |

Each contribution has exactly one target interpretation or assessment and references one input. Multiple contributions express more complex reasoning. Proposed values and identity judgments require a traceable rationale and support; source-derived content must trace back to source evidence.

Opposing contributions are retained even when a value is selected. A reviewer decision can explain a choice but is not, by itself, new source evidence or independent verification.

Two observations are not independent merely because they occur in different panels, passages, extraction runs, or files. In particular, a diagram side inferred from the report cannot independently confirm that report's laterality.

## Certainty assessment

A qualitative account of how strongly we hold an interpretation and what limits it.

| Attribute | Description |
| --- | --- |
| Identity certainty | Confidence that the interpreted source subjects refer to one finding. |
| Property certainty | Confidence in the selected or proposed property conclusion. |
| Explanation | Why that level is appropriate, including contrary evidence. |
| Limiting factors | Extraction quality, interpretation ambiguity, pairing, matching, comparability, source dependence, or incomplete coverage. |

Finding interpretations have identity certainty. Property assessments and candidates have property certainty. Use `unassessed`, `high`, `medium`, or `low` initially; no calibrated probability is implied.

Retain the extraction and interpretation certainty from step 2, matching certainty from step 3, comparison outcomes, and reviewer decisions as separate inputs. Do not collapse them into one overall validity percentage or automatically increase certainty when sources agree.

A clearly read statement may still have uncertain meaning. A strong match may still contain an unresolved location conflict. A well-supported grade may have only one reporting source. Each situation should remain expressible without labelling the entire finding simply valid or invalid.

## Open issue and review decision

An unresolved question affecting our combined interpretation. Reuse relevant step 3 review questions by reference rather than silently resolving or duplicating them.

| Attribute | Description |
| --- | --- |
| Question | What needs to be clarified or decided. |
| Context | Affected interpretations, assessments, candidates, and source or matching inputs. |
| Alternatives | Plausible decisions, including retaining uncertainty. |
| Impact | Which conclusions remain conditional or require reassessment. |
| Status | Open, resolved, or deferred. |
| Decision record | Reviewer, timestamp, action, rationale, and affected conclusions when addressed. |

A decision may adopt a proposed value, retain competing candidates, reject an unsupported inference, request extraction correction, or return grouping to step 3. No decision may silently overwrite source observations or matching results.

Deferral is not resolution. Accepting an interpretation does not automatically close its issues. A recorded resolution must identify the decision and its scope; resolving one property's issue does not establish all other properties.

## Overall understanding

A revision's summary should explain:

- Which finding interpretations are adopted or provisional.
- Which interpretations are competing alternatives rather than additional findings.
- What each source contributes, and which properties lack corroboration.
- Which conflicts, assumptions, and missing information remain.
- What can be stated despite those limitations, and what cannot yet be concluded.

Lesion count is not mark count, hypothesis count, or interpretation count. A count may be assessed at specimen scope only with an explicit definition, coverage statement, and supporting grouping decisions. Where alternatives change the count, keep it conditional or unresolved rather than forcing an integer. A source-reported count remains distinguishable from a count inferred from the combined interpretation.

No overall validity score or database-readiness flag is required.

## Relationships and cardinality

Minimum counts allow incomplete assessments. Cardinalities are expressed in words rather than arrow styles.

| Relationship | Cardinality |
| --- | --- |
| Assessment revision uses matching attempt | Each revision references exactly one specified matching attempt; an attempt may support zero or more revisions. |
| Revision contains finding interpretations | One revision has zero or more finding interpretations; each interpretation belongs to exactly one revision. |
| Finding interpretation references source grouping | Each interpretation references exactly one matching hypothesis or exactly one unmatched subject from the attempt's inputs, not both. A hypothesis or subject may be referenced by zero or more revisions. |
| Finding interpretation has property assessments | One interpretation has zero or more property assessments; each assessment concerns exactly one interpretation. Within a revision, use at most one current assessment for the same property and scope of an interpretation. |
| Property assessment proposes value | One assessment has zero or one proposed value, subject to its disposition. |
| Property assessment considers candidates | One assessment has zero or more candidates; each candidate belongs to exactly one assessment and has exactly one typed candidate value. |
| Interpretation or assessment has support contributions | A finding interpretation, property assessment, or candidate has zero or more contributions; each contribution concerns exactly one target and references exactly one input. Non-empty conclusions require traceable support. |
| Finding interpretation has identity certainty | Each finding interpretation has exactly one identity certainty assessment, which may be unassessed. |
| Property assessment or candidate has property certainty | Each property assessment and candidate has exactly one property certainty assessment, which may be unassessed. |
| Interpretations are alternatives | An interpretation may have zero or more alternative interpretations within its revision; each relationship records the reason and whether the alternatives are mutually exclusive. |
| Revision tracks open issues | A revision has zero or more issues; each issue concerns one or more relevant assessment or input components and may reference zero or more step 3 review questions. |
| Issue has review decisions | An issue has zero or more decision records; each decision concerns exactly one issue and records its affected conclusions. |
| Revision supersedes revision | A revision supersedes zero or one earlier revision; an earlier revision may have zero or more successors. Supersession must not contain cycles. |

All source and matching references must resolve to the revision's declared input lineage. Decisions and conclusions retain their own provenance rather than becoming facts attributed to an original document.

## Interpretation rules

1. **Assess understanding, not database readiness.** The result is a reviewable interpretation with limitations, not an import record.
2. **Preserve all layers.** Source observations, matching results, and assessment judgments remain distinguishable and inspectable.
3. **Do not require a single answer.** Unresolved alternatives and unavailable properties are valid outcomes.
4. **Separate confidence from acceptance.** A disposition, qualitative certainty, and human review status answer different questions.
5. **Keep identity conditional where necessary.** Uncertain pairing or grouping limits conclusions that combine sources, not necessarily each source's individual statements.
6. **Assess properties individually.** A conflict about location does not automatically invalidate a source-supported size or grade.
7. **Retain counterevidence.** Selecting one interpretation does not erase an opposing observation or establish that it was extracted incorrectly.
8. **Do not invent precision or corroboration.** Complementary information is not independent confirmation; conflicting values are not averaged by default.
9. **Keep scope intact.** Preserve tissue denominator, anatomical level, axes, units, classification edition, and specimen-versus-lesion scope.
10. **Keep single-source findings visible.** Lack of a diagram counterpart is not evidence that a reported finding is absent.
11. **Record dependencies and changes.** When a prerequisite changes, reassess dependent conclusions in a traceable new revision. Derivation and decision dependencies must not contain cycles.
12. **Limit the claim.** This model assesses the supplied documents; it does not independently verify a patient's clinical state or recommend treatment.

## Worked examples

These examples illustrate assessment structure, not fresh extraction of the sample scans or independently verified clinical interpretation.

### Complementary sources, not universal confirmation

| Component | Example |
| --- | --- |
| Step 3 input | A report focus is provisionally matched to marks across several diagram panels. |
| Finding interpretation | One proposed tumour focus; identity remains conditional on that grouping. |
| Dimensions assessment | Approximately 11 × 15 × 8 mm, retained from the report; anatomical axes unspecified. |
| Dimensions support | Report observation and quotation. Uncalibrated diagram geometry does not independently confirm the size. |
| Location assessment | Provisional combined location using the report and supported panel-sector interpretations. |
| Certainty | Assessed separately for identity, dimensions, and location; initially unassessed unless explicitly evaluated. |
| Summary | The sources may describe one finding and contribute complementary information; not every property is corroborated. |

### A matched finding with unresolved location

| Component | Example |
| --- | --- |
| Step 3 input | Plausible identity match; comparable anterior and posterior location observations conflict. |
| Location disposition | Unresolved, with no selected location value. |
| Candidates | Anterior and posterior interpretations, each retaining its support and opposition. |
| Other properties | Reported grade or size may be assessed separately without treating the location conflict as resolved. |
| Review decision | Retain the conflict pending review, or select a reasoned interpretation without deleting the alternative. |
| Summary | A plausible single finding with unresolved location, not a uniformly invalid finding. |

### Single-source information and incomplete coverage

| Component | Example |
| --- | --- |
| Source situation | A report supplies grade; the diagram was checked and supplies no grade value. |
| Grade disposition | May be adopted from the report with explicit single-source support, subject to reading and interpretation certainty. |
| Cross-source assessment | No grade corroboration, but no grading disagreement either. |
| Separate diagram mark | Remains an unmatched interpretation if its relationship to reported findings is unclear. |
| Lesion count | Not increased merely because that mark remains unmatched; count may remain unresolved. |

At the end of step 4, we can explain **what we think the documents mean together, how strongly we hold each conclusion, what opposes it, and what remains undecided**. Preparing those conclusions for a database is a separate later task.
