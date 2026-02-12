# CIT/CAFC Decision Analysis — Trade-Lawyer Assessment Protocol

## Overview

This methodology defines how to search for, analyze, and assess Court of International Trade (CIT) and Court of Appeals for the Federal Circuit (CAFC) decisions like a trade lawyer. The goal is not just to find decisions — it is to understand their **impact on practice**, **strategic implications**, and **position in the precedent landscape**.

---

## Phase 1: Decision Search

### Multi-Source Search Protocol

Execute these searches in sequence to find relevant decisions:

**1. CIT Slip Opinions Index**
```
web_fetch("https://www.cit.uscourts.gov/content/slip-opinions-{YYYY}")
```
- Scan for cases involving the relevant HTS heading(s)
- Filter by jurisdiction code: `1581(a)` for classification cases
- Note: This gives case metadata only — not opinion text

**2. Justia Case Law (best for full text)**
```
web_search("site:law.justia.com Court International Trade {HTS heading} classification")
web_search("site:law.justia.com CIT {product type} {heading}")
```

**3. Google-Indexed Decisions**
```
web_search("Court of International Trade {HTS heading} classification")
web_search("CIT {product type} tariff classification GRI")
```

**4. CAFC Appeals**
```
web_search("CAFC {product type} HTS classification appeal")
web_search("Federal Circuit {heading} tariff classification")
```

**5. Heading-Specific Deep Search**
```
web_search("CIT heading {XXXX} classification {year range}")
web_search("{product} v. United States tariff classification")
```

### Decision Selection Criteria

Prioritize decisions that are:
1. **On point:** Involving the same or similar HTS heading(s)
2. **Recent:** More recent decisions better reflect current legal standards
3. **Binding:** CAFC decisions over CIT decisions
4. **Published:** Published decisions over unpublished/nonprecedential
5. **Classification-specific:** § 1581(a) cases, not AD/CVD or other jurisdictions

---

## Phase 2: Decision Summarization

For each relevant decision found, extract and synthesize:

### A. Case Information
- **Caption:** Full case name (e.g., *Acme Corp. v. United States*)
- **Court:** CIT or CAFC
- **Date:** Decision date
- **Docket/Slip Op.:** Docket number and/or slip opinion number
- **Judge:** Presiding judge (for CIT)
- **Jurisdiction:** § 1581 subsection
- **Procedural posture:** Trial, summary judgment, appeal from CIT

### B. Factual Background
- **Product at issue:** Description of the imported merchandise
- **Classification dispute:** What heading did the importer propose vs. what CBP classified?
- **Key physical/functional characteristics** relied on by the court

### C. Legal Framework
- **GRI(s) applied:** Which General Rule(s) resolved the case
- **Section/Chapter Notes cited:** Specific notes the court relied on
- **Explanatory Notes cited:** WCO Explanatory Notes referenced
- **Key legal test applied:** (e.g., essential character, common meaning, principal use)

### D. Court's Analysis
- **Step-by-step reasoning:** How the court worked through the GRI analysis
- **Dispositive finding:** What factual or legal determination decided the case
- **The "money quote":** The key sentence or passage a practitioner would cite

### E. Holding
- **Classification determined:** The HTS subheading the court found correct
- **Which party prevailed:** Importer or government
- **Scope of ruling:** Does it apply narrowly to the specific product, or broadly to a product category?

---

## Phase 3: Impact Assessment

After summarizing, assess the decision's impact on practice:

### A. Effect on Classification Practice
- How does this decision affect classification of **similar products**?
- Does it **narrow** or **expand** the scope of a heading/subheading?
- Does it establish a **new test** or refine an existing one?
- Does it **clarify ambiguity** in heading text or notes?

### B. CROSS Ruling Alignment
- Which existing CROSS rulings does this decision **reinforce**?
- Which CROSS rulings does it **undermine or distinguish**?
- Should CBP revoke or modify any rulings in light of this decision?
- Are there outstanding rulings that are now inconsistent with the court's reasoning?

### C. Practical Scope
- Does the decision apply only to the **specific product** before the court?
- Or does it establish a **principle** applicable to a broader category?
- Could it be used as authority in disputes over **related products**?

---

## Phase 4: Strategic Analysis

Provide trade-lawyer strategic assessment:

### A. Client Advisory
- What should **importers of similar goods** do now?
- Should existing entries be **reviewed** for potential reclassification?
- Should **protests be filed** on past entries under the old classification?
- Should **prior disclosures** be made if entries were filed at the wrong rate?
- Does the decision create an opportunity for **reclassification at a lower rate**?

### B. Litigation Outlook
- Is the decision likely to be **appealed** (CIT → CAFC)?
- If a CAFC decision, is it likely to be **reconsidered en banc** or taken by the Supreme Court?
- What are the **odds of reversal** on appeal? (Consider: clarity of reasoning, factual record, applicable standard of review)
- Is this an **outlier** among CIT judges, or does it reflect the court's consensus?

### C. CBP Response
- Will CBP likely **acquiesce** to this decision?
- Will CBP issue new CROSS rulings consistent with the decision?
- Will CBP limit the decision to its **specific facts** (as it often does)?

---

## Phase 5: Precedent Mapping

Position the decision in the broader precedent landscape:

### A. Line of Cases
- What **prior decisions** does the court cite and follow?
- Does the decision **follow**, **distinguish**, or **depart** from prior CIT/CAFC authority?
- Does it **resolve** a split among CIT judges on this issue?
- Does it create a **new split** or diverge from another judge's approach?

### B. Unresolved Questions
- What issues does the court **not reach** or **leave open**?
- What **factual variations** might lead to a different result?
- What **future cases** could test or extend this decision's principles?

### C. Trend Analysis
- Is the court trending toward a **broader or narrower** interpretation of the heading?
- Is there a pattern in how the court applies GRI 3(b) essential character to this product type?
- Are there emerging **tensions** between CIT judges on classification methodology?

---

## Cross-Reference with Classification Workflow

When CIT analysis is performed as part of a classification (Workflow 1, Step 5):

1. **Search for decisions** on each candidate HTS heading
2. **Filter** for § 1581(a) classification cases
3. **Cross-reference** findings with CROSS ruling research:
   - Do court decisions support the same classification as the CROSS rulings?
   - If not, flag the conflict (per `reference/human-review-triggers.md`)
4. **Adjust confidence** in the recommended classification based on judicial support:
   - CAFC support → high confidence
   - CIT support (no appeal) → moderate-high confidence
   - No judicial precedent → confidence depends on CROSS ruling consistency
   - Adverse judicial precedent → flag for attorney review
5. **Include** relevant decisions in the classification memo

---

## Output

Generate the assessment using `templates/cit-decision-brief.md`.
