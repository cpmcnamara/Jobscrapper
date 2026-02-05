# Capgemini Invent – Data & AI Job Scraper

Scrapes the Capgemini careers site using [Firecrawl](https://firecrawl.dev) to find **Invent Data & AI** roles in **North America**.

## Quick Start

```bash
pip install -r requirements.txt
python scraper.py
```

## Configuration

Edit the constants at the top of `scraper.py` to adjust:

- `FIRECRAWL_API_KEY` – your Firecrawl API key (or set the `FIRECRAWL_API_KEY` env var)
- `KEYWORDS_MUST` – required keywords (default: "invent")
- `KEYWORDS_DOMAIN` – domain keywords (data, AI, etc.)
- `KEYWORDS_REGION` – location keywords (North America cities/regions)

## Output

Results are saved to:

- `results/jobs.json` – full structured data
- `results/jobs.csv` – title, location, and URL
