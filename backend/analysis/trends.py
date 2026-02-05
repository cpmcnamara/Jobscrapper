from datetime import datetime, timezone

from backend.database.repository import JobRepository


class TrendAnalyzer:
    def __init__(self, repo: JobRepository):
        self.repo = repo

    def compute_daily_metrics(self, date: str | None = None):
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        rows = self.repo.conn.execute("""
            SELECT j.company_id, j.category, j.seniority, j.location_country,
                   COUNT(*) as active,
                   SUM(CASE WHEN j.first_seen_at >= ? THEN 1 ELSE 0 END) as new_today
            FROM jobs j
            WHERE j.is_active = 1
            GROUP BY j.company_id, j.category, j.seniority, j.location_country
        """, (date,)).fetchall()

        for row in rows:
            self.repo.save_daily_metrics(
                date=date,
                company_id=row["company_id"],
                category=row["category"],
                seniority=row["seniority"] or "",
                country=row["location_country"] or "",
                active=row["active"],
                new=row["new_today"],
                closed=0,
            )
