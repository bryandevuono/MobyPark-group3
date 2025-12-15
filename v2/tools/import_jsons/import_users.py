import json
import sqlite3

USERS_JSON = "./tools/import_jsons/data/users.json"

def run(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    with open(USERS_JSON, "r", encoding="utf-8") as f:
        users = json.load(f)

    sql = """
        INSERT OR REPLACE INTO users
            (id, username, password_hash, name, email, phone, role, created_at, birth_year, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for u in users:
        cur.execute(sql, (
            int(u["id"]),
            u["username"],
            u["password"],
            u["name"],
            u["email"],
            u["phone"],
            u["role"].lower(),
            u["created_at"],
            u["birth_year"],
            1 if u["active"] else 0,
        ))
        conn.commit()

    print(f"[users] imported {len(users)} records")
