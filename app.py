import streamlit as st
import pandas as pd
from db import init_db, save_routes, route_exists_for_week, delete_all_routes
from route_engine import (
    parse_raw_file, suggest_routes, build_route_string,
    MAX_PALLETS, MAX_WEIGHT,
)

# ── Password gate ──────────────────────────────────────────────────────────────
def _check_password():
    if st.session_state.get("authenticated"):
        return
    st.set_page_config(page_title="Tropicana Route Builder", page_icon="🍊")
    st.title("🍊 Tropicana Route Builder")
    st.caption("Enter your team password to continue.")
    pwd = st.text_input("Password", type="password", key="_pw")
    if st.button("Sign In", type="primary"):
        try:
            expected = st.secrets["APP_PASSWORD"]
        except Exception:
            expected = "tropicana2025"
        if pwd == expected:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password — ask your team admin.")
    st.stop()

_check_password()

# ── App bootstrap ──────────────────────────────────────────────────────────────
init_db()
st.set_page_config(
    page_title="Tropicana Route Builder",
    page_icon="🍊",
    layout="wide",
)
st.title("🍊 Tropicana Walmart Route Builder")

# ── Sidebar: seed history (one-time admin action) ─────────────────────────────
with st.sidebar:
    st.subheader("⚙️ Admin")
    if st.button("🌱 Seed historical routes"):
        try:
            from seed_history import (
                WEEK_530_3322, WEEK_530_3943,
                WEEK_636_3322, WEEK_636_3943,
                WEEK_624_3322, WEEK_624_3943,
                WEEK_71_3322,  WEEK_71_3943,
                WEEK_78_3322,  WEEK_78_3943,
            )
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
            seeded = skipped = 0
            for rdd, origin, trucks in datasets:
                if route_exists_for_week(rdd, origin):
                    skipped += 1
                else:
                    save_routes(rdd, origin, trucks)
                    seeded += 1
            if seeded:
                st.success(f"✅ Seeded {seeded} week(s) into history.")
            if skipped:
                st.info(f"⏭️ Skipped {skipped} week(s) already in history.")
        except Exception as e:
            st.error(f"Seed failed: {e}")
    st.caption("Click once to load all historical weeks. Safe to click again — duplicates are skipped.")

    if st.button("🔄 Force Re-seed (clears & re-loads all history)"):
        try:
            from seed_history import (
                WEEK_530_3322, WEEK_530_3943,
                WEEK_636_3322, WEEK_636_3943,
                WEEK_624_3322, WEEK_624_3943,
                WEEK_71_3322,  WEEK_71_3943,
                WEEK_78_3322,  WEEK_78_3943,
            )
            delete_all_routes()
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
            for rdd, origin, trucks in datasets:
                save_routes(rdd, origin, trucks)
            st.success("✅ All history cleared and re-seeded with latest data.")
        except Exception as e:
            st.error(f"Force re-seed failed: {e}")

    st.divider()
    st.subheader("📚 Route History")
    if st.button("Show stored history"):
        from db import get_all_routes_for_origin
        for orig in ['3322', '3943']:
            rows = get_all_routes_for_origin(orig)
            if rows:
                st.markdown(f"**Origin {orig}** — {len(rows)} truck(s)")
                for r in rows:
                    keys = ', '.join(r['stop_keys'])
                    st.caption(f"Week {r['week_rdd']} | Rate: {'$'+str(int(r['rate'])) if r['rate'] else 'none'} | {keys}")
            else:
                st.caption(f"Origin {orig}: no history yet")

ORIGIN_LABELS = {
    '3322': '🏭 Origin 3322 — Walnut, CA',
    '3943': '🏭 Origin 3943 — Brockport, NY',
}
ORIGIN_KEYS = {'3322': 'trucks_3322', '3943': 'trucks_3943'}


# ── Session state ──────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        'step':          'upload',
        'trucks_3322':   [],
        'trucks_3943':   [],
        'raw_df':        None,
        'orders':        [],
        'rdd':           '',
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ── Truck editing helpers ──────────────────────────────────────────────────────
def move_up(key, ti, si):
    stops = st.session_state[key][ti]['stops']
    if si > 0:
        stops[si - 1], stops[si] = stops[si], stops[si - 1]


def move_down(key, ti, si):
    stops = st.session_state[key][ti]['stops']
    if si < len(stops) - 1:
        stops[si], stops[si + 1] = stops[si + 1], stops[si]


def move_to_truck(key, from_ti, si, to_num):
    trucks = st.session_state[key]
    stop   = trucks[from_ti]['stops'].pop(si)
    to_ti  = next(i for i, t in enumerate(trucks) if t['truck_number'] == to_num)
    trucks[to_ti]['stops'].append(stop)
    # Drop empty trucks and renumber
    st.session_state[key] = [t for t in trucks if t['stops']]
    for i, t in enumerate(st.session_state[key]):
        t['truck_number'] = i + 1


