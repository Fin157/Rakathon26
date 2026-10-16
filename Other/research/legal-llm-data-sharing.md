# Pseudonymised health data and external LLMs

## Recommendation

**Do not send real reports, drawings or extracted patient text to an external
LLM merely because the Rakathon ID has been masked.** Keep real cases local
until the hospital/data controller has approved the specific purpose, recipient,
contract, security measures and international-transfer arrangements. Use
synthetic cases for external development in the meantime.

Pseudonymisation can be an appropriate safeguard within a lawful processing
arrangement. It is not a legal basis, an exemption for hackathons or a certificate
of anonymity. There is no general GDPR ban on using an external LLM for health
data, but there is no blanket permission either.

Assessment date: **2026-10-16**. This is a technical decision aid for the
institution's data protection officer (DPO) and legal team, not a legal opinion.
No patient data was submitted to research services for this assessment.

## What the current preprocessing does

The component reads printed Rakathon IDs locally, proposes report/drawing pairs
and masks recognised ID regions with opaque pixels. A separate private JSON
dictionary retains original IDs, random case IDs, source references and evidence.
Original scans remain unchanged. The MVP exports two JPGs per random case ID and
a manifest; there is no external LLM integration or automatic upload.

This does not establish that IDs are the only identifying information. Other
text, dates, annotations, identifiers embedded in filenames, unusual clinical
details or combinations of facts could permit linkage. OCR may also miss an ID.
The actual dataset's origin, prior de-identification and sharing permissions
have not been legally verified here. The project name on an ID does not establish
that the underlying case is synthetic or anonymous.

The private browser comparison page is a visual aid, not an approval record or
proof of professional authority, patient consent or institutional permission.
Local export of clean pairs is separate from authorising external disclosure.

## Pseudonymisation versus anonymity

GDPR Article 4(5) defines pseudonymisation around separately protected additional
information needed to attribute data to someone. Recital 26 distinguishes this
from anonymous information by considering the means reasonably likely to be
used to identify a person, including available technology, cost and time.

Here the institution's retained mapping and clinical records mean it must
continue to treat its linkable case data as personal data. Masking an identifier
and dropping metadata do not, alone, demonstrate anonymisation of a medical
narrative or drawing. Even genuine anonymisation is itself processing that needs
to be lawful while the source data remains personal.

There is an important qualification: in **C-413/23 P, EDPS v SRB (2025)**, the
CJEU explained that pseudonymised information is not necessarily personal data
for every recipient in every circumstance. Recipient identifiability requires
a contextual assessment; it cannot be decided just from the existence of a key
elsewhere. The case concerned Regulation (EU) 2018/1725 and also preserved the
original controller's relevant transparency obligations. It is not a blanket
exemption for sending pseudonymised clinical scans to a model provider.

Do not infer recipient anonymity solely from withholding our mapping: the report
content and other realistically accessible information matter too. Any reliance
on that distinction needs an institution-approved, recipient-specific assessment.
Our engineering default is to handle the full workflow as personal health data.

## Conditions to assess before using an external provider

| Question | Required institutional assessment |
| --- | --- |
| Who is responsible? | Identify the controller, authorised users, processors/subprocessors and any separate or joint-controller purposes. A collaborator's personal account is not institutional authorisation. |
| Why is it processed? | Define whether this is patient care, registry administration, research or hackathon development. Assess purpose compatibility; a care basis does not automatically authorise development or vendor training. |
| What permits it? | Document an Article 6 lawful basis **and** an applicable Article 9(2) condition for health data, including any professional-secrecy and national-law requirements. Legitimate interests alone do not lift Article 9's prohibition. |
| Is consent necessary? | Explicit consent may be one route, not the only route and not an automatic solution. Care/research exceptions have their own conditions. Neither ordinary treatment consent nor an engineer's permission can be assumed to cover disclosure or provider training. |
| Is confidentiality preserved? | Assess Czech medical confidentiality, including Section 51 of Act No. 372/2011 Coll., access/disclosure rules and applicable institutional policies. GDPR compliance alone does not settle every confidentiality obligation. |
| What is the provider's role? | If acting as a processor, require Article 28 terms, documented instructions, confidentiality, approved subprocessors, deletion/return, assistance and audit provisions. A provider's own-purpose reuse needs separate role and lawful-basis analysis. |
| What leaves the hospital? | Minimise inputs; exclude original IDs, mappings, local paths, source metadata and unnecessary clinical context. Keep outputs and logs within the same protection/retention assessment. Redaction quality must be measured. |
| What does the provider retain? | Verify the exact API/product/account contract: prompt/image/output retention, abuse-monitoring logs, human access, deletion, backups and training/reuse. "No training" does not mean zero retention or no processing. |
| Where can data be accessed? | Document hosting, support access and subprocessors. EU hosting does not settle every transfer issue. Where Chapter V applies, verify a valid mechanism, its scope and any required transfer assessment/supplementary measures. |
| Is risk assessed? | Assess Article 35 DPIA triggers before processing; a DPIA is mandatory where processing is likely to result in high risk, including specified large-scale special-category processing. Not every small test automatically triggers it. Consult the DPO; unresolved high residual risk may require Article 36 consultation. |
| Are safeguards operational? | Cover Articles 25/32: access controls, encryption, separate keys/mappings, retention, deletion, incident response and controlled logging. Maintain appropriate transparency, rights handling and processing records. |

