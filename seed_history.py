"""Seed the route history database with completed weeks of real data."""

from db import init_db, save_routes, route_exists_for_week

init_db()

# ─── Week of 5/30/2026 — Origin 3322 (Walnut, CA) ────────────────────────────
WEEK_530_3322 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Buckeye',        'state': 'AZ', 'dest_name': 'WALMART DC #6031G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Litchfield Park','state': 'AZ', 'dest_name': 'WALMART.COM SORT GLENDALE PHX1',     'pallets': 1, 'weight': 0},
            {'city': 'Plainview',      'state': 'TX', 'dest_name': 'WALMART DC #6012G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'New Braunfels',  'state': 'TX', 'dest_name': 'WALMART DC #6016G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Sealy',          'state': 'TX', 'dest_name': 'WALMART DC #7036G-GENERAL',          'pallets': 1, 'weight': 0},
        ],
        'rate': 3000,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Apple Valley', 'state': 'CA', 'dest_name': 'WALMART RDC 7033',          'pallets': 1, 'weight': 0},
            {'city': 'Sparks',       'state': 'NV', 'dest_name': 'WALMART.COM SORT JET NV1',  'pallets': 1, 'weight': 0},
            {'city': 'Grantsville',  'state': 'UT', 'dest_name': 'WALMART DC #7026G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Loveland',     'state': 'CO', 'dest_name': 'WALMART DC #6019G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2800,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Chino',           'state': 'CA', 'dest_name': 'WALMART.COM SORT CHINO LAX', 'pallets': 1, 'weight': 0},
            {'city': 'Porterville',     'state': 'CA', 'dest_name': 'WALMART DC #6021D-DSDC',     'pallets': 1, 'weight': 0},
            {'city': 'Red Bluff',       'state': 'CA', 'dest_name': 'WALMART DC #6026G-GENERAL',  'pallets': 1, 'weight': 0},
            {'city': 'South Hermiston', 'state': 'OR', 'dest_name': 'WALMART DC #6037D-DSDC',     'pallets': 1, 'weight': 0},
        ],
        'rate': 2900,
    },
]

