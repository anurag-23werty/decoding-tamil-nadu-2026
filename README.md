# 🗳️ Decoding Tamil Nadu 2026

> **A storytelling-first election analytics project** — exploring constituency shifts, regional changes, and victory patterns in the 2026 Tamil Nadu Assembly Election.

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-decoding--tamil--nadu--2026.vercel.app-blue?style=flat-square&logo=vercel)](https://decoding-tamil-nadu-2026.vercel.app)
[![Jupyter Notebook](https://img.shields.io/badge/Analysis-TNelections.ipynb-orange?style=flat-square&logo=jupyter)](./TNelections.ipynb)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python)](./Scrappers)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 📌 Overview

This project analyses the **2026 Tamil Nadu Assembly Election** through the lens of publicly available Election Commission of India (ECI) data. The goal is not just to present numbers, but to tell the story of a state that was politically remapped — three chapters, one coherent narrative.

| Stat | Value |
|------|-------|
| Constituencies analysed | **234** |
| Seats that changed hands | **163 (70%)** |
| TVK seats on debut | **108** |
| Average margin (2026) | **16,784 votes** ↓ 27% from 2021 |
| Voter turnout (2026) | **85.1%** — a state record |
| Seats won with < 35% vote share | **61** |

---

## 📊 Analysis Highlights

### Chapter 1 · The Flip — 163 Seats Changed Hands

In 2021, Tamil Nadu was a two-party contest. By 2026, TVK (Tamilaga Vettri Kazhagam) emerged as the single largest party on debut — reshaping the entire political map.

> *"The biggest source of TVK's seats were constituencies that DMK held in 2021 — 65 of TVK's 108 wins came directly from former DMK territory."*

**Seat flow: 2021 winners → 2026 winners**

```
2021                  2026
────────────────────────────────
DMK (65 seats) ──────────► TVK
AIADMK ──────────────────► TVK / AIADMK
Others ───────────────────► scattered
```

![Seat Flow Sankey — 2021 to 2026](https://decoding-tamil-nadu-2026.vercel.app/og-sankey.png)
> *Width of each band = number of seats transferred. The thick orange band shows 65 DMK seats flowing directly to TVK.*

**Regional breakdown of seat shifts:**

| Region | TVK | DMK | AIADMK | Others |
|--------|-----|-----|--------|--------|
| Chennai Metro | Dominant | Contracted | Minimal | — |
| Central | Competitive | Held some | Held 2021 count | — |
| North | Strong | Lost heavily | Moderate | — |
| South | Strong | Contracted | Contracted | — |
| West | Competitive | Moderate | Moderate | — |
| Delta | Mixed | Moderate | Some | — |

---

### Chapter 2 · The Vote Share Story

TVK matched DMK's 2021 state-wide vote share — almost perfectly — region by region.

**State-wide vote share comparison:**

| Party | 2021 | 2026 |
|-------|------|------|
| DMK | 38.0% | 24.3% |
| AIADMK | 33.5% | 21.3% |
| TVK | — | **35.1%** |
| INC | 4.3% | 3.4% |
| PMK | 3.8% | — |

![Vote Share Mirror — TVK 2026 vs DMK 2021](https://decoding-tamil-nadu-2026.vercel.app/og-mirror.png)
> *Orange line (TVK 2026) and red dashed line (DMK 2021) run almost parallel across all six regions — the clearest evidence of a coherent, directional voter shift.*

**Turnout surge:**

```
2021: 73.4%  ████████████████████░░░░░░
2026: 86.2%  ████████████████████████░░  (+12.8 pp — state record)
```

> *Voter turnout rose nearly 13 percentage points. TVK's arrival may have mobilised previously non-voting citizens, expanding the electorate rather than only redistributing it.*

---

### Chapter 3 · The Margin of Victory

With three parties splitting the vote, victories became slimmer and majority wins became rare.

![Distribution of Winner Vote % — 2021 vs 2026](https://decoding-tamil-nadu-2026.vercel.app/og-distribution.png)
> *The entire distribution shifts left in 2026. In 2021 the peak was at 45–50%. In 2026 it moved to 35–40% — reflecting the three-way split compressing every winner's share.*

**Seats won with >50% vote share:**

| Year | Seats with >50% | Seats with <35% |
|------|-----------------|-----------------|
| 2021 | **84** | 2 |
| 2026 | **14** | **61** |

**Tightest finishes in 2026:**

| Constituency | Winner | Margin | Vote% |
|---|---|---|---|
| Tiruppattur | TVK | **1 vote** | 38.8% |
| Veppanahalli | DMK | 138 | 33.8% |
| Kanniyakumari | AIADMK | 214 | 31.5% |
| Polur | TVK | 227 | 32.2% |
| Tirukkoyilur | AIADMK | 285 | 33.7% |

**Most decisive wins in 2026:**

| Constituency | Winner | Margin | Vote% |
|---|---|---|---|
| Edapadi | AIADMK | 98,110 | 58.0% |
| Shozhinganallur | TVK | 96,780 | 49.5% |
| Madavaram | TVK | 94,985 | 52.8% |
| Avadi | TVK | 76,311 | 52.4% |
| Salem (West) | TVK | 74,867 | 51.6% |

---

## 📁 Repository Structure

```
decoding-tamil-nadu-2026/
│
├── TNelections.ipynb          # Main analysis notebook (EDA, charts, insights)
├── anurag.pptx                # Presentation deck summarising findings
│
├── Dashboard/                 # Interactive web dashboard (HTML/JS)
│   └── index.html             # Storytelling dashboard — deployed on Vercel
│
└── Scrappers/                 # Data collection scripts
    ├── tnelections_scraper.py # Scraper for tnelections2026.in
    └── eci_scraper.py         # Scraper for Election Commission of India data
```

---

## 🔧 Setup & Usage

### Prerequisites

```bash
python >= 3.10
jupyter notebook
pandas, matplotlib, seaborn, plotly
requests, beautifulsoup4
```

### Install dependencies

```bash
pip install pandas matplotlib seaborn plotly requests beautifulsoup4 jupyter
```

### Run the analysis

```bash
# Clone the repo
git clone https://github.com/anurag-23werty/decoding-tamil-nadu-2026.git
cd decoding-tamil-nadu-2026

# Launch the notebook
jupyter notebook TNelections.ipynb
```

### Run the scrapers (optional — data already included)

```bash
cd Scrappers

# Scrape from tnelections2026.in
python tnelections_scraper.py

# Scrape from Election Commission of India
python eci_scraper.py
```

---

## 🗄️ Data Sources

| Source | Description | URL |
|--------|-------------|-----|
| **tnelections2026.in** | 2026 Tamil Nadu election results, candidate-wise data | [tnelections2026.in](https://tnelections2026.in/) |
| **Election Commission of India (ECI)** | Official constituency-wise results, vote shares, margins | [eci.gov.in](https://eci.gov.in/) |

> ⚠️ This project uses only **publicly available ECI data**. All analysis is strictly non-partisan — no causation is attributed to any party, leader, or community.

---

## 🌐 Live Dashboard

The interactive storytelling dashboard is deployed at:

**[decoding-tamil-nadu-2026.vercel.app](https://decoding-tamil-nadu-2026.vercel.app)**

It features:
- Animated Sankey chart of seat flows (2021 → 2026)
- Regional vote share comparison (bar + line charts)
- Victory margin distribution (histogram overlay 2021 vs 2026)
- Constituency-level tables for tightest and most decisive wins

---

## 📈 Key Findings Summary

1. **The Flip** — 163 of 234 constituencies (70%) changed their winning party. TVK collected 108 seats, with 65 coming directly from DMK-held constituencies of 2021.

2. **The Vote** — TVK's 35.1% state-wide share mirrors DMK's 38% from 2021 — region by region, the trend lines are near-identical. A record 86.2% turnout suggests new voters entered the pool alongside transfers.

3. **The Margin** — The three-way split compressed victories sharply. Average margin fell 27%. Seats won with <35% jumped from 2 to 61. The map looks decisive in seats; the margins tell a more fragile story.

---

## 🙌 Acknowledgements

- **AtliQ Media** — for the editorial framing and dashboard design
- **Election Commission of India** — for making constituency-level data publicly available
- **tnelections2026.in** — for aggregated candidate and party data

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

*Made with 📊 and curiosity · AtliQ Media — Tamil Nadu 2026 Election Special*
