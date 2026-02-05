#!/usr/bin/env python3
"""
Capgemini Invent – Data & AI (North America) Job Scraper
Uses Firecrawl to crawl the Capgemini careers site and filter for
Invent Data & AI roles in North America.
"""

import json
import csv
import re
import os
import sys
from datetime import datetime
from firecrawl import FirecrawlApp

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "fc-64580eaba63647c789cafebb9c1e37e2")
CAREERS_URL = "https://www.capgemini.com/careers/job-search/"

# Keywords used to identify relevant roles (case-insensitive)
KEYWORDS_MUST = ["invent"]                         # Must contain at least one
KEYWORDS_DOMAIN = ["data", "ai", "artificial intelligence", "machine learning",
                   "analytics", "data science", "data engineer", "gen ai",
                   "generative ai", "llm"]          # Must contain at least one
KEYWORDS_REGION = ["north america", "united states", "usa", "us", "canada",
                   "new york", "chicago", "atlanta", "dallas", "houston",
                   "san francisco", "los angeles", "seattle", "boston",
                   "washington", "toronto", "montreal", "detroit", "denver",
                   "charlotte", "philadelphia", "miami", "austin", "raleigh",
                   "minneapolis", "columbus", "pittsburgh", "tampa",
                   "remote - us", "remote - north america"]

OUTPUT_JSON = "results/jobs.json"
OUTPUT_CSV = "results/jobs.csv"


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """Return True if *text* contains at least one keyword (case-insensitive)."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def extract_jobs_from_markdown(markdown: str, source_url: str) -> list[dict]:
    """
    Best-effort extraction of individual job postings from a markdown page.
    Capgemini's job search pages typically list jobs as repeated blocks.
    """
    jobs = []
    # Try to split on common heading patterns that delimit individual jobs
    # Pattern: lines that look like job titles (short, often a heading)
    blocks = re.split(r'\n(?=#{1,3}\s)', markdown)
    if len(blocks) <= 1:
        # Fallback: treat the whole page as one block
        blocks = [markdown]

    for block in blocks:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        title = lines[0].lstrip("#").strip()
        body = "\n".join(lines[1:]) if len(lines) > 1 else ""
        full_text = f"{title} {body}"

        # Extract any URLs in the block
        urls = re.findall(r'https?://[^\s\)]+', block)
        job_url = urls[0] if urls else source_url

        # Try to find location
        loc_match = re.search(r'(?:location|city|region|office)[:\s]+([^\n|]+)', body, re.I)
        location = loc_match.group(1).strip() if loc_match else ""

        jobs.append({
            "title": title,
            "location": location,
            "url": job_url,
            "full_text": full_text[:1000],
            "source_page": source_url,
        })
    return jobs


def filter_jobs(jobs: list[dict]) -> list[dict]:
    """Keep only jobs that match Invent + Data/AI + North America criteria."""
    filtered = []
    for job in jobs:
        text = f"{job['title']} {job['location']} {job['full_text']}"
        if (matches_keywords(text, KEYWORDS_MUST)
                and matches_keywords(text, KEYWORDS_DOMAIN)
                and matches_keywords(text, KEYWORDS_REGION)):
            filtered.append(job)
    return filtered


def save_results(jobs: list[dict]) -> None:
    os.makedirs("results", exist_ok=True)

    # JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"[+] Saved {len(jobs)} jobs to {OUTPUT_JSON}")

    # CSV
    if jobs:
        fieldnames = ["title", "location", "url", "source_page"]
        with open(OUTPUT_CSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(jobs)
        print(f"[+] Saved {len(jobs)} jobs to {OUTPUT_CSV}")


def main():
    print("=" * 60)
    print("Capgemini Invent – Data & AI Job Scraper (North America)")
    print("=" * 60)

    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    # ------------------------------------------------------------------
    # Step 1: Map the careers site to discover all job-related URLs
    # ------------------------------------------------------------------
    print("\n[1/4] Mapping Capgemini careers site...")
    map_result = app.map(
        CAREERS_URL,
        search="invent data ai",
        limit=200,
    )

    links = map_result.links if hasattr(map_result, "links") else []
    print(f"      Found {len(links)} links on the careers site")

    # Keep only links that look like job postings or search results
    job_links = [
        link for link in links
        if any(seg in link.lower() for seg in ["/job/", "/jobs/", "job-search", "career"])
    ]
    # Also include the main search URL itself
    if CAREERS_URL not in job_links:
        job_links.insert(0, CAREERS_URL)

    print(f"      Filtered to {len(job_links)} career-related links")

    # ------------------------------------------------------------------
    # Step 2: Crawl the careers section
    # ------------------------------------------------------------------
    print("\n[2/4] Crawling careers pages (this may take a minute)...")
    crawl_result = app.crawl(
        CAREERS_URL,
        include_paths=["/careers/*", "/jobs/*", "/job/*"],
        limit=100,
        max_discovery_depth=3,
    )

    crawled_docs = crawl_result.data if hasattr(crawl_result, "data") else []
    print(f"      Crawled {len(crawled_docs)} pages")

    # ------------------------------------------------------------------
    # Step 3: Scrape individual mapped links not already crawled
    # ------------------------------------------------------------------
    crawled_urls = {doc.url for doc in crawled_docs if hasattr(doc, "url")}
    extra_links = [l for l in job_links if l not in crawled_urls][:20]  # cap at 20

    if extra_links:
        print(f"\n[3/4] Scraping {len(extra_links)} additional mapped links...")
        for i, link in enumerate(extra_links, 1):
            try:
                doc = app.scrape(link, formats=["markdown"])
                crawled_docs.append(doc)
                print(f"      [{i}/{len(extra_links)}] {link}")
            except Exception as e:
                print(f"      [{i}/{len(extra_links)}] SKIP {link}: {e}")
    else:
        print("\n[3/4] No additional links to scrape.")

    # ------------------------------------------------------------------
    # Step 4: Extract & filter jobs
    # ------------------------------------------------------------------
    print("\n[4/4] Extracting and filtering jobs...")
    all_jobs: list[dict] = []
    for doc in crawled_docs:
        md = doc.markdown if hasattr(doc, "markdown") else ""
        url = doc.url if hasattr(doc, "url") else (
            doc.metadata.get("url", "") if hasattr(doc, "metadata") and doc.metadata else ""
        )
        if md:
            all_jobs.extend(extract_jobs_from_markdown(md, url))

    print(f"      Extracted {len(all_jobs)} total job blocks")

    filtered = filter_jobs(all_jobs)
    print(f"      Matched {len(filtered)} Invent Data & AI (North America) roles")

    # Deduplicate by URL
    seen = set()
    unique = []
    for job in filtered:
        key = (job["title"], job["url"])
        if key not in seen:
            seen.add(key)
            unique.append(job)
    filtered = unique
    print(f"      {len(filtered)} unique roles after dedup")

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------
    save_results(filtered)

    # Print summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {len(filtered)} matching roles found")
    print("=" * 60)
    for i, job in enumerate(filtered, 1):
        print(f"\n  {i}. {job['title']}")
        if job["location"]:
            print(f"     Location: {job['location']}")
        print(f"     URL: {job['url']}")

    if not filtered:
        print("\n  No exact matches found. Try broadening the keyword filters")
        print("  in the configuration section at the top of scraper.py.")
        print("\n  All crawled content has been saved — check results/jobs.json")
        # Save all extracted jobs anyway for manual review
        save_results(all_jobs)
        print(f"  (saved all {len(all_jobs)} extracted blocks for manual review)")

    return filtered


if __name__ == "__main__":
    jobs = main()
    sys.exit(0 if jobs else 1)