# ─── Week of 5/30/2026 — Origin 3943 (Brockport, NY) ─────────────────────────
WEEK_530_3943 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Marcy',      'state': 'NY', 'dest_name': 'WALMART DC #6038D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Raymond',    'state': 'NH', 'dest_name': 'WALMART DC #6030D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Tobyhanna',  'state': 'PA', 'dest_name': 'WALMART DC #6080G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Bethlehem',  'state': 'PA', 'dest_name': 'WALMART DC #7356',          'pallets': 1, 'weight': 0},
            {'city': 'Smyrna',     'state': 'DE', 'dest_name': 'WALMART DC #7034G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 1300,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Troutman',   'state': 'NC', 'dest_name': 'WALMART.COM SORT TROUTMAN CLT1', 'pallets': 1, 'weight': 0},
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Alachua',    'state': 'FL', 'dest_name': 'WALMART DC #7035',               'pallets': 1, 'weight': 0},
            {'city': 'Brooksville','state': 'FL', 'dest_name': 'WALMART DC #6020G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Fort Pierce','state': 'FL', 'dest_name': 'WALMART DC #7038G-GENERAL',      'pallets': 1, 'weight': 0},
        ],
        'rate': 3900,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Mount Crawford','state': 'VA', 'dest_name': 'ARA@WALMART DC #7045-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Olive Branch',  'state': 'MS', 'dest_name': 'WALMART DC #4301',             'pallets': 1, 'weight': 0},
            {'city': 'Brookhaven',    'state': 'MS', 'dest_name': 'WALMART DC #6011G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Opelousas',     'state': 'LA', 'dest_name': 'WALMART DC #6048G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Palestine',     'state': 'TX', 'dest_name': 'WALMART DC #6036D-DSDC',       'pallets': 1, 'weight': 0},
        ],
        'rate': 2700,
    },
    {
        'truck_number': 4,
        'stops': [
            {'city': 'Grove City', 'state': 'OH', 'dest_name': 'WALMART DC #6024D-DSDC',              'pallets': 1, 'weight': 0},
            {'city': 'Ottawa',     'state': 'KS', 'dest_name': 'WALMART DC #6035G-GENERAL',           'pallets': 1, 'weight': 0},
            {'city': 'Searcy',     'state': 'AR', 'dest_name': 'WALMART DC #6018G-GENERAL',           'pallets': 1, 'weight': 0},
            {'city': 'Sanger',     'state': 'TX', 'dest_name': 'WALMART DC #6068G-GENERAL',           'pallets': 1, 'weight': 0},
            {'city': 'Lancaster',  'state': 'TX', 'dest_name': 'WALMART.COM SORT LANCASTER DFW5 WFS', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2700,
    },
    {
        'truck_number': 5,
        'stops': [
            {'city': 'Coldwater',    'state': 'MI', 'dest_name': 'WALMART DC #6043D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Joliet',       'state': 'IL', 'dest_name': 'WALMART.COM SORT JOLIET ORD1', 'pallets': 1, 'weight': 0},
            {'city': 'Spring Valley','state': 'IL', 'dest_name': 'WALMART DC #6092D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Beaver Dam',   'state': 'WI', 'dest_name': 'WALMART DC #7039-REGULAR',     'pallets': 1, 'weight': 0},
            {'city': 'Menomonie',    'state': 'WI', 'dest_name': 'WALMART DC #6025G-GENERAL',    'pallets': 1, 'weight': 0},
        ],
        'rate': 2100,
    },
    {
        'truck_number': 6,
        'stops': [
            {'city': 'Seymour',       'state': 'IN', 'dest_name': 'WALMART DC #6017G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Mccordsville',  'state': 'IN', 'dest_name': 'WALMART.COM SORT MCCORDSVILLE IND3', 'pallets': 1, 'weight': 0},
            {'city': 'Mount Pleasant','state': 'IA', 'dest_name': 'WALMART DC #6009G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Saint James',   'state': 'MO', 'dest_name': 'WALMART DC #6069G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Bentonville',   'state': 'AR', 'dest_name': 'WALMART DC #6094G-GENERAL',          'pallets': 1, 'weight': 0},
        ],
        'rate': None,
    },
    {
        'truck_number': 7,
        'stops': [
            {'city': 'Sutherland', 'state': 'VA', 'dest_name': 'WALMART DC #6023G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Hope Mills', 'state': 'NC', 'dest_name': 'WALMART DC #6040D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Shelby',     'state': 'NC', 'dest_name': 'WALMART DC #6070G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Lagrange',   'state': 'GA', 'dest_name': 'WALMART DC #6054D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Cullman',    'state': 'AL', 'dest_name': 'WALMART DC #6006G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': None,
    },
    {
        'truck_number': 8,
        'stops': [
            {'city': 'Woodland',    'state': 'PA', 'dest_name': 'WALMART DC #6027G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Greencastle', 'state': 'PA', 'dest_name': 'WALMART DC #3124',          'pallets': 1, 'weight': 0},
            {'city': 'Midway',      'state': 'TN', 'dest_name': 'WALMART DC #6039D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Hopkinsville','state': 'KY', 'dest_name': 'WALMART DC #6066G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': None,
    },
]

# ─── Week of 6/3/2026 + 6/6/2026 — Origin 3322 (Walnut, CA) ─────────────────
WEEK_636_3322 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Buckeye',        'state': 'AZ', 'dest_name': 'WALMART DC #6031G-GENERAL',      'pallets': 1, 'weight': 315.1},
            {'city': 'Litchfield Park','state': 'AZ', 'dest_name': 'WALMART.COM SORT GLENDALE PHX1', 'pallets': 1, 'weight': 333.6},
            {'city': 'Plainview',      'state': 'TX', 'dest_name': 'WALMART DC #6012G-GENERAL',      'pallets': 1, 'weight': 141.4},
            {'city': 'New Braunfels',  'state': 'TX', 'dest_name': 'WALMART DC #6016G-GENERAL',      'pallets': 1, 'weight': 112.3},
            {'city': 'Sealy',          'state': 'TX', 'dest_name': 'WALMART DC #7036G-GENERAL',      'pallets': 1, 'weight': 215.1},
        ],
        'rate': 2800,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Apple Valley', 'state': 'CA', 'dest_name': 'WALMART RDC 7033',          'pallets': 2, 'weight': 1870.5},
            {'city': 'Sparks',       'state': 'NV', 'dest_name': 'WALMART.COM SORT JET NV1',  'pallets': 1, 'weight': 304.0},
            {'city': 'Grantsville',  'state': 'UT', 'dest_name': 'WALMART DC #7026G-GENERAL', 'pallets': 1, 'weight': 125.9},
            {'city': 'Loveland',     'state': 'CO', 'dest_name': 'WALMART DC #6019G-GENERAL', 'pallets': 1, 'weight': 939.0},
        ],
        'rate': 2600,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Chino',           'state': 'CA', 'dest_name': 'WALMART.COM SORT CHINO LAX', 'pallets': 1, 'weight': 422.1},
            {'city': 'Porterville',     'state': 'CA', 'dest_name': 'WALMART DC #6021D-DSDC',     'pallets': 1, 'weight': 169.9},
            {'city': 'Red Bluff',       'state': 'CA', 'dest_name': 'WALMART DC #6026G-GENERAL',  'pallets': 1, 'weight': 169.5},
            {'city': 'South Hermiston', 'state': 'OR', 'dest_name': 'WALMART DC #6037D-DSDC',     'pallets': 1, 'weight': 764.8},
        ],
        'rate': 2600,
    },
]

