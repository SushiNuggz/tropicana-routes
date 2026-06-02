import json
import os
from datetime import datetime


# ── DB connection ──────────────────────────────────────────────────────────────
# Uses PostgreSQL when DATABASE_URL is set (Streamlit Cloud / production).
# Falls back to local SQLite for development.

def _pg_url():
    """Return PostgreSQL connection URL from Streamlit secrets or environment."""
    try:
        import streamlit as st
        url = st.secrets.get("DATABASE_URL")
        if url:
            return url
    except Exception:
        pass
    return os.environ.get("DATABASE_URL")


class _Conn:
    """Thin wrapper that normalises SQLite and psycopg2 into one interface.
    Uses '?' placeholders in all SQL — auto-converts to '%s' for PostgreSQL.
    """

    def __init__(self):
        url = _pg_url()
        if url:
            import psycopg2
            self._conn = psycopg2.connect(url)
            self._pg = True
        else:
            import sqlite3
            db_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "route_history.db"
            )
            self._conn = sqlite3.connect(db_path)
            self._pg = False

    def execute(self, sql, params=()):
        if self._pg:
            sql = sql.replace('?', '%s')
            cur = self._conn.cursor()
            cur.execute(sql, params)
            return cur
        return self._conn.execute(sql, params)

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, *_):
        if exc_type is None:
            self.commit()
        self.close()


# ── Schema ─────────────────────────────────────────────────────────────────────

def init_db():
    with _Conn() as conn:
        if _pg_url():
            conn.execute("""
                CREATE TABLE IF NOT EXISTS route_history (
                    id                SERIAL PRIMARY KEY,
                    week_rdd          TEXT NOT NULL,
                    origin            TEXT NOT NULL,
                    truck_number      INTEGER NOT NULL,
                    stop_keys_json    TEXT NOT NULL,
                    stops_detail_json TEXT NOT NULL,
                    rate              REAL,
                    created_at        TEXT NOT NULL
                )
            """)
        else:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS route_history (
                    id                INTEGER PRIMARY KEY AUTOINCREMENT,
                    week_rdd          TEXT NOT NULL,
                    origin            TEXT NOT NULL,
                    truck_number      INTEGER NOT NULL,
                    stop_keys_json    TEXT NOT NULL,
                    stops_detail_json TEXT NOT NULL,
                    rate              REAL,
                    created_at        TEXT NOT NULL
                )
            """)


# ── Write ──────────────────────────────────────────────────────────────────────

def save_routes(week_rdd, origin, trucks):
    """Save finalised routes to history.

    trucks: list of dicts with keys:
        truck_number  : int
        stops         : list of {city, state, dest_name, pallets, weight}
        rate          : float or None
    """
    with _Conn() as conn:
        for truck in trucks:
            stops = truck['stops']
            stop_keys = sorted(
                [f"{s['city'].upper()}|{s['state'].upper()}" for s in stops]
            )
            conn.execute(
                """
                INSERT INTO route_history
                    (week_rdd, origin, truck_number,
                     stop_keys_json, stops_detail_json, rate, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    week_rdd,
                    origin,
                    truck['truck_number'],
                    json.dumps(stop_keys),
                    json.dumps(stops),
                    truck.get('rate'),
                    datetime.now().isoformat(),
                ),
            )


# ── Read ───────────────────────────────────────────────────────────────────────

def get_all_routes_for_origin(origin):
    """Return all historical routes for an origin, most recent first."""
    with _Conn() as conn:
        cur = conn.execute(
            """
            SELECT week_rdd, truck_number, stop_keys_json,
                   stops_detail_json, rate, created_at
            FROM route_history
            WHERE origin = ?
            ORDER BY created_at DESC
            """,
            (origin,),
        )
        rows = cur.fetchall()
    return [
        {
            'week_rdd':     r[0],
            'truck_number': r[1],
            'stop_keys':    json.loads(r[2]),
            'stops':        json.loads(r[3]),
            'rate':         r[4],
            'created_at':   r[5],
        }
        for r in rows
    ]


def delete_routes_for_week(week_rdd, origin):
    """Delete all stored routes for a specific week + origin."""
    with _Conn() as conn:
        conn.execute(
            "DELETE FROM route_history WHERE week_rdd = ? AND origin = ?",
            (week_rdd, origin),
        )


def delete_all_routes():
    """Delete ALL route history (admin reset)."""
    with _Conn() as conn:
        conn.execute("DELETE FROM route_history")


def route_exists_for_week(week_rdd, origin):
    """Return True if routes are already stored for this week + origin."""
    with _Conn() as conn:
        cur = conn.execute(
            "SELECT COUNT(*) FROM route_history WHERE week_rdd = ? AND origin = ?",
            (week_rdd, origin),
        )
        count = cur.fetchone()[0]
    return count > 0
