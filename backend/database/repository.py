import hashlib
import sqlite3
from datetime import datetime, timezone

from backend.config.companies.base import CompanyConfig
from backend.database.connection import get_connection


def _fingerprint(company_slug: str, title_normalized: str, url: str) -> str:
    raw = f"{company_slug}|{title_normalized.lower()}|{url}".encode()
    return hashlib.sha256(raw).hexdigest()


class JobRepository:
    def __init__(self, db_path: str):
        self.conn = get_connection(db_path)

    def close(self):
        self.conn.close()

    # -- companies ----------------------------------------------------------

    def upsert_company(self, config: CompanyConfig) -> int:
        cur = self.conn.execute(
            "SELECT id FROM companies WHERE slug = ?", (config.slug,)
        )
        row = cur.fetchone()
        if row:
            return row["id"]
        self.conn.execute(
            "INSERT INTO companies (slug, name, sector, careers_url) VALUES (?,?,?,?)",
            (config.slug, config.name, config.sector, config.careers_url),
        )
        self.conn.commit()
        return self.conn.execute(
            "SELECT id FROM companies WHERE slug = ?", (config.slug,)
        ).fetchone()["id"]

    # -- scrape runs --------------------------------------------------------

    def start_scrape_run(self, company_id: int) -> int:
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            "INSERT INTO scrape_runs (company_id, started_at) VALUES (?,?)",
            (company_id, now),
        )
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def complete_scrape_run(
        self, run_id: int, status: str, pages: int = 0, jobs: int = 0, error: str = ""
    ):
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            """UPDATE scrape_runs
               SET completed_at=?, status=?, pages_crawled=?, jobs_found=?, error_message=?
               WHERE id=?""",
            (now, status, pages, jobs, error, run_id),
        )
        self.conn.commit()

    # -- jobs ---------------------------------------------------------------

    def upsert_job(self, job: dict, scrape_run_id: int) -> int:
        fp = _fingerprint(job["company_slug"], job["title_normalized"], job["url"])
        now = datetime.now(timezone.utc).isoformat()

        existing = self.conn.execute(
            "SELECT id FROM jobs WHERE fingerprint = ?", (fp,)
        ).fetchone()

        if existing:
            job_id = existing["id"]
            self.conn.execute(
                "UPDATE jobs SET last_seen_at=?, is_active=1 WHERE id=?",
                (now, job_id),
            )
        else:
            self.conn.execute(
                """INSERT INTO jobs
                   (company_id, fingerprint, external_id, title_raw, title_normalized,
                    category, seniority, location_raw, location_city, location_state,
                    location_country, is_remote, url, description_snippet,
                    first_seen_at, last_seen_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    job["company_id"], fp, job.get("external_id"),
                    job["title_raw"], job["title_normalized"],
                    job["category"], job["seniority"],
                    job["location_raw"], job["location_city"],
                    job["location_state"], job["location_country"],
                    int(job["is_remote"]), job["url"],
                    job.get("description_snippet", "")[:1000],
                    now, now,
                ),
            )
            job_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        # Record sighting
        self.conn.execute(
            "INSERT OR IGNORE INTO job_sightings (job_id, scrape_run_id) VALUES (?,?)",
            (job_id, scrape_run_id),
        )
        self.conn.commit()
        return job_id

    def mark_stale_jobs(self, company_id: int, days_threshold: int = 14):
        cutoff = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            """UPDATE jobs SET is_active = 0
               WHERE company_id = ? AND is_active = 1
               AND julianday(?) - julianday(last_seen_at) > ?""",
            (company_id, cutoff, days_threshold),
        )
        self.conn.commit()

    # -- queries for analysis -----------------------------------------------

    def get_active_jobs(self, filters: dict | None = None) -> list[dict]:
        sql = """
            SELECT j.*, c.name as company_name, c.slug as company_slug, c.sector
            FROM jobs j JOIN companies c ON j.company_id = c.id
            WHERE j.is_active = 1
        """
        params: list = []
        if filters:
            if filters.get("company"):
                sql += " AND c.slug = ?"
                params.append(filters["company"])
            if filters.get("sector"):
                sql += " AND c.sector = ?"
                params.append(filters["sector"])
            if filters.get("category"):
                sql += " AND j.category = ?"
                params.append(filters["category"])
        sql += " ORDER BY j.last_seen_at DESC"
        rows = self.conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def get_all_jobs(self) -> list[dict]:
        rows = self.conn.execute("""
            SELECT j.*, c.name as company_name, c.slug as company_slug, c.sector
            FROM jobs j JOIN companies c ON j.company_id = c.id
            ORDER BY j.last_seen_at DESC
        """).fetchall()
        return [dict(r) for r in rows]

    def get_company_summary(self) -> list[dict]:
        rows = self.conn.execute("""
            SELECT c.slug, c.name, c.sector,
                   COUNT(CASE WHEN j.is_active=1 THEN 1 END) as active_jobs,
                   COUNT(*) as total_jobs
            FROM companies c LEFT JOIN jobs j ON c.id = j.company_id
            GROUP BY c.id ORDER BY active_jobs DESC
        """).fetchall()
        return [dict(r) for r in rows]

    def get_category_breakdown(self) -> list[dict]:
        rows = self.conn.execute("""
            SELECT j.category, c.sector,
                   COUNT(*) as count
            FROM jobs j JOIN companies c ON j.company_id = c.id
            WHERE j.is_active = 1
            GROUP BY j.category, c.sector
        """).fetchall()
        return [dict(r) for r in rows]

    def get_seniority_breakdown(self) -> list[dict]:
        rows = self.conn.execute("""
            SELECT j.seniority, j.category,
                   COUNT(*) as count
            FROM jobs j WHERE j.is_active = 1
            GROUP BY j.seniority, j.category
        """).fetchall()
        return [dict(r) for r in rows]

    def get_geo_distribution(self) -> list[dict]:
        rows = self.conn.execute("""
            SELECT j.location_country, j.location_state, j.location_city,
                   j.is_remote, c.slug as company_slug, j.category,
                   COUNT(*) as count
            FROM jobs j JOIN companies c ON j.company_id = c.id
            WHERE j.is_active = 1
            GROUP BY j.location_country, j.location_state, j.location_city,
                     j.is_remote, c.slug, j.category
        """).fetchall()
        return [dict(r) for r in rows]

    def get_daily_metrics(self, start_date: str = "", end_date: str = "") -> list[dict]:
        sql = "SELECT * FROM daily_metrics WHERE 1=1"
        params: list = []
        if start_date:
            sql += " AND date >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND date <= ?"
            params.append(end_date)
        sql += " ORDER BY date"
        rows = self.conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def save_daily_metrics(self, date: str, company_id: int, category: str,
                           seniority: str, country: str,
                           active: int, new: int, closed: int):
        self.conn.execute(
            """INSERT OR REPLACE INTO daily_metrics
               (date, company_id, category, seniority, location_country,
                active_jobs, new_jobs, closed_jobs)
               VALUES (?,?,?,?,?,?,?,?)""",
            (date, company_id, category, seniority or "", country or "",
             active, new, closed),
        )
        self.conn.commit()