# ─── Week of 6/3/2026 + 6/6/2026 — Origin 3943 (Brockport, NY) ──────────────
WEEK_636_3943 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL', 'pallets': 1, 'weight': 1135.9},
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL', 'pallets': 2, 'weight': 3451.4},
            {'city': 'Alachua',    'state': 'FL', 'dest_name': 'WALMART DC #7035',          'pallets': 1, 'weight': 928.3},
            {'city': 'Brooksville','state': 'FL', 'dest_name': 'WALMART DC #6020G-GENERAL', 'pallets': 1, 'weight': 507.1},
            {'city': 'Davenport',  'state': 'FL', 'dest_name': 'WALMART.COM SORT MCO1',     'pallets': 1, 'weight': 304.0},
            {'city': 'Fort Pierce','state': 'FL', 'dest_name': 'WALMART DC #7038G-GENERAL', 'pallets': 1, 'weight': 140.2},
        ],
        'rate': 3800,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Sutherland', 'state': 'VA', 'dest_name': 'WALMART DC #6023G-GENERAL',      'pallets': 2, 'weight': 3375.6},
            {'city': 'Hope Mills', 'state': 'NC', 'dest_name': 'WALMART DC #6040D-DSDC',         'pallets': 2, 'weight': 2006.9},
            {'city': 'Troutman',   'state': 'NC', 'dest_name': 'WALMART.COM SORT TROUTMAN CLT1', 'pallets': 1, 'weight': 658.1},
            {'city': 'Shelby',     'state': 'NC', 'dest_name': 'WALMART DC #6070G-GENERAL',      'pallets': 1, 'weight': 1335.8},
            {'city': 'Lagrange',   'state': 'GA', 'dest_name': 'WALMART DC #6054D-DSDC',         'pallets': 1, 'weight': 667.1},
        ],
        'rate': 2000,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Marcy',     'state': 'NY', 'dest_name': 'WALMART DC #6038D-DSDC',    'pallets': 1, 'weight': 97.1},
            {'city': 'Raymond',   'state': 'NH', 'dest_name': 'WALMART DC #6030D-DSDC',    'pallets': 1, 'weight': 97.4},
            {'city': 'Tobyhanna', 'state': 'PA', 'dest_name': 'WALMART DC #6080G-GENERAL', 'pallets': 1, 'weight': 1153.2},
            {'city': 'Tobyhanna', 'state': 'PA', 'dest_name': 'WALMART DC #6080G-GENERAL', 'pallets': 1, 'weight': 1173.5},
            {'city': 'Bethlehem', 'state': 'PA', 'dest_name': 'WALMART DC #7356',          'pallets': 1, 'weight': 423.1},
            {'city': 'Smyrna',    'state': 'DE', 'dest_name': 'WALMART DC #7034G-GENERAL', 'pallets': 1, 'weight': 854.7},
        ],
        'rate': 1300,
    },
    {
        'truck_number': 4,
        'stops': [
            {'city': 'Woodland',      'state': 'PA', 'dest_name': 'WALMART DC #6027G-GENERAL',    'pallets': 1, 'weight': 413.1},
            {'city': 'Mount Crawford','state': 'VA', 'dest_name': 'ARA@WALMART DC #7045-GENERAL', 'pallets': 1, 'weight': 1767.5},
            {'city': 'Midway',        'state': 'TN', 'dest_name': 'WALMART DC #6039D-DSDC',       'pallets': 1, 'weight': 329.6},
            {'city': 'Olive Branch',  'state': 'MS', 'dest_name': 'WALMART DC #4301',             'pallets': 1, 'weight': 128.1},
            {'city': 'Opelousas',     'state': 'LA', 'dest_name': 'WALMART DC #6048G-GENERAL',    'pallets': 1, 'weight': 493.4},
        ],
        'rate': 2400,
    },
    {
        'truck_number': 5,
        'stops': [
            {'city': 'Grove City', 'state': 'OH', 'dest_name': 'WALMART DC #6024D-DSDC',              'pallets': 1, 'weight': 155.5},
            {'city': 'Saint James','state': 'MO', 'dest_name': 'WALMART DC #6069G-GENERAL',           'pallets': 1, 'weight': 311.6},
            {'city': 'Sanger',     'state': 'TX', 'dest_name': 'WALMART DC #6068G-GENERAL',           'pallets': 1, 'weight': 213.8},
            {'city': 'Lancaster',  'state': 'TX', 'dest_name': 'WALMART.COM SORT LANCASTER DFW5 WFS', 'pallets': 1, 'weight': 289.3},
            {'city': 'Palestine',  'state': 'TX', 'dest_name': 'WALMART DC #6036D-DSDC',              'pallets': 1, 'weight': 155.6},
        ],
        'rate': 2300,
    },
    {
        'truck_number': 6,
        'stops': [
            {'city': 'Greencastle', 'state': 'PA', 'dest_name': 'WALMART DC #3124',          'pallets': 1, 'weight': 600.2},
            {'city': 'Hopkinsville','state': 'KY', 'dest_name': 'WALMART DC #6066G-GENERAL', 'pallets': 1, 'weight': 112.1},
            {'city': 'Cullman',     'state': 'AL', 'dest_name': 'WALMART DC #6006G-GENERAL', 'pallets': 1, 'weight': 140.7},
            {'city': 'Brookhaven',  'state': 'MS', 'dest_name': 'WALMART DC #6011G-GENERAL', 'pallets': 1, 'weight': 962.7},
        ],
        'rate': 2400,
    },
    {
        'truck_number': 7,
        'stops': [
            {'city': 'Coldwater',     'state': 'MI', 'dest_name': 'WALMART DC #6043D-DSDC',    'pallets': 1, 'weight': 402.5},
            {'city': 'Mount Pleasant','state': 'IA', 'dest_name': 'WALMART DC #6009G-GENERAL', 'pallets': 1, 'weight': 155.9},
            {'city': 'Ottawa',        'state': 'KS', 'dest_name': 'WALMART DC #6035G-GENERAL', 'pallets': 1, 'weight': 213.2},
            {'city': 'Bentonville',   'state': 'AR', 'dest_name': 'WALMART DC #6094G-GENERAL', 'pallets': 1, 'weight': 199.8},
            {'city': 'Searcy',        'state': 'AR', 'dest_name': 'WALMART DC #6018G-GENERAL', 'pallets': 1, 'weight': 1531.7},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 8,
        'stops': [
            {'city': 'Seymour',      'state': 'IN', 'dest_name': 'WALMART DC #6017G-GENERAL',          'pallets': 1, 'weight': 537.1},
            {'city': 'Mccordsville', 'state': 'IN', 'dest_name': 'WALMART.COM SORT MCCORDSVILLE IND3', 'pallets': 1, 'weight': 540.1},
            {'city': 'Spring Valley','state': 'IL', 'dest_name': 'WALMART DC #6092D-DSDC',             'pallets': 1, 'weight': 521.9},
            {'city': 'Joliet',       'state': 'IL', 'dest_name': 'WALMART.COM SORT JOLIET ORD1',       'pallets': 1, 'weight': 481.1},
            {'city': 'Beaver Dam',   'state': 'WI', 'dest_name': 'WALMART DC #7039-REGULAR',           'pallets': 1, 'weight': 1265.7},
        ],
        'rate': 2100,
    },
]

