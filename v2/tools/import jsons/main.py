import sqlite3
import importlib

DB_PATH = "./data/mobypark.db"

IMPORTERS = [
    "import_users",
    "import_parking_lots",
    "import_vehicles",
    "import_sessions",
    "import_reservations",
    "import_payments",
]

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")

        for mod_name in IMPORTERS:
            try:
                mod = importlib.import_module(mod_name)
            except ModuleNotFoundError:
                print(f"[skip] {mod_name}.py not found.")
                continue

            if not hasattr(mod, "run"):
                print(f"[skip] {mod_name}.py has no run(conn) function.")
                continue

            print(f"[run] {mod_name}.run(conn)")
            mod.run(conn)

        print("All available imports finished.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
