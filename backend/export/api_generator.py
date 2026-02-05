import json
import os
from collections import defaultdict
from datetime import datetime, timezone

from backend.database.repository import JobRepository
from backend.config.categories import CATEGORIES


class APIGenerator:
    def __init__(self, repo: JobRepository, output_dir: str):
        self.repo = repo
        self.output_dir = output_dir

    def generate_all(self):
        os.makedirs(self.output_dir, exist_ok=True)
        self._generate_metadata()
        self._generate_overview()
        self._generate_trends()
        self._generate_companies()
        self._generate_categories()
        self._generate_geo()
        self._generate_jobs()
        print(f"  API JSON files written to {self.output_dir}")

    def _write(self, filename: str, data: dict | list):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _generate_metadata(self):
        self._write("metadata.json", {
            "lastUpdated": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
        })

    def _generate_overview(self):
        jobs = self.repo.get_active_jobs()
        cat_counts = defaultdict(int)
        sector_counts = defaultdict(int)
        company_counts = defaultdict(int)
        for j in jobs:
            cat_counts[j["category"]] += 1
            sector_counts[j["sector"]] += 1
            company_counts[j["company_name"]] += 1

        top_cat = max(cat_counts, key=cat_counts.get, default="N/A")
        top_company = max(company_counts, key=company_counts.get, default="N/A")
        cat_name_map = {c.id: c.name for c in CATEGORIES}

        self._write("overview.json", {
            "totalActiveJobs": len(jobs),
            "totalCompanies": len(company_counts),
            "topCategory": cat_name_map.get(top_cat, top_cat),
            "topCategoryId": top_cat,
            "consultingVsTech": {
                "consulting": sector_counts.get("consulting", 0),
                "tech": sector_counts.get("tech", 0),
            },
            "topGrowthCompany": top_company,
        })

    def _generate_trends(self):
        metrics = self.repo.get_daily_metrics()
        companies = {r["slug"]: r for r in self.repo.get_company_summary()}

        by_date: dict[str, dict] = defaultdict(lambda: {
            "total": 0,
            "byCategory": defaultdict(int),
            "bySector": defaultdict(int),
            "byCompany": defaultdict(int),
        })

        company_id_to_info = {}
        for row in self.repo.conn.execute("SELECT id, slug, sector FROM companies").fetchall():
            company_id_to_info[row["id"]] = {"slug": row["slug"], "sector": row["sector"]}

        for m in metrics:
            d = m["date"]
            info = company_id_to_info.get(m["company_id"], {})
            by_date[d]["total"] += m["active_jobs"]
            by_date[d]["byCategory"][m["category"]] += m["active_jobs"]
            by_date[d]["bySector"][info.get("sector", "unknown")] += m["active_jobs"]
            by_date[d]["byCompany"][info.get("slug", "unknown")] += m["active_jobs"]

        time_series = []
        for date in sorted(by_date.keys()):
            entry = by_date[date]
            time_series.append({
                "date": date,
                "total": entry["total"],
                "byCategory": dict(entry["byCategory"]),
                "bySector": dict(entry["bySector"]),
                "byCompany": dict(entry["byCompany"]),
            })

        self._write("trends.json", {"timeSeries": time_series})

    def _generate_companies(self):
        summary = self.repo.get_company_summary()
        jobs = self.repo.get_active_jobs()

        company_jobs: dict[str, list] = defaultdict(list)
        for j in jobs:
            company_jobs[j["company_slug"]].append(j)

        companies = []
        for s in summary:
            cjobs = company_jobs.get(s["slug"], [])
            by_cat = defaultdict(int)
            by_sen = defaultdict(int)
            top_titles: dict[str, int] = defaultdict(int)
            for j in cjobs:
                by_cat[j["category"]] += 1
                by_sen[j["seniority"] or "unknown"] += 1
                top_titles[j["title_normalized"]] += 1

            sorted_titles = sorted(top_titles.items(), key=lambda x: -x[1])[:10]
            companies.append({
                "slug": s["slug"],
                "name": s["name"],
                "sector": s["sector"],
                "totalActiveJobs": s["active_jobs"],
                "byCategory": dict(by_cat),
                "bySeniority": dict(by_sen),
                "topRoles": [{"title": t, "count": c} for t, c in sorted_titles],
            })

        self._write("companies.json", {"companies": companies})

    def _generate_categories(self):
        jobs = self.repo.get_active_jobs()
        cat_name_map = {c.id: c.name for c in CATEGORIES}

        by_cat: dict[str, list] = defaultdict(list)
        for j in jobs:
            by_cat[j["category"]].append(j)

        categories = []
        for cat_id, cat_jobs in by_cat.items():
            by_company = defaultdict(int)
            by_sen = defaultdict(int)
            top_titles: dict[str, int] = defaultdict(int)
            for j in cat_jobs:
                by_company[j["company_slug"]] += 1
                by_sen[j["seniority"] or "unknown"] += 1
                top_titles[j["title_normalized"]] += 1

            sorted_titles = sorted(top_titles.items(), key=lambda x: -x[1])[:10]
            categories.append({
                "id": cat_id,
                "name": cat_name_map.get(cat_id, cat_id),
                "totalJobs": len(cat_jobs),
                "byCompany": dict(by_company),
                "bySeniority": dict(by_sen),
                "topTitles": [{"title": t, "count": c} for t, c in sorted_titles],
            })

        self._write("categories.json", {"categories": categories})

    def _generate_geo(self):
        geo_data = self.repo.get_geo_distribution()
        locations = []
        remote_total = 0
        country_counts: dict[str, int] = defaultdict(int)

        for row in geo_data:
            locations.append({
                "country": row["location_country"] or "Unknown",
                "state": row["location_state"] or "",
                "city": row["location_city"] or "",
                "isRemote": bool(row["is_remote"]),
                "company": row["company_slug"],
                "category": row["category"],
                "count": row["count"],
            })
            if row["is_remote"]:
                remote_total += row["count"]
            country_counts[row["location_country"] or "Unknown"] += row["count"]

        top_countries = sorted(country_counts.items(), key=lambda x: -x[1])[:20]

        self._write("geo.json", {
            "locations": locations,
            "remoteTotal": remote_total,
            "topCountries": [{"country": c, "count": n} for c, n in top_countries],
        })

    def _generate_jobs(self):
        jobs = self.repo.get_active_jobs()
        output = []
        for j in jobs:
            output.append({
                "title": j["title_normalized"],
                "titleRaw": j["title_raw"],
                "company": j["company_name"],
                "companySlug": j["company_slug"],
                "sector": j["sector"],
                "category": j["category"],
                "seniority": j["seniority"] or "unknown",
                "city": j["location_city"] or "",
                "state": j["location_state"] or "",
                "country": j["location_country"] or "",
                "isRemote": bool(j["is_remote"]),
                "url": j["url"] or "",
                "firstSeen": j["first_seen_at"],
                "lastSeen": j["last_seen_at"],
            })
        self._write("jobs.json", {"jobs": output})
