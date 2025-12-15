import json
import re
import sqlite3

VEHICLES_JSON = "./tools/import_jsons/data/vehicles.json"

def _lpclean(plate: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", plate).upper()

def run(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    with open(VEHICLES_JSON, "r", encoding="utf-8") as f:
        vehicles = json.load(f)

    # quick helper to verify user exists
    def _user_exists(user_id: int) -> bool:
        cur.execute("SELECT 1 FROM users WHERE id = ? LIMIT 1", (user_id,))
        return cur.fetchone() is not None

    sql = """
        INSERT OR REPLACE INTO vehicles
            (id, users_id, license_plate_clean, license_plate, make, model, color, year, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    inserted, skipped = 0, 0
    for v in vehicles:
        uid = int(v["user_id"])
        if not _user_exists(uid):
            skipped += 1
            continue

        plate = v["license_plate"]
        cur.execute(sql, (
            int(v["id"]),
            uid,
            _lpclean(plate),
            plate,
            v.get("make"),
            v.get("model"),
            v.get("color"),
            v.get("year"),
            v.get("created_at"),
        ))
        inserted += 1

    conn.commit()
    print(f"[vehicles] imported={inserted} skipped_missing_user={skipped} total={len(vehicles)}")
