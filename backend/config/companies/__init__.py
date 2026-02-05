from backend.config.companies.base import CompanyConfig
from backend.config.companies.consulting import CONSULTING_COMPANIES
from backend.config.companies.tech import TECH_COMPANIES

ALL_COMPANIES: list[CompanyConfig] = CONSULTING_COMPANIES + TECH_COMPANIES

_SLUG_MAP = {c.slug: c for c in ALL_COMPANIES}


def get_company(slug: str) -> CompanyConfig:
    return _SLUG_MAP[slug]


__all__ = [
    "CompanyConfig", "ALL_COMPANIES", "CONSULTING_COMPANIES",
    "TECH_COMPANIES", "get_company",
]
