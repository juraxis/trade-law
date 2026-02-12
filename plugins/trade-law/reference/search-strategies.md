# Search Strategies — Query Patterns for All Data Sources

This file contains validated, curated search patterns for retrieving trade and customs data. Use these patterns in `web_search` and `web_fetch` calls throughout all workflows.

---

## 1. HTS Classification Lookup

### USITC REST API (Tier 1 — Always try first)
```
web_fetch("https://hts.usitc.gov/reststop/search?keyword={TERM}")
```
- Returns: Up to 100 tariff articles as JSON
- Fields: htsno, description, indent, general, special, other, footnotes, units
- **Does NOT include** chapter/section notes — only heading/subheading data
- URL-encode the keyword term
- Try multiple keyword variations for best coverage

### Bulk JSON (Tier 2 — For hierarchy navigation)
```
web_fetch("https://www.usitc.gov/sites/default/files/tata/hts/hts_2026_revision_2_json.json")
```
- Returns: Complete flat array of all HTS line items
- Use `scripts/hts-hierarchy-builder.py` to convert to navigable tree
- Or user uploads the file for local processing

### Chapter PDFs (Tier 3 — For chapter/section notes)
```
web_fetch("https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter+{N}")
```
- Returns: Binary PDF — recommend user download
- **Only source** for chapter notes, section notes, and General Notes
- Critical for GRI 1 analysis

### Web Search Fallback
```
web_search("{product name} HTS classification HTSUS")
web_search("{product function} tariff heading chapter {XX}")
web_search("HTSUS {heading number} {product description}")
web_search("HTS chapter {N} notes {relevant note topic}")
```

---

## 2. CROSS Ruling Research

### Primary Method — Google Site Search (validated, best results)
```
web_search("site:rulings.cbp.gov {product} {HTS heading}")
web_search("site:rulings.cbp.gov {product description} classification")
web_search("CBP CROSS ruling {product type} classification {heading}")
web_search("{product type} tariff classification ruling CBP")
```
- Google indexes the full ruling text from the CROSS SPA
- Returns: Ruling number, full legal analysis, HTS classification, cross-references

### Direct Ruling URL (for known ruling IDs)
```
web_fetch("https://rulings.cbp.gov/ruling/{RULING_ID}")
```
- **Warning:** CROSS is a JS SPA — `web_fetch` returns empty shell
- Use the ruling ID from search results and reference it for the attorney
- Alternatively, search for the specific ruling number via web_search

### Boolean Search Patterns (for use within CROSS interface)
- AND: `keyboard AND bluetooth AND 8471`
- OR: `smartwatch OR "smart watch" OR "wrist computer"`
- AND NOT: `keyboard AND NOT piano`
- NEAR: `essential NEAR character` (finds terms in proximity)
- Wildcard: `comput*` (matches computer, computing, computation)
- Exact phrase: `"essential character"`
- Collections: ALL (default), HQ (Headquarters only), NY (New York only)

### Ruling Research Strategy
1. Start broad: `web_search("site:rulings.cbp.gov {product name}")`
2. Narrow by heading: `web_search("site:rulings.cbp.gov {product} {4-digit heading}")`
3. Search for GRI-specific reasoning: `web_search("CBP ruling {product} essential character GRI 3")`
4. Check for revocations: `web_search("CBP ruling revoked {ruling number}")`
5. Find HQ rulings: `web_search("site:rulings.cbp.gov HQ {product} {heading}")`

---

## 3. CIT/CAFC Court Decisions

Sources are **not** co-equal. Follow this strict priority order:

### Step 1: CIT Slip Opinions Index — identify decisions
```
web_fetch("https://www.cit.uscourts.gov/content/slip-opinions-{YYYY}")
```
- Returns: Structured table with opinion #, caption, date, docket, judge, jurisdiction code
- Filter for jurisdiction code `1581(a)` = classification cases

### Step 2: PDF Text Extraction — PRIMARY SOURCE for opinion text
```
bash: python3 plugins/trade-law/scripts/cit-opinion-fetcher.py {slip-op-number}
```
- Example: `python3 plugins/trade-law/scripts/cit-opinion-fetcher.py 26-11`
- Downloads the PDF from `cit.uscourts.gov` and extracts full text using pymupdf
- Also accepts a full URL or local file path
- This is the primary source for opinion text. Always use this before fallbacks.

