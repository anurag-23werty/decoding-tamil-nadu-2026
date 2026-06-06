# 🗳️ Decoding Tamil Nadu 2026

> **A storytelling-first election analytics project** exploring constituency shifts, regional changes, voter participation, and victory patterns in the 2026 Tamil Nadu Assembly Election.

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-decoding--tamil--nadu--2026.vercel.app-blue?style=flat-square&logo=vercel)](https://decoding-tamil-nadu-2026.vercel.app)

---

## 📌 Overview

This project analyzes the **2026 Tamil Nadu Assembly Election** using publicly available Election Commission of India (ECI) data.

Developed as part of the **Codebasics Resume Project Challenge (RPC)**, the project focuses on identifying meaningful patterns in election data and presenting them through a storytelling-first approach.

---

## 🌐 Live Dashboard

🔗 https://decoding-tamil-nadu-2026.vercel.app

---

## 📊 Executive Summary

| Metric | Value |
|----------|----------|
| Constituencies Analyzed | **234** |
| Seats That Changed Winners | **163 (69.7%)** |
| TVK Seats Won | **108** |
| Average Winning Margin (2026) | **16,784 votes** |
| Change in Average Margin | **-27% vs 2021** |
| Average Turnout (2026) | **86.2%** |
| Seats Won Below 35% Vote Share | **61** |

---

## Chapter 1 · The Flip Story

### 163 Constituencies Changed Winners

- 163 out of 234 constituencies elected a different winner compared to 2021.
- Only 71 constituencies retained the same winning party.
- Nearly 70% of Tamil Nadu's electoral map experienced a change in winning party.

### Seat Flow Analysis

- 65 constituencies won by DMK in 2021 were won by TVK in 2026.
- This represents the single largest constituency-flow segment observed in the analysis.

---

## Chapter 2 · Vote Share & Participation

### State-wide Vote Share

| Party | 2021 | 2026 |
|----------|----------|----------|
| DMK | 38.0% | 24.3% |
| AIADMK | 33.5% | 21.3% |
| TVK | — | 35.1% |
| INC | 4.3% | 3.4% |
| PMK | 3.8% | — |

### Voter Participation

| Metric | Value |
|----------|----------|
| Average Turnout (2021) | 73.4% |
| Average Turnout (2026) | 86.2% |
| Change | +12.8 percentage points |

---

## Chapter 3 · The Margin Story

### Average Winning Margin

| Year | Average Margin |
|----------|----------|
| 2021 | 22,871 votes |
| 2026 | 16,784 votes |

### Winner Vote Share Distribution

| Year | Seats Won Above 50% | Seats Won Below 35% |
|----------|----------|----------|
| 2021 | 84 | 2 |
| 2026 | 14 | 61 |

---

## 📁 Repository Structure

```text
decoding-tamil-nadu-2026/
│
├── TNelections.ipynb
├── anurag.pptx
│
├── Dashboard/
│   └── index.html
│
└── Scrappers/
    ├── tnelections_scraper.py
    └── eci_scraper.py
```

## 🔧 Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Matplotlib
- Jupyter Notebook
- HTML
- CSS
- Git
- GitHub
- Vercel

---

## 🗄️ Data Sources

- Election Commission of India (ECI)
- https://results.eci.gov.in
- https://tnelections2026.in
- Codebasics RPC Dataset

---

## ⚠️ Disclaimer

This project was developed as part of the Codebasics Resume Project Challenge.

The analysis is based solely on publicly available election data and is intended for educational and analytical purposes only.

This project does not endorse, criticize, or take any political position regarding any political party, candidate, alliance, community, region, or election outcome.

All findings presented in this repository are descriptive observations derived from the available data.

---

## 🙌 Acknowledgements

- Codebasics Resume Project Challenge
- Election Commission of India
- tnelections2026.in
- Open-source Python ecosystem

---

*Built with Python, data storytelling, and curiosity for understanding elections through data.*
