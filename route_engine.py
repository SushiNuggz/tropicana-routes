import pandas as pd
from utils import extract_city, geo_distance, STATE_COORDS
from db import get_all_routes_for_origin

MAX_PALLETS = 21
MAX_WEIGHT  = 44000
TARGET_STOPS = 5
MAX_STOPS    = 6


# ── File parsing ───────────────────────────────────────────────────────────────

def parse_raw_file(df):
    """Parse a raw Tropicana DataFrame into a list of order dicts.

    Handles files with or without Pallets / Weight columns and with or
    without a Destination Location ID column.
    """
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    col_lower = {c.lower(): c for c in df.columns}

    def find_col(*keywords):
        for k, v in col_lower.items():
            if all(kw in k for kw in keywords):
                return v
        return None

    origin_col    = find_col('origin', 'location')
    dest_name_col = find_col('destination', 'name')
    dest_addr_col = find_col('destination', 'address')
    dest_state_col = find_col('destination', 'state') or find_col('destination', 'province')
    dest_id_col   = find_col('destination', 'location', 'id')
    pallets_col   = col_lower.get('pallets')
    weight_col    = col_lower.get('weight')

    orders = []
    for _, row in df.iterrows():
        if origin_col is None or pd.isna(row.get(origin_col)):
            continue
        origin = str(row[origin_col]).strip()
        if origin not in ('3322', '3943'):
            continue

        state     = str(row[dest_state_col]).strip() if dest_state_col else ''
        address   = str(row[dest_addr_col]).strip()  if dest_addr_col  else ''
        dest_name = str(row[dest_name_col]).strip()  if dest_name_col  else ''
        dest_id   = str(row[dest_id_col]).strip()    if dest_id_col    else ''
        city      = extract_city(address, state)

        pallets = (
            float(row[pallets_col])
            if pallets_col and not pd.isna(row.get(pallets_col, None))
            else 1.0
        )
        weight = (
            float(row[weight_col])
            if weight_col and not pd.isna(row.get(weight_col, None))
            else 0.0
        )

        orders.append({
            'origin':    origin,
            'dest_id':   dest_id,
            'dest_name': dest_name,
            'address':   address,
            'state':     state,
            'city':      city,
            'pallets':   pallets,
            'weight':    weight,
        })

    return orders


# ── Route suggestion entry point ───────────────────────────────────────────────

def suggest_routes(orders, rdd=None):
    """Suggest truck routes from a list of orders.

    Returns {'3322': [truck, ...], '3943': [truck, ...]}
    Each truck dict has: truck_number, stops, historical_rate,
                         historical_rdd, from_history
    """
    result = {}
    for origin in ['3322', '3943']:
        origin_orders = [o for o in orders if o['origin'] == origin]
        if not origin_orders:
            result[origin] = []
            continue
        trucks = _match_and_cluster(origin, origin_orders)
        result[origin] = trucks
    return result


# ── Internal routing logic ─────────────────────────────────────────────────────

def _match_and_cluster(origin, orders):
    """Try to match orders to historical routes; cluster the remainder."""
    remaining = list(orders)
    trucks    = []
    historical = get_all_routes_for_origin(origin)
    used_hist_sets = []

    if historical:
        for hist in historical:
            if not remaining:
                break

            hist_key_list = hist['stop_keys']  # sorted list, may have duplicates
            hist_key_set  = set(hist_key_list)

            # Skip if we already consumed a route with this exact stop set
            if hist_key_list in used_hist_sets:
                continue

            current_keys = {
                f"{o['city'].upper()}|{o['state'].upper()}" for o in remaining
            }
            matching_keys = hist_key_set & current_keys

            # Require at least 3 matching stops (or full match if route has <3)
            min_match = min(3, len(hist_key_set))
            if len(matching_keys) < min_match:
                continue

            matched_orders = [
                o for o in remaining
                if f"{o['city'].upper()}|{o['state'].upper()}" in hist_key_set
            ]
            if not matched_orders:
                continue

            total_p = sum(o['pallets'] for o in matched_orders)
            total_w = sum(o['weight']  for o in matched_orders)

            if total_p <= MAX_PALLETS and total_w <= MAX_WEIGHT:
                trucks.append({
                    'stops':          matched_orders,
                    'historical_rate': hist['rate'],
                    'historical_rdd':  hist['week_rdd'],
                    'from_history':    True,
                })
                for o in matched_orders:
                    remaining.remove(o)
                used_hist_sets.append(hist_key_list)

    # Cluster whatever is left geographically
    geo_trucks = _geo_cluster(remaining)
    trucks.extend(geo_trucks)

    # Assign final truck numbers
    for i, truck in enumerate(trucks):
        truck['truck_number'] = i + 1

    return trucks


def _geo_cluster(orders):
    """Greedy nearest-neighbor clustering by state centroid."""
    if not orders:
        return []

    # Start from westernmost stop and work east
    remaining = sorted(
        orders,
        key=lambda o: STATE_COORDS.get(o['state'].upper(), (39.5, -98.4))[1],
    )
    trucks = []

    while remaining:
        stops   = []
        pallets = 0.0
        weight  = 0.0

        seed = remaining.pop(0)
        stops.append(seed)
        pallets += seed['pallets']
        weight  += seed['weight']

        while remaining and len(stops) < MAX_STOPS:
            last = stops[-1]
            best      = None
            best_dist = float('inf')

            for o in remaining:
                if pallets + o['pallets'] > MAX_PALLETS:
                    continue
                if weight  + o['weight']  > MAX_WEIGHT:
                    continue
                d = geo_distance(last['state'], o['state'])
                if d < best_dist:
                    best_dist = d
                    best      = o

            # Stop adding if nothing fits or we've hit target and next is far
            if best is None:
                break
            if len(stops) >= TARGET_STOPS and best_dist > 10:
                break

            stops.append(best)
            pallets += best['pallets']
            weight  += best['weight']
            remaining.remove(best)

        trucks.append({
            'stops':          stops,
            'historical_rate': None,
            'historical_rdd':  None,
            'from_history':    False,
        })

    return trucks


# ── Export helpers ─────────────────────────────────────────────────────────────

def build_route_string(truck_number, stops, rate=None):
    """Build the Tropicana-format route string.

    Example: 'Truck 1:  Buckeye AZ, Litchfield Park AZ, Plainview TX:  $3,000'
    Duplicate cities are shown as 'City ST x 2'.
    """
    city_state_list = [(s['city'], s['state']) for s in stops]

    # Count occurrences of each (city, state) pair
    counts = {}
    for cs in city_state_list:
        counts[cs] = counts.get(cs, 0) + 1

    seen  = set()
    parts = []
    for cs in city_state_list:
        if cs not in seen:
            label = f"{cs[0]} {cs[1]}"
            if counts[cs] > 1:
                label += f" x {counts[cs]}"
            parts.append(label)
            seen.add(cs)

    route = f"Truck {truck_number}:  {', '.join(parts)}"

    if rate:
        try:
            rate_val = float(str(rate).replace('$', '').replace(',', ''))
            route += f":  ${rate_val:,.0f}"
        except (ValueError, TypeError):
            route += f":  {rate}"

    return route
