from dataclasses import dataclass, field


@dataclass
class CompanyConfig:
    name: str
    slug: str
    sector: str  # "consulting" | "tech"
    careers_url: str

    # Firecrawl parameters
    include_paths: list[str] = field(default_factory=list)
    search_query: str = "data ai machine learning"
    crawl_limit: int = 100
    max_depth: int = 3
    scrape_extra_limit: int = 20