### Step 3: Fallback Sources — only if PDF reader is unavailable
```
web_search("site:law.justia.com Court International Trade {product} classification")
web_search("site:law.justia.com CIT {HTS heading} {year}")
```
- Justia indexes full case text in readable format
- Use only as a fallback when direct PDF fetch fails

```
web_search("Court of International Trade {HTS heading} classification")
web_search("CIT {product type} classification {heading} GRI")
web_search("site:cit.uscourts.gov {product} classification")
```

### CAFC Appeals
```
web_search("CAFC {product type} HTS classification appeal")
web_search("Federal Circuit {heading} tariff classification")
web_search("Court of Appeals Federal Circuit customs classification {product}")
```

### CIT Decision Filtering
- Jurisdiction 1581(a): Classification disputes (primary interest)
- Jurisdiction 1581(c): AD/CVD cases
- Jurisdiction 1581(i): Residual jurisdiction
- Always check for CAFC appeal status of any CIT decision cited

---

## 4. Chapter 99 / Trade Remedy Surcharges

### Section 301 (China Tariffs)
```
web_search("Section 301 tariff {HTS heading} China {current_year}")
web_search("USTR Section 301 list {product type} {current_year}")
web_search("9903.88 {HTS heading} Section 301")
web_search("Section 301 exclusion {product} {HTS heading} {current_year}")
```

### Section 232 (Steel/Aluminum)
```
web_search("Section 232 tariff {product} {current_year}")
web_search("Section 232 steel aluminum tariff rate {current_year}")
web_search("Section 232 exclusion {product} {current_year}")
```

### Section 201 (Safeguard)
```
web_search("Section 201 safeguard tariff {product} {current_year}")
```

---

## 5. AD/CVD Orders

```
web_search("antidumping duty order {product} {country}")
web_search("countervailing duty {product} {country}")
web_search("AD/CVD order {product} {country} Federal Register")
web_search("International Trade Administration antidumping {product}")
web_search("Commerce Department scope ruling {product} {country}")
```

---

## 6. Country of Origin

### Marking Rules
```
web_search("CBP country of origin marking {product type}")
web_search("19 CFR 134 substantial transformation {product}")
web_search("site:rulings.cbp.gov country of origin {product}")
```

### FTA Rules of Origin
```
web_search("USMCA rules of origin {HTS heading} tariff shift")
web_search("{FTA name} rules of origin {product type}")
web_search("CAFTA-DR origin {HTS chapter} rule")
```

### Trade Agreements Act (TAA)
```
web_search("TAA substantial transformation {product} {country}")
web_search("Trade Agreements Act designated country list {current_year}")
```

---

## 7. Supplemental Sources

### Informed Compliance Publications
```
web_search("CBP informed compliance {product type}")
web_search("site:cbp.gov informed compliance classification {chapter}")
```

### Explanatory Notes (World Customs Organization)
```
web_search("WCO Explanatory Notes heading {XXXX}")
web_search("Harmonized System Explanatory Notes {heading} {product}")
```

### Federal Register Notices
```
web_search("Federal Register {topic} tariff {current_year}")
web_search("site:federalregister.gov customs {product} {current_year}")
```

---

## CROSS API Investigation (Developer Note)

The CROSS SPA at `rulings.cbp.gov` likely makes XHR calls to an internal REST API for search and ruling retrieval. If this API endpoint can be identified, it would provide a more reliable retrieval method than Google snippet indexing.

**Investigation approach (developer task, not a Claude runtime task):**
1. Open Chrome DevTools → Network tab → XHR filter
2. Navigate to `rulings.cbp.gov` and perform a search
3. Capture the endpoint URL, request headers, and response format
4. Document the API contract (query parameters, response schema, pagination)

If discovered, document the endpoint here and add as a primary retrieval method in `methodology/cross-ruling-research.md`. This would enable **Verified** evidence quality (see evidence quality protocol) for all rulings retrieved via the API.

---

## Search Strategy Tips

1. **Always search with the current year** to get the most recent information
2. **Use multiple keyword variations** — trade terminology may differ from common language
3. **Prioritize site-specific searches** (`site:rulings.cbp.gov`, `site:law.justia.com`) for authoritative sources
4. **Cross-reference** results from multiple searches — no single search captures everything
5. **Check footnotes** in HTS API results for Chapter 99 cross-references (e.g., "See 9903.88.15")
6. **REST API first** for HTS data, then web_search for context and interpretation
