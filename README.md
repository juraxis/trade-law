# Trade Law — Claude Code Plugin

A Claude Code plugin for U.S. trade & customs classification, CROSS ruling research, CIT/CAFC decision analysis, duty rate compilation, and compliance review.

> **Disclaimer:** All outputs produced by this plugin are **draft work product** intended for review by a U.S.-licensed attorney or licensed customs broker. Nothing in this plugin or its outputs constitutes legal advice, and no attorney-client or broker-client relationship is created by its use. Users must independently verify all classifications, duty rates, and compliance determinations before relying on them for any import transaction.

---

## Install

```
/plugin marketplace add juraxis/trade-law
/plugin install trade-law@juraxis
```

Then use:

```
/trade-law classify a Bluetooth keyboard from China
/trade-law find CROSS rulings for ceramic mugs under heading 6912
/trade-law calculate duty for HTS 8471.30.0100 from Taiwan
```

---

## v1.0 Features

| # | Workflow | Description |
|---|----------|-------------|
| 1 | **Classify a Product** | Full GRI 1-6 analysis with CROSS research, CIT/CAFC check, and duty compilation |
| 2 | **Research CROSS Rulings** | Search and digest CBP rulings with authority-level assessment |
| 3 | **Analyze CIT/CAFC Decision** | Court decision briefing with precedent mapping and strategic analysis |
| 4 | **Calculate Duty Rate** | Complete duty compilation: General + Special + Chapter 99 + AD/CVD + MPF/HMF |
| 5 | **Check Surcharges** | Section 301, 232, 201 surcharge applicability and exclusion screening |
| 6 | **Country of Origin Analysis** | Marking, FTA qualification, TAA compliance, substantial transformation |
| 7 | **Full Compliance Review** | End-to-end review: classification + duty + origin + PGA + UFLPA screening |

---

## Domain Configuration

The plugin accesses live government data sources via `web_fetch`. After installing, add the following domains to your Claude Code settings (`~/.claude/settings.local.json` or project-level):

```json
{
  "permissions": {
    "allow": [
      "WebFetch(hts.usitc.gov/*)",
      "WebFetch(www.usitc.gov/*)",
      "WebFetch(search.uscourts.gov/*)",
      "WebFetch(www.cit.uscourts.gov/*)",
      "WebFetch(law.justia.com/*)",
      "WebFetch(www.federalregister.gov/*)",
      "WebFetch(rulings.cbp.gov/*)"
    ]
  }
}
```

| Domain | Purpose |
|--------|---------|
| `hts.usitc.gov` | USITC HTS REST API (tariff data) |
| `www.usitc.gov` | USITC website (general reference) |
| `search.uscourts.gov` | Federal court decision search |
| `www.cit.uscourts.gov` | Court of International Trade slip opinions |
| `law.justia.com` | CIT/CAFC full-text decisions |
| `www.federalregister.gov` | AD/CVD orders and trade actions |
| `rulings.cbp.gov` | CBP CROSS rulings (future use) |

---

## File Structure

```
trade-law/
├── .claude-plugin/
│   └── marketplace.json                  # Marketplace catalog
├── plugins/
│   └── trade-law/
│       ├── .claude-plugin/
│       │   └── plugin.json               # Plugin manifest
│       ├── commands/
│       │   └── trade-law.md              # /trade-law slash command
│       ├── SKILL.md                      # Full skill definition + workflow router
│       ├── methodology/                  # 11 classification methodology files
│       ├── reference/                    # 9 reference files
│       ├── templates/                    # 5 output templates
│       └── scripts/
│           └── hts-hierarchy-builder.py  # HTS JSON hierarchy builder
├── .gitignore
└── README.md
```

---

## Roadmap

- **v1.1** — Customs Valuation (transaction value, assists, royalties, first-sale)
- **v1.2** — Entry & Post-Entry (entry types, protests, reconciliation, prior disclosure)
- **v1.3** — AD/CVD Deep Dive (scope rulings, circumvention, EAPA)
- **v1.4** — Quota & TRQ
- **v1.5** — Foreign Trade Zones
- **v1.6** — Entry Document Review

---

## License

All rights reserved. This skill framework is published for reference and educational purposes.
