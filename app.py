import streamlit as st
import pandas as pd
import io
from db import init_db, save_routes, route_exists_for_week
from route_engine import (
    parse_raw_file, suggest_routes, build_route_string,
    MAX_PALLETS, MAX_WEIGHT,
)

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

init_db()
st.set_page_config(
    page_title="Tropicana Route Builder",
    page_icon="🍊",
    layout="wide",
)
st.title("🍊 Tropicana Walmart Route Builder")

with st.sidebar:
    st.subheader("⚙️ Admin")
    if st.button("🌱 Seed historical routes"):
        try:
            from seed_history import (
                WEEK_530_3322, WEEK_530_3943,
                WEEK_636_3322, WEEK_636_3943,
            )
            datasets = [
                ('5/30/2026',         '3322', WEEK_530_3322),
                ('5/30/2026',         '3943', WEEK_530_3943),
                ('6/3/2026-6/6/2026', '3322', WEEK_636_3322),
                ('6/3/2026-6/6/2026', '3943', WEEK_636_3943),
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
    st.caption("Click once to load historical weeks. Safe to click again — duplicates are skipped.")

ORIGIN_LABELS = {
    '3322': '🏭 Origin 3322 — Walnut, CA',
    '3943': '🏭 Origin 3943 — Brockport, NY',
}
ORIGIN_KEYS = {'3322': 'trucks_3322', '3943': 'trucks_3943'}

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
                    c1, c2, c3, c4, c5 = st.columns([5, 1, 1, 2, 1])
                    c1.write(
                        f"**{si + 1}.** {stop['city']}, {stop['state']}"
                        f"  —  _{stop.get('dest_name', '')[:50]}_"
                    )
                    if c2.button("↑", key=f"up_{key}_{ti}_{si}", disabled=(si == 0)):
                        move_up(key, ti, si)
                        st.rerun()
                    if c3.button("↓", key=f"dn_{key}_{ti}_{si}", disabled=(si == len(truck['stops']) - 1)):
                        move_down(key, ti, si)
                        st.rerun()
                    if other_nums:
                        dest_num = c4.selectbox(
                            "Move to", other_nums,
                            key=f"sel_{key}_{ti}_{si}",
                            label_visibility="collapsed",
                            format_func=lambda n: f"→ Truck {n}",
                        )
                        if c5.button("Move", key=f"mv_{key}_{ti}_{si}"):
                            move_to_truck(key, ti, si, dest_num)
                            st.rerun()
            st.divider()
            if over_p:
                st.error(f"⚠️ Over pallet limit: {total_p:.0f} / {MAX_PALLETS}")
            if over_w:
                st.error(f"⚠️ Over weight limit: {total_w:,.0f} / {MAX_WEIGHT:,} lbs")
            c_rate, c_hint = st.columns([2, 4])
            rate_key     = f"rate_{key}_{truck['truck_number']}"
            default_rate = (
                f"{truck['historical_rate']:,.0f}"
                if truck.get('historical_rate') else ""
            )
            c_rate.text_input(
                "Rate ($)",
                value=st.session_state.get(rate_key, default_rate),
                key=rate_key,
                placeholder="e.g. 2800",
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

def build_export_excel():
    raw_df = st.session_state.raw_df.copy()
    rdd    = st.session_state.rdd
    route_strings = []
    save_payload  = {'3322': [], '3943': []}
    for origin in ['3322', '3943']:
        key = ORIGIN_KEYS[origin]
        for truck in st.session_state[key]:
            if not truck['stops']:
                continue
            rate_key = f"rate_{key}_{truck['truck_number']}"
            raw_rate = st.session_state.get(rate_key, '')
            rate_val = None
            try:
                if raw_rate:
                    rate_val = float(str(raw_rate).replace('$', '').replace(',', ''))
            except ValueError:
                pass
            rs = build_route_string(truck['truck_number'], truck['stops'], rate_val)
            route_strings.append((origin, rs))
            save_payload[origin].append({
                'truck_number': truck['truck_number'],
                'stops':        truck['stops'],
                'rate':         rate_val,
            })
    origin_col = str(raw_df.columns[0])
    df_3322 = raw_df[raw_df[origin_col].astype(str).str.strip() == '3322'].copy()
    df_3943 = raw_df[raw_df[origin_col].astype(str).str.strip() == '3943'].copy()
    df_out  = pd.concat([df_3322, df_3943], ignore_index=True)
    route_col   = [''] * len(df_out)
    routes_3322 = [rs for o, rs in route_strings if o == '3322']
    routes_3943 = [rs for o, rs in route_strings if o == '3943']
    first_3943  = len(df_3322)
    for i, rs in enumerate(routes_3322):
        if i < len(df_out):
            route_col[i] = rs
    for i, rs in enumerate(routes_3943):
        idx = first_3943 + i
        if idx < len(df_out):
            route_col[idx] = rs
    df_out[''] = route_col
    for origin in ['3322', '3943']:
        if save_payload[origin] and not route_exists_for_week(rdd, origin):
            save_routes(rdd, origin, save_payload[origin])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df_out.to_excel(writer, index=False)
    buf.seek(0)
    return buf.getvalue()

if st.session_state.step == 'upload':
    st.subheader("Step 1 — Upload Tropicana Order File")
    col1, col2 = st.columns([2, 1])
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
                        st.error("No valid orders found. Ensure Origin Location ID column contains 3322 or 3943.")
                    else:
                        suggestions = suggest_routes(orders, rdd_input)
                        st.session_state.raw_df      = df
                        st.session_state.orders      = orders
                        st.session_state.rdd         = rdd_input
                        st.session_state.trucks_3322 = suggestions.get('3322', [])
                        st.session_state.trucks_3943 = suggestions.get('3943', [])
                        for k in [k for k in st.session_state if k.startswith('rate_')]:
                            del st.session_state[k]
                        st.session_state.step = 'review'
                        st.rerun()
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    st.exception(e)

elif st.session_state.step == 'review':
    hdr_l, hdr_r = st.columns([5, 2])
    hdr_l.subheader(f"Step 2 — Review Routes  |  RDD: {st.session_state.rdd}")
    with hdr_r:
        ca, cb = st.columns(2)
        if ca.button("← Start Over"):
            st.session_state.step = 'upload'
            st.rerun()
        if cb.button("✅ Finalize & Export", type="primary"):
            st.session_state.step = 'export'
            st.rerun()
    n3322 = len(st.session_state.trucks_3322)
    n3943 = len(st.session_state.trucks_3943)
    st.caption(
        f"**{n3322}** truck(s) from Origin 3322  |  "
        f"**{n3943}** truck(s) from Origin 3943  |  "
        f"Max **{MAX_PALLETS} pallets** / **{MAX_WEIGHT:,} lbs** per truck"
    )
    st.divider()
    tab1, tab2 = st.tabs([ORIGIN_LABELS['3322'], ORIGIN_LABELS['3943']])
    with tab1:
        render_origin_editor('3322')
    with tab2:
        render_origin_editor('3943')

elif st.session_state.step == 'export':
    st.subheader("Step 3 — Export")
    if st.button("← Back to Review"):
        st.session_state.step = 'review'
        st.rerun()
    with st.spinner("Building Excel file…"):
        try:
            excel_bytes = build_export_excel()
            rdd_safe    = st.session_state.rdd.replace('/', '.').replace(',', '_').replace(' ', '')
            filename = f"Tropicana_Walmart_Routes_RDD_{rdd_safe}.xlsx"
            st.success("✅ Routes saved to history and file is ready to download!")
            st.download_button(
                label="📥 Download Completed Excel",
                data=excel_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.error(f"Export error: {e}")
            st.exception(e)
    st.divider()
    st.subheader("Route Summary")
    for origin in ['3322', '3943']:
        key    = ORIGIN_KEYS[origin]
        trucks = st.session_state[key]
        if any(t['stops'] for t in trucks):
            st.markdown(f"**{ORIGIN_LABELS[origin]}**")
            for truck in trucks:
                if not truck['stops']:
                    continue
                rate_key = f"rate_{key}_{truck['truck_number']}"
                raw_rate = st.session_state.get(rate_key, '')
                rate_val = None
                try:
                    if raw_rate:
                        rate_val = float(str(raw_rate).replace('$', '').replace(',', ''))
                except ValueError:
                    pass
                st.write(f"• {build_route_string(truck['truck_number'], truck['stops'], rate_val)}")
