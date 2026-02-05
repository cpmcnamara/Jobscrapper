import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

from firecrawl import FirecrawlApp

from backend.config.companies.base import CompanyConfig


@dataclass
class RawJob:
    title: str
    location: str
    url: str
    description_snippet: str
    source_page: str
    company_slug: str
    external_id: str | None = None
    scraped_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GeneralizedScraper:
    def __init__(self, api_key: str, rate_limit_rpm: int = 20):
        self.app = FirecrawlApp(api_key=api_key)
        self.min_interval = 60.0 / rate_limit_rpm
        self._last_call = 0.0

    def _rate_limit(self):
        elapsed = time.time() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.time()

    def scrape_company(self, config: CompanyConfig) -> tuple[list[RawJob], int]:
        """Full pipeline for one company. Returns (raw_jobs, pages_crawled)."""
        print(f"\n  [{config.name}] Mapping site...")
        links = self._map_site(config)
        print(f"  [{config.name}] Found {len(links)} links")

        print(f"  [{config.name}] Crawling pages...")
        documents = self._crawl_pages(config)
        print(f"  [{config.name}] Crawled {len(documents)} pages")

        crawled_urls = set()
        for doc in documents:
            url = getattr(doc, "url", None) or (
                doc.metadata.get("url", "") if hasattr(doc, "metadata") and doc.metadata else ""
            )
            if url:
                crawled_urls.add(url)

        extra = [l for l in links if l not in crawled_urls][:config.scrape_extra_limit]
        if extra:
            print(f"  [{config.name}] Scraping {len(extra)} extra links...")
            documents.extend(self._scrape_extra(extra))

        pages = len(documents)
        jobs = self._extract_all(documents, config)
        print(f"  [{config.name}] Extracted {len(jobs)} job blocks from {pages} pages")
        return jobs, pages

    def _map_site(self, config: CompanyConfig) -> list[str]:
        self._rate_limit()
        try:
            result = self.app.map(
                config.careers_url,
                search=config.search_query,
                limit=200,
            )
            links = result.links if hasattr(result, "links") else []
            return [l for l in links if any(
                seg in l.lower()
                for seg in ["/job", "/career", "/search", "/position", "/opening"]
            )]
        except Exception as e:
            print(f"  [{config.name}] Map failed: {e}")
            return []

    def _crawl_pages(self, config: CompanyConfig) -> list:
        self._rate_limit()
        try:
            result = self.app.crawl(
                config.careers_url,
                include_paths=config.include_paths or None,
                limit=config.crawl_limit,
                max_discovery_depth=config.max_depth,
            )
            return list(result.data) if hasattr(result, "data") else []
        except Exception as e:
            print(f"  [{config.name}] Crawl failed: {e}")
            return []

    def _scrape_extra(self, links: list[str]) -> list:
        docs = []
        for link in links:
            self._rate_limit()
            try:
                doc = self.app.scrape(link, formats=["markdown"])
                docs.append(doc)
            except Exception as e:
                print(f"    SKIP {link}: {e}")
        return docs

    def _extract_all(self, documents: list, config: CompanyConfig) -> list[RawJob]:
        jobs: list[RawJob] = []
        for doc in documents:
            md = getattr(doc, "markdown", "") or ""
            url = getattr(doc, "url", None) or (
                doc.metadata.get("url", "") if hasattr(doc, "metadata") and doc.metadata else ""
            )
            if not md:
                continue
            jobs.extend(self._extract_jobs(md, url, config))
        return jobs

    def _extract_jobs(self, markdown: str, source_url: str, config: CompanyConfig) -> list[RawJob]:
        blocks = re.split(r'\n(?=#{1,3}\s)', markdown)
        if len(blocks) <= 1:
            blocks = re.split(r'\n(?=\*\*[A-Z])', markdown)
        if len(blocks) <= 1:
            blocks = [markdown]

        jobs = []
        for block in blocks:
            lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
            if not lines:
                continue
            title = lines[0].lstrip("#").lstrip("*").strip().rstrip("*")
            if len(title) < 5 or len(title) > 200:
                continue
            body = "\n".join(lines[1:]) if len(lines) > 1 else ""

            urls = re.findall(r'https?://[^\s\)\]]+', block)
            job_url = urls[0] if urls else source_url

            loc_match = re.search(
                r'(?:location|city|region|office|where)[:\s]+([^\n|]+)', body, re.I
            )
            location = loc_match.group(1).strip() if loc_match else ""

            id_match = re.search(r'(?:job\s*id|req\s*id|reference)[:\s]*(\S+)', body, re.I)
            ext_id = id_match.group(1).strip() if id_match else None

            jobs.append(RawJob(
                title=title,
                location=location,
                url=job_url,
                description_snippet=body[:500],
                source_page=source_url,
                company_slug=config.slug,
                external_id=ext_id,
            ))
        return jobs
