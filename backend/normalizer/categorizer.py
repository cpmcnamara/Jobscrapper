from backend.config.categories import CATEGORIES, JobCategory

STRONG_WEIGHT = 3
WEAK_WEIGHT = 1
MIN_SCORE = 3


def categorize_job(title: str, description: str = "") -> str:
    text = f"{title} {description}".lower()
    best_cat = "uncategorized"
    best_score = 0

    for cat in CATEGORIES:
        # Check excludes first
        if any(kw.lower() in text for kw in cat.exclude_keywords):
            continue

        score = 0
        for kw in cat.keywords_strong:
            if kw.lower() in text:
                score += STRONG_WEIGHT
        for kw in cat.keywords_weak:
            if kw.lower() in text:
                score += WEAK_WEIGHT

        if score > best_score and score >= MIN_SCORE:
            best_score = score
            best_cat = cat.id

    return best_cat
