# ProstaPaper production deployment and patient data

Sources checked on 2026-10-16. Scope: a future hospital deployment that converts paper pathology reports and drawings into draft REDCap fields, followed by doctor review. It uses an existing model for extraction. The user has confirmed that the current hackathon samples are fully anonymised and unrestricted; their use is not the question here.

## Recommendation

A hospital can in principle run this workflow on a rented EU server or use a proprietary model API. GDPR and the Czech healthcare provisions examined below do not impose a universal requirement for hospital-owned, on-premise hardware. The hospital must establish a lawful purpose, lawful access, processor arrangements, confidentiality, suitable security, and any necessary international-transfer safeguards. A particular hospital's security obligations or contracts can narrow its deployment choices.

For production, treat reports and patient-linked outputs as personal health data. Removing rodné číslo before inference reduces exposure but does not remove the hospital's GDPR obligations when it can reconnect the result to a patient. An API's zero-retention setting addresses retention, not authority to disclose or process the data.

My suggested architecture is local ingestion and redaction, a hospital-held mapping between random request IDs and patients, minimal text or image crops sent to an approved inference service, and local reassociation and doctor review before REDCap export. This is a design recommendation, not a statutory architecture or certification of any vendor.

## GDPR and the production workflow

The project drafts registry fields from Czech prostatectomy reports and annotated drawings. In production those records describe identified or identifiable patients. Health information receives special protection under Article 9. OCR, redaction, inference, temporary processing and storage are all processing when personal data are involved. [GDPR, Articles 4 and 9][gdpr]

Recital 26 excludes genuinely anonymous information. Identification depends on means reasonably likely to be used, including linkage to other information. For the hospital's patient-linked workflow, replacing identifiers while retaining a mapping is pseudonymisation. Review dates, accession numbers, barcodes and identifying free text as well as names and rodné číslo. These are proposed redaction checks, not findings about every sample. An OCR-only redaction does not remove information from an image uploaded separately. [GDPR, recital 26 and Article 4(5)][gdpr]; [ÚOOÚ healthcare Q&A, indirect identification][uoou-health]

Identifiability is contextual. The Court's official summary of C-413/23 P, decided under the parallel EU-institution regulation, explains that pseudonymised data are not necessarily personal for every recipient in every circumstance. It also explains that the controller's information obligations were assessed from its perspective before transfer. That distinction does not eliminate the hospital's obligations for a patient-linked production system. [Court of Justice official summary, 4 September 2025][court]

Personal health-data processing needs an Article 6 legal basis and an applicable Article 9 exception. Necessary healthcare or healthcare management can fall under Article 9(2)(h), subject to Article 9(3) secrecy safeguards. For this workflow, the hospital should establish that its basis for the existing registry entry also covers the extraction service and supplier arrangement. Automating transcription does not itself establish a new research purpose. Patient consent is not universally required for every healthcare IT operation. A processor contract does not itself provide the underlying legal basis. [GDPR][gdpr]

The hospital is normally controller for its own patient-record workflow. A supplier processing only under hospital instructions is normally a processor. The actual decisions about purposes and means determine those roles. The supplier's instructions should cover extraction and return of draft fields for the hospital's review. [European Commission, controller and processor roles][commission-roles]

## Czech healthcare law

Act 372/2011 Sb. applies alongside GDPR:

- Section 51(1) imposes medical confidentiality on the provider. Section 51(5) extends it to specified people, including authorised record accessors and others obtaining health information in activities under the relevant laws.
- Section 65 regulates who may access medical documentation and for what necessary purposes. A generic software-developer role does not itself establish access authority. The hospital must establish how its staff and contractors lawfully participate in the actual workflow.
- Section 55d requires written rules and appropriate technical and organisational measures for processing medical documentation.

These provisions do not prescribe an on-premise model. They also do not authorise every proposed disclosure to an API. [Official Act 372/2011 Sb., consolidated PDF][health-act]; see the companion [Czech statutory source note](czech_health_law_sources.md).

## Rented EU server

This is a legally possible option. The Czech supervisory authority expressly identifies cloud providers and external IT-system operators as typical processors. [ÚOOÚ processor Q&A][uoou-processor]

The hospital needs an Article 28 contract or other qualifying legal act for processing on its behalf. The processor must follow documented instructions; relevant personnel must be bound to confidentiality. Subprocessors require prior specific or general written controller authorisation and the required contractual obligations. [GDPR, Articles 28 and 29][gdpr]; [ÚOOÚ][uoou-processor]

Article 32 requires security appropriate to the risk. For this workload, assess access restrictions, encryption, isolation, patching, content-free operational logs, backups and recovery, retention and end-of-service handling. Those are practical measures to assess, not an exhaustive mandatory statutory checklist. A server's EU location alone does not establish who can access it or where backups and support operate. [GDPR, Article 32][gdpr]

