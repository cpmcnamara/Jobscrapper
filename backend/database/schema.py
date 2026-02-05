SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS companies (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    slug        TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    sector      TEXT NOT NULL CHECK(sector IN ('consulting', 'tech')),
    careers_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scrape_runs (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id     INTEGER NOT NULL REFERENCES companies(id),
    started_at     TEXT NOT NULL,
    completed_at   TEXT,
    status         TEXT NOT NULL DEFAULT 'running'
                   CHECK(status IN ('running','completed','failed')),
    pages_crawled  INTEGER DEFAULT 0,
    jobs_found     INTEGER DEFAULT 0,
    error_message  TEXT
);

CREATE TABLE IF NOT EXISTS jobs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          INTEGER NOT NULL REFERENCES companies(id),
    fingerprint         TEXT NOT NULL UNIQUE,
    external_id         TEXT,
    title_raw           TEXT NOT NULL,
    title_normalized    TEXT NOT NULL,
    category            TEXT NOT NULL,
    seniority           TEXT,
    location_raw        TEXT,
    location_city       TEXT,
    location_state      TEXT,
    location_country    TEXT,
    is_remote           INTEGER DEFAULT 0,
    url                 TEXT,
    description_snippet TEXT,
    first_seen_at       TEXT NOT NULL,
    last_seen_at        TEXT NOT NULL,
    is_active           INTEGER DEFAULT 1,
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS job_sightings (
    job_id        INTEGER NOT NULL REFERENCES jobs(id),
    scrape_run_id INTEGER NOT NULL REFERENCES scrape_runs(id),
    PRIMARY KEY (job_id, scrape_run_id)
);

CREATE TABLE IF NOT EXISTS daily_metrics (
    date              TEXT NOT NULL,
    company_id        INTEGER NOT NULL REFERENCES companies(id),
    category          TEXT NOT NULL,
    seniority         TEXT DEFAULT '',
    location_country  TEXT DEFAULT '',
    active_jobs       INTEGER NOT NULL DEFAULT 0,
    new_jobs          INTEGER NOT NULL DEFAULT 0,
    closed_jobs       INTEGER NOT NULL DEFAULT 0,
    UNIQUE(date, company_id, category, seniority, location_country)
);

CREATE INDEX IF NOT EXISTS idx_jobs_company    ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_category   ON jobs(category);
CREATE INDEX IF NOT EXISTS idx_jobs_active     ON jobs(is_active);
CREATE INDEX IF NOT EXISTS idx_jobs_last_seen  ON jobs(last_seen_at);
CREATE INDEX IF NOT EXISTS idx_jobs_fingerprint ON jobs(fingerprint);
CREATE INDEX IF NOT EXISTS idx_metrics_date    ON daily_metrics(date);
CREATE INDEX IF NOT EXISTS idx_metrics_company ON daily_metrics(company_id);
"""
