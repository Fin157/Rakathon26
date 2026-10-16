# Czech healthcare law for a production ProstaPaper service

Checked on 2026-10-16. This note concerns hospital production using real patient records. The user has confirmed the current hackathon examples are fully anonymous and unrestricted.

## Finding

The provisions examined regulate confidentiality, authorised access and safeguards. They do not create a universal on-premise hosting requirement. They also do not automatically authorise disclosure to any cloud or model supplier. The hospital must establish a lawful arrangement for the particular production purpose.

## Act 372/2011 Sb.

Primary sources: [official current-law page](https://e-sbirka.gov.cz/sb/2011/372?odkazId=91859203) and [official consolidated PDF](https://e-sbirka.gov.cz/souborove-sluzby/soubory/70c921c1-add0-4773-be4e-0860790bdd91).

The PDF is labelled 2026-01-01. The delegated source check compared the relevant provisions with e-Sbírka's wording current from 1 July 2026. It reported that the later change by Act 300/2025 concerns section 45(3)(h), rather than the provisions cited below. The PDF text for the cited provisions was also downloaded and inspected locally by the parent agent. This note does not claim a comprehensive audit of all hospital cybersecurity or sector-specific obligations.

- Section 51(1) requires provider confidentiality about facts learned in connection with providing healthcare. Section 51(2) specifies circumstances in which disclosure does not breach that duty, including disclosure within a patient's release and disclosures permitted by law without consent.
- Section 51(5) extends confidentiality to the listed people. These include health professionals, authorised accessors under section 65(2), and other people learning health information in activities performed under this Act or other law. It does not expressly establish a generic category of unrestricted hackathon or software-vendor access.
- Section 53(2) excludes information processed exclusively for a purpose other than care of a particular patient from the definition of medical documentation. That classification supplies neither an independent GDPR legal basis nor permission to disclose the source records.
- Section 53(3) permits use of the patient's rodné číslo when processing personal data in medical documentation. Removing it can reduce exposure without settling whether the remaining information is personal data.
- Section 55b requires a provider processing medical-record data for science and research to anonymise them so patient identity is not ascertainable. The resulting information is not medical documentation. Its application must be considered for research uses; it does not describe every routine care or registry-administration operation.
- Section 55d requires written processing rules and suitable technical and organisational measures so processing follows this Act and applicable personal-data protection requirements.
- Section 65(2) limits no-consent access to the listed categories, relevant purposes and necessary extent. Section 65(2)(a) covers provider workers and people in analogous positions with specified care-related qualifications or further tasks under the relevant laws. This is not a blanket access entitlement for every software contractor. Section 65(2)(s), addressing clinical-study oversight, does not create a general software-development research entitlement.

The conclusion about external hosting is a reading of these provisions together with GDPR's processor framework. The hospital still needs to establish how its actual contractor arrangement satisfies access and confidentiality rules.

## GDPR and Czech supervisory guidance

[GDPR](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679) applies directly in Czechia. Articles 6 and 9 govern the underlying basis and health-data exception; Articles 28 and 29 govern processor instructions and contracts; Article 32 governs risk-appropriate security; Chapter V governs international transfers.

[ÚOOÚ's processor Q&A](https://uoou.gov.cz/profesional/qa-otazky-a-odpovedi/zpracovatel) expressly lists cloud storage and external IT-system operators as typical processors. It explains documented instructions, contractual requirements and prior written controller authorisation of subprocessors.

[ÚOOÚ's professional healthcare Q&A](https://uoou.gov.cz/profesional/qa-otazky-a-odpovedi/zdravotnictvi) also discusses confidentiality for other people who learn health information during their activities and processing only under controller instructions.

Act 110/2019 Sb. is the Czech GDPR adaptation law. No conclusion in this note depends on treating its research provisions as a blanket exemption. In particular, a claim of research does not itself establish the production service's legal basis or displace the section 55b question.