## Proprietary model API and zero retention

The cited law has no general ban based on a model being closed source. Establish the provider's role and whether the actual agreement permits the intended health-data processing. Document purposes, confidentiality, subprocessors, security, retention and access locations. Include any gateway or intermediary in that assessment.

Zero retention is useful, but GDPR does not universally require it. Any retention must fit a justified purpose and applicable obligations. Processing occurs even if prompts disappear after the response. A zero-retention promise cannot replace the hospital's lawful basis or processor arrangements. [GDPR, Articles 4, 5, 9 and 28][gdpr]

Transfers outside the EEA need a Chapter V arrangement. Depending on the recipient and circumstances, this may be an applicable adequacy decision or Article 46 safeguards, such as standard contractual clauses with the necessary assessment and supplementary measures. Remote access by a separate overseas recipient can create a transfer even where the server is in the EU. [EDPB Opinion 22/2024, paragraphs 75 and 88 to 92][edpb-transfers]; [Commission adequacy decisions][adequacy]

OpenAI's official documentation says API content is not used for training by default. Ordinary abuse logs may retain content for up to 30 days, subject to stated exceptions. ZDR requires approval and has endpoint, feature and image exceptions. European residency needs additional arrangements and regional configuration; the listed Europe region includes the EEA and Switzerland. Its regional image-support footnote requires enhanced ZDR or enhanced Modified Abuse Monitoring approval. Verify the exact model, endpoint and account configuration. `store:false` alone does not establish ZDR. These are vendor terms, not legal permission. [Official OpenAI data controls][openai]

## What this means for the supplier

For a hospital-controlled deployment, process only within the agreed instructions. Keep copies, clinical-content logs, retention and additional suppliers within that arrangement. Notify the hospital promptly of personal-data breaches. Processor duties include helping the controller meet the applicable patient-rights and security obligations. [GDPR, Articles 28, 29 and 33(2)][gdpr]

Before production the hospital should assess whether a data protection impact assessment is required. Article 35 covers processing likely to create high risk, including large-scale special-category processing. An AI component alone does not settle the test. Consult the hospital's DPO as part of this assessment. No general requirement to obtain advance permission from ÚOOÚ follows merely from using an API. [GDPR, Articles 35 and 36][gdpr]

The unresolved production questions are the registry's precise purpose and legal basis, supplier roles and contracts, actual provider settings, and MOÚ's applicable security requirements. This research did not audit those matters or authorise a deployment. The local project description was read; no patient scan or extracted patient text was submitted to an external service during this research.

## Dated primary sources

Checked 2026-10-16. Statutes and the regulation are law. Supervisory guidance, the Court's press summary and vendor documentation have different legal status.

- [GDPR, Regulation (EU) 2016/679][gdpr], recital 26 and Articles 4, 5, 6, 9, 25, 28, 29, 32, 33, 35, 36, 44 to 46 and 89.
- [Act 372/2011 Sb., official consolidated PDF][health-act], sections 51, 53, 55b, 55d and 65. The PDF is labelled 2026-01-01; the companion Czech note records the check against the July 2026 wording.
- [ÚOOÚ processor Q&A][uoou-processor] and [healthcare Q&A][uoou-health].
- [European Commission, application of GDPR and controller/processor roles][commission-roles].
- [EDPB Opinion 22/2024 on reliance on processors and subprocessors][edpb-transfers].
- [European Commission, adequacy decisions][adequacy]. No provider certification was verified and no specific transfer mechanism was selected.
- [Court of Justice, official summary of C-413/23 P][court]. This is a non-binding press summary, not the full judgment.
- [Official OpenAI API data controls][openai]. No customer account, negotiated agreement or configuration was inspected.

[gdpr]: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679
[health-act]: https://e-sbirka.gov.cz/souborove-sluzby/soubory/70c921c1-add0-4773-be4e-0860790bdd91
[uoou-processor]: https://uoou.gov.cz/profesional/qa-otazky-a-odpovedi/zpracovatel
[uoou-health]: https://uoou.gov.cz/verejnost/qa-otazky-a-odpovedi/zdravotnictvi
[commission-roles]: https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/application-gdpr_en
[edpb-transfers]: https://www.edpb.europa.eu/system/files/2024-10/edpb_opinion_202422_relianceonprocessors-sub-processors_en.pdf
[adequacy]: https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en
[court]: https://curia.europa.eu/site/upload/docs/application/pdf/2025-09/cp250107en.pdf
[openai]: https://developers.openai.com/api/docs/guides/your-data
