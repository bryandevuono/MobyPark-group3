import json
import sqlite3

PARKING_LOTS_JSON = "./tools/import_jsons/data/parking-lots.json"

def run(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    with open(PARKING_LOTS_JSON, "r", encoding="utf-8") as f:
        lots_data = json.load(f)

    # parking-lots.json is an object keyed by id, so take the values
    lots = list(lots_data.values())

    sql = """
        INSERT OR REPLACE INTO parking_lots
            (id, name, location, address, capacity, reserved, tariff, daytariff, created_at, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for lot in lots:
        coords = lot.get("coordinates", {})
        cur.execute(sql, (
            int(lot["id"]),
            lot["name"],
            lot.get("location"),
            lot.get("address"),
            int(lot.get("capacity", 0)),
            int(lot.get("reserved", 0)),
            float(lot.get("tariff")) if lot.get("tariff") is not None else None,
            float(lot.get("daytariff")) if lot.get("daytariff") is not None else None,
            lot.get("created_at"),
            coords.get("lat"),
            coords.get("lng"),
        ))
        conn.commit()

    print(f"[parking_lots] imported {len(lots)} records (duplicates replaced)")