# ─── Week of 6/24/2026 + 6/27/2026 — Origin 3322 (Walnut, CA) ───────────────
WEEK_624_3322 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Porterville',     'state': 'CA', 'dest_name': 'WALMART DC #6021D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Red Bluff',       'state': 'CA', 'dest_name': 'WALMART DC #6026G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'South Hermiston', 'state': 'OR', 'dest_name': 'WALMART DC #6037D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'South Hermiston', 'state': 'OR', 'dest_name': 'WALMART DC #6037D-DSDC',    'pallets': 1, 'weight': 0},
        ],
        'rate': 2400,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Apple Valley', 'state': 'CA', 'dest_name': 'WALMART RDC 7033',          'pallets': 1, 'weight': 0},
            {'city': 'Apple Valley', 'state': 'CA', 'dest_name': 'WALMART RDC 7033',          'pallets': 1, 'weight': 0},
            {'city': 'Grantsville',  'state': 'UT', 'dest_name': 'WALMART DC #7026G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Loveland',     'state': 'CO', 'dest_name': 'WALMART DC #6019G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Loveland',     'state': 'CO', 'dest_name': 'WALMART DC #6019G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2400,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Buckeye',        'state': 'AZ', 'dest_name': 'WALMART DC #6031G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Litchfield Park','state': 'AZ', 'dest_name': 'WALMART.COM SORT GLENDALE PHX1', 'pallets': 1, 'weight': 0},
            {'city': 'Plainview',      'state': 'TX', 'dest_name': 'WALMART DC #6012G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'New Braunfels',  'state': 'TX', 'dest_name': 'WALMART DC #6016G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Sealy',          'state': 'TX', 'dest_name': 'WALMART DC #7036G-GENERAL',      'pallets': 1, 'weight': 0},
        ],
        'rate': 2400,
    },
]

