# AI Job Market Trend Tracker

Tracks AI and data job trends across major consulting and tech companies using [Firecrawl](https://firecrawl.dev). Includes a Next.js dashboard deployable to Vercel.

## Companies Tracked

**Consulting:** Capgemini, Deloitte, Accenture, McKinsey, BCG, EY, PwC, KPMG, Bain

**Tech:** Google, Microsoft, Amazon, Meta, Apple, OpenAI, Anthropic, Databricks, Snowflake, Palantir

## Job Categories

- **AI / Data Strategy** — AI transformation, data strategy, governance
- **Data Readiness / Engineering** — Data engineering, pipelines, governance, quality
- **AI / ML Engineering** — ML engineers, MLOps, research scientists
- **Business Context / Domain AI** — AI consultants, applied AI, analytics
- **Gen AI / LLM** — Generative AI, prompt engineering, LLM roles

## Quick Start

### 1. Run the scraper

```bash
pip install -r requirements.txt
export FIRECRAWL_API_KEY=your-key-here
python -m backend.main                    # Scrape all companies
python -m backend.main --company google   # Single company
python -m backend.main --sector consulting # All consulting firms
python -m backend.main --generate-only    # Regenerate JSON from existing DB
python -m backend.main --list-companies   # List all configured companies
```

### 2. Run the dashboard locally

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000

### 3. Deploy to Vercel

Push this repo to GitHub, then import the `dashboard` directory in Vercel.

Set the **Root Directory** to `dashboard` in Vercel project settings.

## Architecture

```
backend/                  Python scraping + analysis
  config/                 Company configs, category definitions
  scraper/                Firecrawl-based generalized scraper
  normalizer/             Title, location, seniority, category normalization
  database/               SQLite storage with deduplication
  analysis/               Trend computations
  export/                 JSON file generator for dashboard

dashboard/                Next.js 14 app (Vercel-ready)
  src/app/                Pages: overview, trends, companies, categories, geo, jobs
  src/components/         Charts (Recharts), data tables, filters
  src/lib/                Types, API helpers, Excel export
  public/data/            Generated JSON data files

scraper.py                Original single-company Capgemini scraper
```

## Data Flow

```
Scraper (Firecrawl) → Normalize → SQLite DB → JSON files → Dashboard
```

The scraper writes to SQLite, then generates static JSON files into `dashboard/public/data/`. The dashboard reads these files at runtime — no backend server needed in production.

## Excel Export

The dashboard includes an "Export to Excel" button on the Overview and Jobs pages. Exports include:
- Full job listing sheet
- Summary by company
- Summary by category
