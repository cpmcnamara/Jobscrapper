#!/usr/bin/env python3
"""
AI Job Market Trend Tracker — CLI entry point.

Usage:
    python -m backend.main                    # Scrape all companies
    python -m backend.main --company google   # Single company
    python -m backend.main --sector tech      # All tech companies
    python -m backend.main --generate-only    # Regenerate JSON from existing DB
"""

import argparse
import sys

from backend.config.settings import Settings
from backend.config.companies import ALL_COMPANIES, CONSULTING_COMPANIES, TECH_COMPANIES, get_company
from backend.scraper.engine import GeneralizedScraper
from backend.normalizer.pipeline import NormalizationPipeline
from backend.database.repository import JobRepository
from backend.analysis.trends import TrendAnalyzer
from backend.export.api_generator import APIGenerator


def parse_args():
    p = argparse.ArgumentParser(description="AI Job Market Trend Tracker")
    p.add_argument("--company", type=str, help="Scrape a single company by slug")
    p.add_argument("--sector", choices=["consulting", "tech"], help="Scrape one sector")
    p.add_argument("--generate-only", action="store_true",
                   help="Skip scraping, only regenerate JSON from DB")
    p.add_argument("--list-companies", action="store_true", help="List configured companies")
    return p.parse_args()


def resolve_companies(args):
    if args.company:
        try:
            return [get_company(args.company)]
        except KeyError:
            print(f"Unknown company slug: {args.company}")
            print("Available:", ", ".join(c.slug for c in ALL_COMPANIES))
            sys.exit(1)
    if args.sector == "consulting":
        return CONSULTING_COMPANIES
    if args.sector == "tech":
        return TECH_COMPANIES
    return ALL_COMPANIES


def main():
    args = parse_args()
    settings = Settings()

    if args.list_companies:
        print("Consulting:")
        for c in CONSULTING_COMPANIES:
            print(f"  {c.slug:20s} {c.name}")
        print("Tech:")
        for c in TECH_COMPANIES:
            print(f"  {c.slug:20s} {c.name}")
        return

    repo = JobRepository(settings.db_path)

    if not args.generate_only:
        companies = resolve_companies(args)
        scraper = GeneralizedScraper(settings.firecrawl_api_key, settings.rate_limit_rpm)
        pipeline = NormalizationPipeline()

        print("=" * 60)
        print("AI Job Market Trend Tracker")
        print(f"Scraping {len(companies)} companies")
        print("=" * 60)

        for config in companies:
            company_id = repo.upsert_company(config)
            run_id = repo.start_scrape_run(company_id)

            try:
                raw_jobs, pages = scraper.scrape_company(config)
                inserted = 0
                for raw in raw_jobs:
                    normalized = pipeline.normalize(raw, company_id)
                    repo.upsert_job(normalized, run_id)
                    inserted += 1

                repo.mark_stale_jobs(company_id)
                repo.complete_scrape_run(run_id, "completed", pages=pages, jobs=inserted)
                print(f"  [{config.name}] Done — {inserted} jobs stored")

            except Exception as e:
                repo.complete_scrape_run(run_id, "failed", error=str(e))
                print(f"  [{config.name}] FAILED: {e}")

        # Compute daily metrics
        print("\nComputing daily metrics...")
        TrendAnalyzer(repo).compute_daily_metrics()

    # Generate JSON API files
    print("\nGenerating dashboard JSON files...")
    generator = APIGenerator(repo, settings.api_output_dir)
    generator.generate_all()

    # Summary
    summary = repo.get_company_summary()
    total = sum(s["active_jobs"] for s in summary)
    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total} active jobs across {len(summary)} companies")
    for s in summary:
        print(f"  {s['name']:20s} {s['active_jobs']:5d} active jobs ({s['sector']})")
    print("=" * 60)

    repo.close()


if __name__ == "__main__":
    main()
