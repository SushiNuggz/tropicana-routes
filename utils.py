import re
import math

STREET_SUFFIXES = {
    'AVE', 'RD', 'ST', 'BLVD', 'DR', 'HWY', 'WAY', 'LN', 'CT', 'PL', 'TER',
    'PKWY', 'TRL', 'STE', 'BOX', 'FM', 'IH', 'HIGHWAY', 'BOULEVARD', 'STREET',
    'AVENUE', 'DRIVE', 'ROAD', 'LANE', 'PLACE', 'COURT', 'CIRCLE', 'CIR',
    'TRAIL', 'N', 'S', 'E', 'W', 'NW', 'NE', 'SE', 'SW', 'SORT', 'REGIONAL',
    'AIRPORT', 'INTERMODAL', 'DISTRIBUTION', 'MANUFACTURERS', 'PRODUCTION',
    'COMMERCE', 'CENTER', 'CROSSROADS', 'VETERANS',
}

STATE_COORDS = {
    'AL': (32.7, -86.8), 'AR': (34.8, -92.2), 'AZ': (34.3, -111.1),
    'CA': (36.8, -119.4), 'CO': (39.1, -105.4), 'CT': (41.6, -72.7),
    'DE': (39.0, -75.5), 'FL': (27.8, -81.6), 'GA': (32.2, -82.9),
    'IA': (42.0, -93.2), 'ID': (44.4, -114.1), 'IL': (40.0, -89.2),
    'IN': (39.8, -86.2), 'KS': (38.5, -98.4), 'KY': (37.5, -85.3),
    'LA': (31.2, -91.8), 'MA': (42.2, -71.5), 'MD': (39.0, -76.8),
    'ME': (44.7, -69.4), 'MI': (43.3, -84.7), 'MN': (46.4, -93.1),
    'MO': (38.4, -92.3), 'MS': (32.7, -89.7), 'MT': (47.0, -109.6),
    'NC': (35.6, -79.8), 'ND': (47.5, -100.5), 'NE': (41.5, -99.9),
    'NH': (43.7, -71.6), 'NJ': (40.1, -74.5), 'NM': (34.5, -106.2),
    'NV': (39.3, -116.6), 'NY': (42.9, -75.5), 'OH': (40.3, -82.8),
    'OK': (35.6, -97.5), 'OR': (44.1, -120.5), 'PA': (40.9, -77.8),
    'RI': (41.7, -71.5), 'SC': (33.8, -80.9), 'SD': (44.4, -100.3),
    'TN': (35.9, -86.4), 'TX': (31.5, -99.3), 'UT': (39.3, -111.1),
    'VA': (37.5, -79.4), 'VT': (44.1, -72.7), 'WA': (47.4, -121.5),
    'WI': (44.3, -89.6), 'WV': (38.7, -80.6), 'WY': (43.0, -107.6),
}


def extract_city(address, state):
    """Extract the city name from a Tropicana address string.
    Format: ' 123 STREET NAME CITY STATE ZIP USA '
    """
    s = address.strip().upper()
    s = re.sub(r'\s+USA\s*$', '', s)
    s = re.sub(r'\s+\d{5}(-\d{4})?\s*$', '', s)
    s = re.sub(rf'\s+{re.escape(state.upper())}\s*$', '', s)
    s = s.strip()

    words = s.split()
    city_words = []
    for w in reversed(words):
        if not re.match(r'^[A-Z]+$', w):
            break
        if w in STREET_SUFFIXES:
            break
        city_words.insert(0, w)

    if city_words:
        return ' '.join(city_words).title()
    return words[-1].title() if words else 'Unknown'


def geo_distance(state1, state2):
    """Approximate distance between two states using lat/lon centroids."""
    default = (39.5, -98.4)
    c1 = STATE_COORDS.get(state1.upper(), default)
    c2 = STATE_COORDS.get(state2.upper(), default)
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
