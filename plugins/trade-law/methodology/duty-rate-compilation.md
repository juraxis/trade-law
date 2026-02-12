# Duty Rate Compilation

## Overview

Total duty on a U.S. import is the sum of multiple components. This methodology ensures all applicable duty layers are identified and compiled.

---

## Duty Components

### A. Column 1 General Rate (MFN/NTR)

The standard "most favored nation" rate applying to imports from all countries with Normal Trade Relations (NTR) status with the United States.

**How to find:**
1. Query USITC REST API:
   ```
   web_fetch("https://hts.usitc.gov/reststop/search?keyword={product}")
   ```
2. The `general` field contains the Column 1 General rate.
3. Rate formats:
   - **Ad valorem:** `6.5%` (percentage of customs value)
   - **Specific:** `3.4¢/kg` (fixed amount per unit)
   - **Compound:** `2.8% + 28.8¢/kg` (both ad valorem and specific)
   - **Free:** No duty

---

### B. Special Program Rates

Preferential rates available under Free Trade Agreements (FTAs) and preference programs.

**How to find:**
1. The `special` field in HTS data shows available programs.
2. Example: `Free (A+,AU,BH,CL,CO,D,E,IL,JO,KR,MA,OM,P,PA,PE,S,SG)`
3. Decode codes using `reference/fta-program-codes.json`.
4. Determine if the country of origin qualifies for any listed program.
5. Verify the specific FTA rules of origin are met (tariff shift, regional value content, etc.).

**Important:** Eligibility for a special rate requires:
- Origin in a qualifying country
- Compliance with the specific program's rules of origin
- Proper documentation (certificate of origin, importer's declaration)
- The program must be currently active (check GSP/AGOA expiration)

---

### C. Column 2 Rate

Applies to imports from countries without NTR status: Cuba, North Korea, and potentially others.

**How to find:** The `other` field in HTS data contains the Column 2 rate. These rates are typically much higher than Column 1.

---

### D. Chapter 99 Additional Duties

These are the surcharges imposed under trade remedy statutes. See `methodology/chapter-99-surcharges.md` for detailed identification.

**Types:**
- **Section 301** (Trade Act of 1974, § 301): Retaliatory tariffs (primarily China)
- **Section 232** (Trade Expansion Act of 1962, § 232): National security tariffs (steel, aluminum)
- **Section 201** (Trade Act of 1974, § 201): Safeguard tariffs (solar cells, washing machines)

**How to find:**
1. Check `footnotes` in HTS API results for Chapter 99 references (e.g., "See 9903.88.15")
2. Search: `web_search("Section 301 tariff {HTS heading} China {current_year}")`
3. Search: `web_search("Section 232 tariff {product} {current_year}")`
4. Follow `methodology/chapter-99-surcharges.md` for complete identification protocol.

---

### E. Antidumping Duties (AD)

Additional duties imposed on specific products from specific countries when the U.S. Department of Commerce determines the products are sold in the U.S. at less than fair value.

**How to find:**
```
web_search("antidumping duty order {product} {country}")
web_search("International Trade Administration antidumping {product}")
```

**Key points:**
- AD rates are company-specific (individual rates for examined producers, an "all others" rate, and a country-wide rate)
- Rates can range from 0% to over 200%
- Scope determinations define exactly which products are covered
- AD duties are assessed in addition to all other duties

---

### F. Countervailing Duties (CVD)

Additional duties imposed to offset subsidies provided by a foreign government to its producers/exporters.

**How to find:**
```
web_search("countervailing duty {product} {country}")
web_search("Commerce Department CVD {product} {country}")
```

**Key points:**
- CVD rates are also typically company-specific
- Can apply concurrently with AD duties
- Scope aligns with the AD order if both exist

---

### G. Merchandise Processing Fee (MPF)

A fee — not a duty — assessed by CBP on most formal entries (19 CFR § 24.23).

**Rate structure:**
- **Ad valorem rate** on the entered value of the merchandise
- **Minimum per entry** and **maximum per entry** thresholds apply
- Formal entries (value >$2,500) and informal entries have different rate structures

**How to find current rates:**
```
web_search("CBP merchandise processing fee {current_year}")
web_search("19 CFR 24.23 merchandise processing fee rate {current_year}")
```

**Important:** Do NOT hard-code MPF dollar amounts. The ad valorem rate, minimum, and maximum thresholds are adjusted periodically. Always verify current-year rates via web_search before presenting.

---

### H. Harbor Maintenance Fee (HMF)

A fee — not a duty — assessed on the customs value of goods arriving by ocean vessel (26 U.S.C. § 4461).

**Rate structure:**
- **Ad valorem rate** on the customs value of the cargo
- Applies to **ocean shipments only** (not air or land border crossings)
- Paid by the importer via CBP

**How to find current rates:**
```
web_search("harbor maintenance fee rate {current_year}")
web_search("HMF harbor maintenance fee CBP {current_year}")
```

**Important:** Do NOT hard-code HMF rates. Always verify the current-year rate via web_search.

---

## Compilation Format

Present the total duty as an itemized table:

```
DUTY RATE COMPILATION
HTS Subheading: {XXXX.XX.XXXX}
Country of Origin: {Country}
Date of Analysis: {Date}

| Component | Rate | Authority | Notes |
|-----------|------|-----------|-------|
| Column 1 General | X.X% | HTSUS {subheading} | MFN/NTR rate |
| Section 301 | XX% | 9903.XX.XX | List {N}, effective {date} |
| Section 232 | XX% | 9903.XX.XX | {Product type}, effective {date} |
| AD Duty | XX.XX% | A-{XXX}-{XXX} | {Company/all others rate} |
| CVD Duty | XX.XX% | C-{XXX}-{XXX} | {Company/all others rate} |
| **TOTAL ESTIMATED DUTY** | **XX.XX%** | | **Sum of all duty components** |
| MPF (fee) | rate% (min/max per entry — verify) | 19 CFR § 24.23 | Formal entry fee |
| HMF (fee) | rate% (verify) | 26 U.S.C. § 4461 | Ocean shipments only |

Special Program Rate: {rate} under {program code} — if origin qualifies
```

---

## Stacking Rules

Duties **stack** (are additive):
- General rate + Section 301 + Section 232 + AD + CVD = Total
- Example: 2.5% general + 25% Section 301 + 10% AD = 37.5% total

Duties do **not** compound (no duty-on-duty):
- Each duty is calculated on the **customs value** (transaction value), not on the duty-inclusive price

---

## Verification Checklist

Before presenting duty compilation, verify:

- [ ] Correct HTS subheading (including statistical suffix)
- [ ] Country of origin confirmed
- [ ] Column 1 General rate from current HTS revision
- [ ] All applicable Chapter 99 surcharges identified
- [ ] AD/CVD orders checked for the specific product-country combination
- [ ] Special program eligibility assessed (if origin qualifies)
- [ ] Footnotes in HTS data reviewed for cross-references
- [ ] MPF rate/min/max verified against current-year sources
- [ ] HMF rate verified (ocean shipments only)
- [ ] Data freshness: all rates verified against current-year sources
