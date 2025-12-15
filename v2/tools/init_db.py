import sqlite3
import os
import sys
import importlib
from pathlib import Path

tools_dir = Path(__file__).parent
import_jsons_dir = tools_dir / "import jsons"
sys.path.insert(0, str(import_jsons_dir))

db_path = "./data/mobypark.db"
data_dir = "./data"

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(db_path):
    open(db_path, 'a').close()
    print(f"Created new database at {db_path}")

with open("./tools/init.sql", "r", encoding="utf-8") as f:
    sql = f.read()

conn = sqlite3.connect(db_path)
conn.executescript(sql)
conn.commit()
print("Database schema initialized successfully.")

# Import data from JSON files
# Order is important due to foreign key dependencies!!!!!!!!

import_modules = [
    ("import_users", "users.json"),
    ("import_parking_lots", "parking-lots.json"),
    ("import_vehicles", "vehicles.json"),
    ("import_sessions", "pdata/p1-sessions.json"),
    ("import_reservations", "reservations.json"),
    ("import_payments", "payments.json"),
]

print("\nStarting data import...")
for module_name, json_file in import_modules:
    try:
        json_path = f"./tools/import jsons/data/{json_file}"
        if not os.path.exists(json_path):
            print(f"[{module_name}] Skipping - {json_file} not found")
            continue
        module = importlib.import_module(module_name)
        if not hasattr(module, "run"):
            print(f"[{module_name}] Skipping - no run() function found")
            continue

        module.run(conn)
    except ModuleNotFoundError:
        print(f"[{module_name}] Skipping - module not found")
    except Exception as e:
        print(f"[{module_name}] Error importing data: {e}")

conn.close()
print("\n✓ Database initialized successfully at ./data/mobypark.db")