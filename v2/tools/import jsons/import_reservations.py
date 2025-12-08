import json
import sqlite3

RESERVATIONS_JSON = "./tools/import jsons/data/reservations.json"

def _cents(value) -> int:
    if value in (None, ""):
        return 0
    return int(round(float(value) * 100))

def _normalize_status(status: str) -> str:
    s = (status or "").strip().lower()
    if s == "completed":
        return "completed"
    if s in {"cancelled", "canceled"}:
        return "canceled"
    # treat "pending" (and everything else) as confirmed
    return "confirmed"

def run(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    with open(RESERVATIONS_JSON, "r", encoding="utf-8") as f:
        reservations = json.load(f)

    def _vehicle_exists(veh_id: int) -> bool:
        cur.execute("SELECT 1 FROM vehicles WHERE id = ? LIMIT 1", (veh_id,))
        return cur.fetchone() is not None

    def _lot_exists(lot_id: int) -> bool:
        cur.execute("SELECT 1 FROM parking_lots WHERE id = ? LIMIT 1", (lot_id,))
        return cur.fetchone() is not None

    sql = """
        INSERT OR REPLACE INTO reservation
            (id, vehicles_id, parking_lots_id, start_time, end_time, status, created_at, cost)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    inserted, skipped_vehicle, skipped_lot = 0, 0, 0
    for r in reservations:
        rid = int(r["id"])
        veh_id = int(r.get("vehicle_id") or 0)
        lot_id = int(r.get("parking_lot_id") or 0)

        if not veh_id or not _vehicle_exists(veh_id):
            skipped_vehicle += 1
            print(f"[reservations] skip id={rid} (vehicle {veh_id} missing)")
            continue

        if not lot_id or not _lot_exists(lot_id):
            skipped_lot += 1
            print(f"[reservations] skip id={rid} (parking_lot {lot_id} missing)")
            continue

        cur.execute(
            sql,
            (
                rid,
                veh_id,
                lot_id,
                r.get("start_time"),
                r.get("end_time"),
                _normalize_status(r.get("status")),
                r.get("created_at") or r.get("start_time"),
                _cents(r.get("cost")),
            ),
        )
        inserted += 1

    conn.commit()
    total = len(reservations)
    skipped = skipped_vehicle + skipped_lot
    print(
        f"[reservations] imported={inserted} "
        f"skipped_vehicle={skipped_vehicle} skipped_lot={skipped_lot} total={total}"
    )