# ─── Week of 6/24/2026 + 6/27/2026 — Origin 3943 (Brockport, NY) ─────────────
WEEK_624_3943 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Grove City',  'state': 'OH', 'dest_name': 'WALMART DC #6024D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Seymour',     'state': 'IN', 'dest_name': 'WALMART DC #6017G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Saint James', 'state': 'MO', 'dest_name': 'WALMART DC #6069G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Saint James', 'state': 'MO', 'dest_name': 'WALMART DC #6069G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Ottawa',      'state': 'KS', 'dest_name': 'WALMART DC #6035G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Bentonville', 'state': 'AR', 'dest_name': 'WALMART DC #6094G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Coldwater',    'state': 'MI', 'dest_name': 'WALMART DC #6043D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Coldwater',    'state': 'MI', 'dest_name': 'WALMART DC #6043D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Spring Valley','state': 'IL', 'dest_name': 'WALMART DC #6092D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Beaver Dam',   'state': 'WI', 'dest_name': 'WALMART DC #7039-REGULAR',  'pallets': 1, 'weight': 0},
            {'city': 'Beaver Dam',   'state': 'WI', 'dest_name': 'WALMART DC #7039-REGULAR',  'pallets': 1, 'weight': 0},
            {'city': 'Menomonie',    'state': 'WI', 'dest_name': 'WALMART DC #6025G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Menomonie',    'state': 'WI', 'dest_name': 'WALMART DC #6025G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2100,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Marcy',          'state': 'NY', 'dest_name': 'WALMART DC #6038D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Raymond',        'state': 'NH', 'dest_name': 'WALMART DC #6030D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Tobyhanna',      'state': 'PA', 'dest_name': 'WALMART DC #6080G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Smyrna',         'state': 'DE', 'dest_name': 'WALMART DC #7034G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Mount Crawford', 'state': 'VA', 'dest_name': 'ARA@WALMART DC #7045-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Mount Crawford', 'state': 'VA', 'dest_name': 'ARA@WALMART DC #7045-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Sutherland',     'state': 'VA', 'dest_name': 'WALMART DC #6023G-GENERAL',    'pallets': 1, 'weight': 0},
        ],
        'rate': 1700,
    },
    {
        'truck_number': 4,
        'stops': [
            {'city': 'Hopkinsville', 'state': 'KY', 'dest_name': 'WALMART DC #6066G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Searcy',       'state': 'AR', 'dest_name': 'WALMART DC #6018G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Searcy',       'state': 'AR', 'dest_name': 'WALMART DC #6018G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Sanger',       'state': 'TX', 'dest_name': 'WALMART DC #6068G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Palestine',    'state': 'TX', 'dest_name': 'WALMART DC #6036D-DSDC',    'pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 5,
        'stops': [
            {'city': 'Hope Mills',  'state': 'NC', 'dest_name': 'WALMART DC #6040D-DSDC',        'pallets': 1, 'weight': 0},
            {'city': 'Hope Mills',  'state': 'NC', 'dest_name': 'WALMART DC #6040D-DSDC',        'pallets': 1, 'weight': 0},
            {'city': 'Troutman',    'state': 'NC', 'dest_name': 'WALMART.COM SORT TROUTMAN CLT1','pallets': 1, 'weight': 0},
            {'city': 'Shelby',      'state': 'NC', 'dest_name': 'WALMART DC #6070G-GENERAL',     'pallets': 1, 'weight': 0},
            {'city': 'Midway',      'state': 'TN', 'dest_name': 'WALMART DC #6039D-DSDC',        'pallets': 1, 'weight': 0},
            {'city': 'Midway',      'state': 'TN', 'dest_name': 'WALMART DC #6039D-DSDC',        'pallets': 1, 'weight': 0},
            {'city': 'Olive Branch','state': 'MS', 'dest_name': 'WALMART DC #4301',              'pallets': 1, 'weight': 0},
        ],
        'rate': 2100,
    },
    {
        'truck_number': 6,
        'stops': [
            {'city': 'Woodland',   'state': 'PA', 'dest_name': 'WALMART DC #6027G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Lagrange',   'state': 'GA', 'dest_name': 'WALMART DC #6054D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Lagrange',   'state': 'GA', 'dest_name': 'WALMART DC #6054D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Cullman',    'state': 'AL', 'dest_name': 'WALMART DC #6006G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Brookhaven', 'state': 'MS', 'dest_name': 'WALMART DC #6011G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Brookhaven', 'state': 'MS', 'dest_name': 'WALMART DC #6011G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Opelousas',  'state': 'LA', 'dest_name': 'WALMART DC #6048G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Opelousas',  'state': 'LA', 'dest_name': 'WALMART DC #6048G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 7,
        'stops': [
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Alachua',    'state': 'FL', 'dest_name': 'WALMART DC #7035',          'pallets': 1, 'weight': 0},
            {'city': 'Alachua',    'state': 'FL', 'dest_name': 'WALMART DC #7035',          'pallets': 1, 'weight': 0},
            {'city': 'Brooksville','state': 'FL', 'dest_name': 'WALMART DC #6020G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Brooksville','state': 'FL', 'dest_name': 'WALMART DC #6020G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Davenport',  'state': 'FL', 'dest_name': 'WALMART.COM SORT MCO1',     'pallets': 1, 'weight': 0},
            {'city': 'Fort Pierce','state': 'FL', 'dest_name': 'WALMART DC #7038G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 3800,
    },
]

# ─── Week of 7/1/2026 + 7/4/2026 — Origin 3322 (Walnut, CA) ─────────────────
WEEK_71_3322 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Buckeye',        'state': 'AZ', 'dest_name': 'WALMART DC #6031G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Litchfield Park','state': 'AZ', 'dest_name': 'WALMART.COM SORT GLENDALE PHX1', 'pallets': 1, 'weight': 0},
            {'city': 'Loveland',       'state': 'CO', 'dest_name': 'WALMART DC #6019G-GENERAL',      'pallets': 1, 'weight': 0},
        ],
        'rate': 2400,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Chino',           'state': 'CA', 'dest_name': 'WALMART.COM SORT CHINO LAX', 'pallets': 1, 'weight': 0},
            {'city': 'Apple Valley',    'state': 'CA', 'dest_name': 'WALMART RDC 7033',           'pallets': 1, 'weight': 0},
            {'city': 'Sparks',          'state': 'NV', 'dest_name': 'WALMART.COM SORT JET NV1',   'pallets': 1, 'weight': 0},
            {'city': 'South Hermiston', 'state': 'OR', 'dest_name': 'WALMART DC #6037D-DSDC',     'pallets': 1, 'weight': 0},
        ],
        'rate': 2400,
    },
]

# ─── Week of 7/1/2026 + 7/4/2026 — Origin 3943 (Brockport, NY) ──────────────
WEEK_71_3943 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Alachua',    'state': 'FL', 'dest_name': 'WALMART DC #7035',          'pallets': 1, 'weight': 0},
            {'city': 'Alachua',    'state': 'FL', 'dest_name': 'WALMART DC #7035',          'pallets': 1, 'weight': 0},
            {'city': 'Brooksville','state': 'FL', 'dest_name': 'WALMART DC #6020G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Brooksville','state': 'FL', 'dest_name': 'WALMART DC #6020G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Davenport',  'state': 'FL', 'dest_name': 'WALMART.COM SORT MCO1',     'pallets': 1, 'weight': 0},
        ],
        'rate': 3800,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Woodland',   'state': 'PA', 'dest_name': 'WALMART DC #6027G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Greencastle','state': 'PA', 'dest_name': 'WALMART DC #3124',          'pallets': 1, 'weight': 0},
            {'city': 'Brookhaven', 'state': 'MS', 'dest_name': 'WALMART DC #6011G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Brookhaven', 'state': 'MS', 'dest_name': 'WALMART DC #6011G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Opelousas',  'state': 'LA', 'dest_name': 'WALMART DC #6048G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Bethlehem', 'state': 'PA', 'dest_name': 'WALMART DC #7356',                'pallets': 1, 'weight': 0},
            {'city': 'Hope Mills','state': 'NC', 'dest_name': 'WALMART DC #6040D-DSDC',          'pallets': 1, 'weight': 0},
            {'city': 'Troutman',  'state': 'NC', 'dest_name': 'WALMART.COM SORT TROUTMAN CLT1', 'pallets': 1, 'weight': 0},
            {'city': 'Shelby',    'state': 'NC', 'dest_name': 'WALMART DC #6070G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Midway',    'state': 'TN', 'dest_name': 'WALMART DC #6039D-DSDC',         'pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 4,
        'stops': [
            {'city': 'Tobyhanna',      'state': 'PA', 'dest_name': 'WALMART DC #6080G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Tobyhanna',      'state': 'PA', 'dest_name': 'WALMART DC #6080G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Smyrna',         'state': 'DE', 'dest_name': 'WALMART DC #7034G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Mount Crawford', 'state': 'VA', 'dest_name': 'ARA@WALMART DC #7045-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Sutherland',     'state': 'VA', 'dest_name': 'WALMART DC #6023G-GENERAL',    'pallets': 1, 'weight': 0},
        ],
        'rate': 1700,
    },
    {
        'truck_number': 5,
        'stops': [
            {'city': 'Coldwater',    'state': 'MI', 'dest_name': 'WALMART DC #6043D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Coldwater',    'state': 'MI', 'dest_name': 'WALMART DC #6043D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Joliet',       'state': 'IL', 'dest_name': 'WALMART.COM SORT JOLIET ORD1', 'pallets': 1, 'weight': 0},
            {'city': 'Spring Valley','state': 'IL', 'dest_name': 'WALMART DC #6092D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Spring Valley','state': 'IL', 'dest_name': 'WALMART DC #6092D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Beaver Dam',   'state': 'WI', 'dest_name': 'WALMART DC #7039-REGULAR',     'pallets': 1, 'weight': 0},
            {'city': 'Menomonie',    'state': 'WI', 'dest_name': 'WALMART DC #6025G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Menomonie',    'state': 'WI', 'dest_name': 'WALMART DC #6025G-GENERAL',    'pallets': 1, 'weight': 0},
        ],
        'rate': 2100,
    },
    {
        'truck_number': 6,
        'stops': [
            {'city': 'Mccordsville', 'state': 'IN', 'dest_name': 'WALMART.COM SORT MCCORDSVILLE IND3', 'pallets': 1, 'weight': 0},
            {'city': 'Seymour',      'state': 'IN', 'dest_name': 'WALMART DC #6017G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Saint James',  'state': 'MO', 'dest_name': 'WALMART DC #6069G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Searcy',       'state': 'AR', 'dest_name': 'WALMART DC #6018G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Lancaster',    'state': 'TX', 'dest_name': 'WALMART.COM SORT LANCASTER DFW5 WFS','pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
]

# ─── Week of 7/8/2026 + 7/11/2026 — Origin 3322 (Walnut, CA) ────────────────
WEEK_78_3322 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Apple Valley',    'state': 'CA', 'dest_name': 'WALMART RDC 7033',         'pallets': 1, 'weight': 0},
            {'city': 'Sparks',          'state': 'NV', 'dest_name': 'WALMART.COM SORT JET NV1', 'pallets': 1, 'weight': 0},
            {'city': 'South Hermiston', 'state': 'OR', 'dest_name': 'WALMART DC #6037D-DSDC',   'pallets': 1, 'weight': 0},
        ],
        'rate': 2700,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Chino',          'state': 'CA', 'dest_name': 'WALMART.COM SORT CHINO LAX',     'pallets': 1, 'weight': 0},
            {'city': 'Litchfield Park','state': 'AZ', 'dest_name': 'WALMART.COM SORT GLENDALE PHX1', 'pallets': 1, 'weight': 0},
            {'city': 'Loveland',       'state': 'CO', 'dest_name': 'WALMART DC #6019G-GENERAL',      'pallets': 1, 'weight': 0},
        ],
        'rate': 2700,
    },
]

