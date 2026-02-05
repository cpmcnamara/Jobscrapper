import re
from dataclasses import dataclass

US_STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}

CA_PROVINCES = {
    "ON": "Ontario", "QC": "Quebec", "BC": "British Columbia",
    "AB": "Alberta", "MB": "Manitoba", "SK": "Saskatchewan",
    "NS": "Nova Scotia", "NB": "New Brunswick", "NL": "Newfoundland",
    "PE": "Prince Edward Island",
}

REMOTE_PATTERNS = [
    r'\bremote\b', r'\bwork from home\b', r'\bwfh\b',
    r'\bvirtual\b', r'\btelecommute\b',
]

STATE_ABBREV_TO_FULL = {**US_STATES, **CA_PROVINCES}
FULL_TO_ABBREV = {v.lower(): k for k, v in STATE_ABBREV_TO_FULL.items()}


@dataclass
class LocationInfo:
    city: str
    state: str
    country: str
    is_remote: bool


def normalize_location(raw: str) -> LocationInfo:
    if not raw:
        return LocationInfo("", "", "", False)

    text = raw.strip()
    is_remote = any(re.search(p, text, re.I) for p in REMOTE_PATTERNS)

    # Clean remote prefix/suffix
    cleaned = re.sub(r'\b(remote|virtual|wfh|telecommute)\s*[-–]?\s*', '', text, flags=re.I).strip()
    cleaned = re.sub(r'\s*[-–]\s*(remote|virtual|wfh|telecommute)\b', '', cleaned, flags=re.I).strip()

    if not cleaned:
        return LocationInfo("", "", "United States" if "us" in text.lower() else "", is_remote)

    parts = [p.strip() for p in cleaned.split(",")]

    city = ""
    state = ""
    country = ""

    if len(parts) >= 3:
        city, state, country = parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        city = parts[0]
        second = parts[1].strip()
        if second.upper() in US_STATES:
            state = US_STATES[second.upper()]
            country = "United States"
        elif second.upper() in CA_PROVINCES:
            state = CA_PROVINCES[second.upper()]
            country = "Canada"
        elif second.lower() in FULL_TO_ABBREV:
            state = second.title()
            country = "United States" if FULL_TO_ABBREV[second.lower()] in US_STATES else "Canada"
        else:
            country = second
    elif len(parts) == 1:
        token = parts[0]
        if token.upper() in US_STATES:
            state = US_STATES[token.upper()]
            country = "United States"
        elif token.lower() in FULL_TO_ABBREV:
            state = token.title()
            country = "United States" if FULL_TO_ABBREV[token.lower()] in US_STATES else "Canada"
        elif token.lower() in ("us", "usa", "united states"):
            country = "United States"
        elif token.lower() in ("canada", "ca"):
            country = "Canada"
        else:
            city = token

    return LocationInfo(
        city=city.strip().title() if city else "",
        state=state.strip(),
        country=country.strip().title() if country else "",
        is_remote=is_remote,
    )
