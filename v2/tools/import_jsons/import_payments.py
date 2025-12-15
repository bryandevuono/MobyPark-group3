import json
import sqlite3
from datetime import datetime
from pathlib import Path

PAYMENTS_JSON = "./tools/import_jsons/data/payments.json"


def _cents(value) -> int:
    if value in (None, ""):
        return 0
    return int(round(float(value) * 100))


def _parse_datetime(date_str: str | None) -> str | None:
    """Payments timestamps are like '22-05-2025 09:09:1747898315'.
    We drop the trailing unix digits and keep day + hour:minute.
    """
    if not date_str:
        return None

    trimmed = date_str.strip()
    for fmt, slice_len in (("%d-%m-%Y %H:%M", 16), ("%d-%m-%Y %H:%M:%S", 19)):
        try:
            dt = datetime.strptime(trimmed[:slice_len], fmt)
            return dt.isoformat()
        except ValueError:
            continue
    return None


def _get_user_id_by_username(cur: sqlite3.Cursor, username: str | None):
    if not username:
        return None
    cur.execute("SELECT id FROM users WHERE username = ? LIMIT 1", (username,))
    row = cur.fetchone()
    return row[0] if row else None


def _session_exists(cur: sqlite3.Cursor, session_id: int) -> bool:
    cur.execute("SELECT 1 FROM sessions WHERE id = ? LIMIT 1", (session_id,))
    return cur.fetchone() is not None


def run(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    with open(PAYMENTS_JSON, "r", encoding="utf-8") as f:
        payments = json.load(f)

    sql = """
        INSERT OR REPLACE INTO payments
            (id, amount, sessions_id, initiator_users_id, created_at, completed_at, hash, method, issuer, bank)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    inserted = skipped_user = skipped_session = 0
    for idx, p in enumerate(payments, start=1):
        user_id = _get_user_id_by_username(cur, p.get("initiator"))
        if not user_id:
            skipped_user += 1
            print(f"[payments] skip id={idx} (user '{p.get('initiator')}' not found)")
            continue

        session_id = p.get("session_id")
        if not session_id or not _session_exists(cur, session_id):
            skipped_session += 1
            print(f"[payments] skip id={idx} (session {session_id} missing)")
            continue

        t_data = p.get("t_data") or {}
        cur.execute(
            sql,
            (
                idx,
                _cents(p.get("amount")),
                int(session_id),
                user_id,
                _parse_datetime(p.get("created_at")),
                _parse_datetime(p.get("completed")),
                p.get("hash"),
                t_data.get("method"),
                t_data.get("issuer"),
                t_data.get("bank"),
            ),
        )
        inserted += 1

    conn.commit()
    total = len(payments)
    print(
        f"[payments] imported={inserted} "
        f"skipped_user={skipped_user} skipped_session={skipped_session} total={total}"
    )
