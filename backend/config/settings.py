import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
API_OUTPUT_DIR = ROOT_DIR / "dashboard" / "public" / "data"


class Settings:
    def __init__(self):
        self.firecrawl_api_key = os.getenv(
            "FIRECRAWL_API_KEY", "fc-64580eaba63647c789cafebb9c1e37e2"
        )
        self.db_path = str(DATA_DIR / "jobs.db")
        self.api_output_dir = str(API_OUTPUT_DIR)
        self.rate_limit_rpm = 20