def add_empty_truck(key):
    trucks = st.session_state[key]
    trucks.append({
        'truck_number':   len(trucks) + 1,
        'stops':          [],
        'historical_rate': None,
        'historical_rdd':  None,
        'from_history':    False,
    })


# ── Truck editor UI ────────────────────────────────────────────────────────────
def render_origin_editor(origin):
    key    = ORIGIN_KEYS[origin]
    trucks = st.session_state[key]

    if not trucks:
        st.info(f"No orders found for origin {origin}.")
        return

    for ti, truck in enumerate(trucks):
        total_p = sum(s.get('pallets', 1) for s in truck['stops'])
        total_w = sum(s.get('weight',  0) for s in truck['stops'])
        over_p  = total_p > MAX_PALLETS
        over_w  = total_w > MAX_WEIGHT
        status  = "🔴" if (over_p or over_w) else "✅"

        hist_hint = ""
        if truck.get('historical_rate'):
            hist_hint = (
                f"  |  📋 {truck.get('historical_rdd', 'prev week')}"
                f" — ${truck['historical_rate']:,.0f}"
            )

        label = (
            f"{status} Truck {truck['truck_number']}"
            f"  —  {len(truck['stops'])} stops"
            f"  |  {total_p:.0f} pallets"
            f"  |  {total_w:,.0f} lbs"
            f"{hist_hint}"
        )

        with st.expander(label, expanded=True):
            if not truck['stops']:
                st.caption("_Empty truck — move stops here from another truck_")
            else:
                st.markdown("**Stop order — top stop is loaded first at shipper:**")
                other_nums = [
                    t['truck_number'] for t in trucks
                    if t['truck_number'] != truck['truck_number']
                ]

                for si, stop in enumerate(truck['stops']):
                    c1, c2, c3, c4 = st.columns([5, 1, 1, 3])
                    c1.write(
                        f"**{si + 1}.** {stop['city']}, {stop['state']}"
                        f"  —  _{stop.get('dest_name', '')[:50]}_"
                    )
                    if c2.button("↑", key=f"up_{key}_{ti}_{si}",
                                 disabled=(si == 0)):
                        move_up(key, ti, si)
                        st.rerun()
                    if c3.button("↓", key=f"dn_{key}_{ti}_{si}",
                                 disabled=(si == len(truck['stops']) - 1)):
                        move_down(key, ti, si)
                        st.rerun()

                    if other_nums:
                        options = ["Move to…"] + other_nums
                        sel_key = f"sel_{key}_{ti}_{si}"

                        def make_handler(_key, _ti, _si, _sel_key):
                            def handler():
                                to_num = st.session_state.get(_sel_key, "Move to…")
                                if to_num != "Move to…":
                                    for sk in [k for k in list(st.session_state.keys())
                                               if k.startswith("sel_")]:
                                        del st.session_state[sk]
                                    move_to_truck(_key, _ti, _si, to_num)
                            return handler

                        c4.selectbox(
                            "Move to",
                            options,
                            key=sel_key,
                            label_visibility="collapsed",
                            format_func=lambda n: n if n == "Move to…" else f"→ Truck {n}",
                            on_change=make_handler(key, ti, si, sel_key),
                        )

            st.divider()

            if over_p:
                st.error(f"⚠️ Over pallet limit: {total_p:.0f} / {MAX_PALLETS}")
            if over_w:
                st.error(f"⚠️ Over weight limit: {total_w:,.0f} / {MAX_WEIGHT:,} lbs")

            c_rate, c_hint = st.columns([2, 4])
            rate_key = f"rate_{key}_{truck['truck_number']}"
            c_rate.text_input(
                "Rate ($)",
                key=rate_key,
                placeholder="Enter rate",
            )
            if truck.get('historical_rate') and truck.get('historical_rdd'):
                c_hint.caption(
                    f"💡 Last rate: **${truck['historical_rate']:,.0f}**"
                    f" (week of {truck['historical_rdd']})"
                )
            elif truck.get('from_history'):
                c_hint.caption("✓ Route matched from history — no rate on file")
            else:
                c_hint.caption("📍 New route (no prior history)")

    st.divider()
    if st.button(f"➕ Add empty truck for {origin}", key=f"add_{key}"):
        add_empty_truck(key)
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Upload
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 'upload':
    st.subheader("Step 1 — Upload Tropicana Order File")

    col1, col2 = st.columns([3, 2])
    with col1:
        uploaded = st.file_uploader(
            "Upload the Excel (.xlsx) or CSV file from Tropicana",
            type=['xlsx', 'xls', 'csv'],
        )
    with col2:
        rdd_input = st.text_input(
            "RDD (from the email)",
            placeholder="e.g.  6/3/2026   or   6/3/2026, 6/6/2026",
        )

    if uploaded and rdd_input:
        if st.button("🔄 Generate Routes", type="primary"):
            with st.spinner("Parsing file and generating routes…"):
                try:
                    if uploaded.name.lower().endswith('.csv'):
                        df = pd.read_csv(uploaded)
                    else:
                        df = pd.read_excel(uploaded)

                    df     = df.dropna(how='all')
                    orders = parse_raw_file(df)

                    if not orders:
                        st.error(
                            "No valid orders found. "
                            "Ensure Origin Location ID column contains 3322 or 3943."
                        )
                    else:
                        suggestions = suggest_routes(orders, rdd_input)
                        st.session_state.raw_df      = df
                        st.session_state.orders      = orders
                        st.session_state.rdd         = rdd_input
                        st.session_state.trucks_3322 = suggestions.get('3322', [])
                        st.session_state.trucks_3943 = suggestions.get('3943', [])

                        # Clear stale rate inputs from prior sessions
                        for k in [k for k in st.session_state if k.startswith('rate_')]:
                            del st.session_state[k]

                        st.session_state.step = 'review'
                        st.rerun()

                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    st.exception(e)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Review & Edit
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 'review':
    hdr_l, hdr_r = st.columns([5, 2])
    hdr_l.subheader(
        f"Step 2 — Review Routes  |  RDD: {st.session_state.rdd}"
    )
    with hdr_r:
        ca, cb = st.columns(2)
        if ca.button("← Start Over"):
            st.session_state.step = 'upload'
            st.rerun()
        if cb.button("✅ Finalize & Copy", type="primary"):
            # Save all rates NOW before widgets disappear on step switch
            captured = {}
            for orig in ['3322', '3943']:
                k = ORIGIN_KEYS[orig]
                for truck in st.session_state[k]:
                    rk = f"rate_{k}_{truck['truck_number']}"
                    captured[rk] = st.session_state.get(rk, '')
            st.session_state['_captured_rates'] = captured
            st.session_state.step = 'export'
            st.rerun()

    n3322 = len(st.session_state.trucks_3322)
    n3943 = len(st.session_state.trucks_3943)
    st.caption(
        f"**{n3322}** truck(s) from Origin 3322  |  "
        f"**{n3943}** truck(s) from Origin 3943  |  "
        f"Max **{MAX_PALLETS} pallets** / **{MAX_WEIGHT:,} lbs** per truck"
    )

    with st.expander("🔍 Debug — extracted cities from uploaded file"):
        for o in st.session_state.orders:
            st.write(f"Origin {o['origin']} → **{o['city']}, {o['state']}** | {o['pallets']} pal | {o['weight']:,.0f} lbs | _{o['dest_name'][:60]}_")

    st.divider()

    tab1, tab2 = st.tabs([ORIGIN_LABELS['3322'], ORIGIN_LABELS['3943']])
    with tab1:
        render_origin_editor('3322')
    with tab2:
        render_origin_editor('3943')


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Finalize & Copy
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 'export':
    st.subheader("Step 3 — Finalize & Copy Routes")

    if st.button("← Back to Review"):
        st.session_state.step = 'review'
        st.rerun()

    try:
        rdd          = st.session_state.rdd
        save_payload = {'3322': [], '3943': []}
        lines        = ["TQYL rates and routes below:", ""]

        for origin, label in [('3322', 'Walnut, CA OB:'), ('3943', 'Brockport, NY OB:')]:
            key    = ORIGIN_KEYS[origin]
            trucks = st.session_state[key]
            if not any(t['stops'] for t in trucks):
                continue
            lines.append(label)
            for truck in trucks:
                if not truck['stops']:
                    continue
                rate_key = f"rate_{key}_{truck['truck_number']}"
                raw_rate = st.session_state.get('_captured_rates', {}).get(rate_key, '')
                rate_val = None
                try:
                    if raw_rate:
                        rate_val = float(str(raw_rate).replace('$', '').replace(',', ''))
                except ValueError:
                    pass
                rs = build_route_string(truck['truck_number'], truck['stops'], rate_val)
                lines.append(rs)
                save_payload[origin].append({
                    'truck_number': truck['truck_number'],
                    'stops':        truck['stops'],
                    'rate':         rate_val,
                })
            lines.append("")

        email_text = "\n".join(lines).strip()

        st.success("✅ Routes ready — select all text below and paste into your email to Dale/Carl.")
        st.text_area(
            "📋 Copy and paste into email:",
            value=email_text,
            height=420,
            key="_email_out",
        )

        # Save to history once per week per origin
        for origin in ['3322', '3943']:
            if save_payload[origin] and not route_exists_for_week(rdd, origin):
                save_routes(rdd, origin, save_payload[origin])
        st.caption("✓ Routes saved to history for future weeks.")

    except Exception as e:
        st.error(f"Error building routes: {e}")
        st.exception(e)
