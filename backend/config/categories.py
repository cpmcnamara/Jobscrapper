from dataclasses import dataclass, field


@dataclass
class JobCategory:
    id: str
    name: str
    keywords_strong: list[str] = field(default_factory=list)
    keywords_weak: list[str] = field(default_factory=list)
    exclude_keywords: list[str] = field(default_factory=list)


CATEGORIES = [
    JobCategory(
        id="ai_strategy",
        name="AI / Data Strategy",
        keywords_strong=[
            "ai strategy", "data strategy", "chief data officer",
            "ai transformation", "analytics strategy", "data officer",
            "ai advisor", "ai roadmap", "digital transformation ai",
            "ai governance", "responsible ai", "ai ethics",
        ],
        keywords_weak=[
            "strategy", "roadmap", "transformation", "advisory",
            "digital", "governance",
        ],
        exclude_keywords=["software engineer", "developer", "devops"],
    ),
    JobCategory(
        id="data_readiness",
        name="Data Readiness / Engineering / Governance",
        keywords_strong=[
            "data engineer", "data governance", "data quality",
            "data pipeline", "data platform", "data architect",
            "etl", "data lakehouse", "data mesh", "data catalog",
            "data steward", "master data", "data integration",
            "data warehouse", "data ops", "dataops",
        ],
        keywords_weak=[
            "data", "pipeline", "warehouse", "catalog", "ingestion",
            "spark", "airflow", "dbt",
        ],
        exclude_keywords=[],
    ),
    JobCategory(
        id="ai_ml_engineering",
        name="AI / ML Engineering",
        keywords_strong=[
            "machine learning engineer", "ml engineer", "ai engineer",
            "mlops", "deep learning", "computer vision", "nlp engineer",
            "ml platform", "ml infrastructure", "applied scientist",
            "research scientist", "ai researcher",
        ],
        keywords_weak=[
            "machine learning", "model training", "inference",
            "pytorch", "tensorflow", "neural network",
        ],
        exclude_keywords=[],
    ),
    JobCategory(
        id="domain_ai",
        name="Business Context / Domain AI",
        keywords_strong=[
            "ai consultant", "business analyst ai", "domain ai",
            "applied ai", "ai solutions architect", "ai product manager",
            "ai business partner", "analytics consultant",
            "data science consultant", "ai use case",
        ],
        keywords_weak=[
            "consultant", "business analyst", "solutions architect",
            "product manager", "use case",
        ],
        exclude_keywords=[],
    ),
    JobCategory(
        id="genai_llm",
        name="Gen AI / LLM",
        keywords_strong=[
            "generative ai", "gen ai", "genai", "llm",
            "large language model", "prompt engineer",
            "foundation model", "rag", "chatbot developer",
            "conversational ai", "ai agent",
        ],
        keywords_weak=[
            "gpt", "claude", "langchain", "vector database",
            "embedding", "fine-tuning", "retrieval augmented",
        ],
        exclude_keywords=[],
    ),
]