# ─── Week of 7/8/2026 + 7/11/2026 — Origin 3943 (Brockport, NY) ─────────────
WEEK_78_3943 = [
    {
        'truck_number': 1,
        'stops': [
            {'city': 'Mccordsville', 'state': 'IN', 'dest_name': 'WALMART.COM SORT MCCORDSVILLE IND3', 'pallets': 1, 'weight': 0},
            {'city': 'Seymour',      'state': 'IN', 'dest_name': 'WALMART DC #6017G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Saint James',  'state': 'MO', 'dest_name': 'WALMART DC #6069G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Olive Branch', 'state': 'MS', 'dest_name': 'WALMART DC #4301',                   'pallets': 1, 'weight': 0},
            {'city': 'Searcy',       'state': 'AR', 'dest_name': 'WALMART DC #6018G-GENERAL',          'pallets': 1, 'weight': 0},
            {'city': 'Lancaster',    'state': 'TX', 'dest_name': 'WALMART.COM SORT LANCASTER DFW5 WFS','pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 2,
        'stops': [
            {'city': 'Coldwater',    'state': 'MI', 'dest_name': 'WALMART DC #6043D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Joliet',       'state': 'IL', 'dest_name': 'WALMART.COM SORT JOLIET ORD1', 'pallets': 1, 'weight': 0},
            {'city': 'Spring Valley','state': 'IL', 'dest_name': 'WALMART DC #6092D-DSDC',       'pallets': 1, 'weight': 0},
            {'city': 'Beaver Dam',   'state': 'WI', 'dest_name': 'WALMART DC #7039-REGULAR',     'pallets': 1, 'weight': 0},
            {'city': 'Menomonie',    'state': 'WI', 'dest_name': 'WALMART DC #6025G-GENERAL',    'pallets': 1, 'weight': 0},
        ],
        'rate': 2100,
    },
    {
        'truck_number': 3,
        'stops': [
            {'city': 'Tobyhanna',      'state': 'PA', 'dest_name': 'WALMART DC #6080G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Bethlehem',      'state': 'PA', 'dest_name': 'WALMART DC #7356',             'pallets': 1, 'weight': 0},
            {'city': 'Smyrna',         'state': 'DE', 'dest_name': 'WALMART DC #7034G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Mount Crawford', 'state': 'VA', 'dest_name': 'ARA@WALMART DC #7045-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Sutherland',     'state': 'VA', 'dest_name': 'WALMART DC #6023G-GENERAL',    'pallets': 1, 'weight': 0},
            {'city': 'Hope Mills',     'state': 'NC', 'dest_name': 'WALMART DC #6040D-DSDC',       'pallets': 1, 'weight': 0},
        ],
        'rate': 1800,
    },
    {
        'truck_number': 4,
        'stops': [
            {'city': 'Woodland',   'state': 'PA', 'dest_name': 'WALMART DC #6027G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Greencastle','state': 'PA', 'dest_name': 'WALMART DC #3124',          'pallets': 1, 'weight': 0},
            {'city': 'Lagrange',   'state': 'GA', 'dest_name': 'WALMART DC #6054D-DSDC',    'pallets': 1, 'weight': 0},
            {'city': 'Brookhaven', 'state': 'MS', 'dest_name': 'WALMART DC #6011G-GENERAL', 'pallets': 1, 'weight': 0},
            {'city': 'Opelousas',  'state': 'LA', 'dest_name': 'WALMART DC #6048G-GENERAL', 'pallets': 1, 'weight': 0},
        ],
        'rate': 2200,
    },
    {
        'truck_number': 5,
        'stops': [
            {'city': 'Troutman',   'state': 'NC', 'dest_name': 'WALMART.COM SORT TROUTMAN CLT1', 'pallets': 1, 'weight': 0},
            {'city': 'Shelby',     'state': 'NC', 'dest_name': 'WALMART DC #6070G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Douglas',    'state': 'GA', 'dest_name': 'WALMART DC #6010G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Brooksville','state': 'FL', 'dest_name': 'WALMART DC #6020G-GENERAL',      'pallets': 1, 'weight': 0},
            {'city': 'Davenport',  'state': 'FL', 'dest_name': 'WALMART.COM SORT MCO1',          'pallets': 1, 'weight': 0},
        ],
        'rate': 3800,
    },
]


def seed():
    print("Seeding route history database...\n")
    datasets = [
        ('5/30/2026',            '3322', WEEK_530_3322),
        ('5/30/2026',            '3943', WEEK_530_3943),
        ('6/3/2026-6/6/2026',   '3322', WEEK_636_3322),
        ('6/3/2026-6/6/2026',   '3943', WEEK_636_3943),
        ('6/24/2026-6/27/2026', '3322', WEEK_624_3322),
        ('6/24/2026-6/27/2026', '3943', WEEK_624_3943),
        ('7/1/2026-7/4/2026',   '3322', WEEK_71_3322),
        ('7/1/2026-7/4/2026',   '3943', WEEK_71_3943),
        ('7/8/2026-7/11/2026',  '3322', WEEK_78_3322),
        ('7/8/2026-7/11/2026',  '3943', WEEK_78_3943),
    ]
    seeded = 0
    for rdd, origin, trucks in datasets:
        if not route_exists_for_week(rdd, origin):
            save_routes(rdd, origin, trucks)
            print(f"  ✓ Seeded {len(trucks)} trucks  —  Origin {origin}  |  RDD {rdd}")
            seeded += 1
        else:
            print(f"  ⚠ Already exists, skipped  —  Origin {origin}  |  RDD {rdd}")

    print(f"\nDone. {seeded} origin-week(s) newly seeded.")


if __name__ == '__main__':
    seed()
