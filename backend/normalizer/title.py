import re


ABBREVIATIONS = {
    r'\bSr\.?\b': 'Senior',
    r'\bJr\.?\b': 'Junior',
    r'\bMgr\.?\b': 'Manager',
    r'\bDir\.?\b': 'Director',
    r'\bEngr\.?\b': 'Engineer',
    r'\bAssoc\.?\b': 'Associate',
    r'\bAdmin\.?\b': 'Administrator',
    r'\bDev\.?\b': 'Developer',
    r'\bOps\.?\b': 'Operations',
    r'\bVP\b': 'Vice President',
    r'\bSVP\b': 'Senior Vice President',
    r'\bEVP\b': 'Executive Vice President',
}

STRIP_PATTERNS = [
    r'\(?\b[A-Z]{2,3}-\d{4,}\b\)?',   # Job IDs like (JR-12345)
    r'\(\d{5,}\)',                       # Numeric IDs like (123456)
    r'\s*[-–]\s*\d{6,}',               # Trailing IDs
    r'\s*\|\s*.*$',                     # Pipe-separated metadata
    r'^\s*[-–]\s*',                     # Leading dashes
]


def normalize_title(raw: str) -> str:
    title = raw.strip()
    for pattern in STRIP_PATTERNS:
        title = re.sub(pattern, '', title)
    for pattern, replacement in ABBREVIATIONS.items():
        title = re.sub(pattern, replacement, title, flags=re.I)
    title = re.sub(r'\s+', ' ', title).strip()
    # Title case, but keep acronyms uppercase
    words = []
    for word in title.split():
        if word.isupper() and len(word) > 1:
            words.append(word)
        else:
            words.append(word.capitalize() if word.islower() else word)
    return ' '.join(words)