For the initial integration, choose a service arrangement that contractually
excludes provider training and other independent reuse of our clinical inputs.
That is our recommended procurement constraint, not a claim that GDPR always
requires consent for all AI training. Any different arrangement would require
separate institutional analysis of purposes, roles, Article 6 and Article 9.

The EDPB's Opinion 28/2024 addresses AI-model anonymity and lawful processing in
development/deployment. Its model-anonymity test is not a certification that an
individual redacted prompt or image is anonymous. Nor does its discussion of
legitimate interests replace Article 9 requirements for health data.

## Practical release decision

1. **Now:** keep real cases local. The supplied artificial hackathon data is
   separately authorised for sharing, as recorded in `TASK.md`. Do not treat
   local review as authorisation for uploading production records.
2. **Before any real external test:** obtain written institutional confirmation
   of the purpose, legal basis/health-data condition, confidentiality route,
   authorised dataset and exact approved provider/product/configuration.
3. **Before enabling it in software:** document the contract, retention,
   subprocessors/transfers, risk assessment and tested data-minimisation controls.
   Keep local export and external transmission as distinct operations.
4. **For the interface:** make originals/redacted views and pairing evidence
   inspectable. Show exception reasons. State that "ID masked" or "reviewed"
   does not mean "anonymous" or "legally authorised for upload."
5. **Repository hygiene:** development scans are currently Git-tracked. Do not
   assume ignore rules make them private. The owner/institution should assess
   repository access/history, removal and any incident obligations. No history
   rewriting or patient-file changes were performed for this assessment.

## Unknowns that prevent a project-specific legal yes

- The user has confirmed that the supplied hackathon cases are fully anonymised
  and unrestricted, as recorded in `TASK.md`. This note does not independently
  verify that assessment or extend it to production records.
- The controller's mandate, patient information, applicable legal bases and
  confidentiality arrangements.
- Which LLM provider, product, region, contract and retention settings would be
  used, and which subprocessors/support staff could access the data.
- The actual residual identifiability and measured masking failure rate.
- Whether additional research, ethics, medical-device or AI Act requirements
  apply to a later intended use. This preprocessing note is not that assessment.

## Dated primary sources

Sources checked/referenced on **2026-10-16**. Recheck current law and the selected
provider's actual contractual terms before deployment.

1. **EU GDPR, Regulation (EU) 2016/679, 27 April 2016.**
   [Official EUR-Lex text](https://eur-lex.europa.eu/eli/reg/2016/679/oj):
   Recital 26; Articles 4(5), 5, 6, 9, 13-14, 25, 28, 30, 32, 35-36 and 44-49.
   Direct EUR-Lex fetching was unavailable during this check; the official
   legal-text reference was also located through web search.
2. **CJEU, EDPS v SRB, C-413/23 P, 4 September 2025.**
   [Judgment reference](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023CJ0413)
   and [Court press release 107/25](https://curia.europa.eu/site/upload/docs/application/pdf/2025-09/cp250107en.pdf).
   The recipient-specific qualification was checked against the Court's indexed
   press-release summary; the full judgment was not readable through the fetcher.
3. **EDPB, Opinion 28/2024, 17 December 2024; announcement 18 December 2024.**
   [Opinion landing page](https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en)
   and [official explanation](https://www.edpb.europa.eu/news/edpb-opinion-on-ai-models-gdpr-principles-support-responsible-ai_en).
   The explanation was retrieved and read. It describes case-specific model
   anonymity and the legal-basis analysis; it does not approve our use case.
4. **Czech Act No. 372/2011 Coll., on Health Services, 6 November 2011.**
   [Official e-Sbirka entry](https://e-sbirka.gov.cz/sb/2011/372), notably Section 51.
   The entry was reachable but its legislative text was not exposed by the
   fetcher. Have institutional counsel verify the applicable current provisions
   and exceptions; no particular disclosure exception is asserted here.
5. **EDPB, Data protection basics, undated guidance, accessed 16 October 2026.**
   [Official guidance](https://www.edpb.europa.eu/sme/learn-the-basics/data-protection-basics_en):
   purpose limitation, data minimisation, retention and security. Retrieved and read.
