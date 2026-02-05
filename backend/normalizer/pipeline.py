from backend.normalizer.title import normalize_title
from backend.normalizer.location import normalize_location
from backend.normalizer.seniority import extract_seniority
from backend.normalizer.categorizer import categorize_job
from backend.scraper.engine import RawJob


class NormalizationPipeline:
    def normalize(self, raw: RawJob, company_id: int) -> dict:
        title_norm = normalize_title(raw.title)
        loc = normalize_location(raw.location)
        seniority = extract_seniority(raw.title)
        category = categorize_job(raw.title, raw.description_snippet)

        return {
            "company_id": company_id,
            "company_slug": raw.company_slug,
            "external_id": raw.external_id,
            "title_raw": raw.title,
            "title_normalized": title_norm,
            "category": category,
            "seniority": seniority,
            "location_raw": raw.location,
            "location_city": loc.city,
            "location_state": loc.state,
            "location_country": loc.country,
            "is_remote": loc.is_remote,
            "url": raw.url,
            "description_snippet": raw.description_snippet,
        }
