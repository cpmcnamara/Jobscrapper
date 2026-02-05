import re

SENIORITY_RULES: list[tuple[str, list[str]]] = [
    ("c_level", [r'\bchief\b', r'\bCTO\b', r'\bCDO\b', r'\bCIO\b', r'\bCAO\b']),
    ("vp", [r'\bvice president\b', r'\bVP\b', r'\bSVP\b', r'\bEVP\b']),
    ("director", [r'\bdirector\b', r'\bhead of\b']),
    ("principal", [r'\bprincipal\b', r'\bdistinguished\b', r'\bfellow\b']),
    ("lead", [r'\blead\b', r'\bteam lead\b', r'\btech lead\b']),
    ("senior", [r'\bsenior\b', r'\bsr\.?\b', r'\bstaff\b', r'\biii\b']),
    ("junior", [r'\bjunior\b', r'\bjr\.?\b', r'\bentry\s+level\b',
                r'\bassociate\b', r'\banalyst\b', r'\bi\b(?=\s|$)']),
    ("intern", [r'\bintern\b', r'\binternship\b', r'\bco-?op\b']),
]


def extract_seniority(title: str) -> str:
    t = title.strip()
    for level, patterns in SENIORITY_RULES:
        for p in patterns:
            if re.search(p, t, re.I):
                return level
    return "mid"
