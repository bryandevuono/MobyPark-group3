import sqlite3
import os
import sys
import importlib
from pathlib import Path

tools_dir = Path(__file__).parent
import_jsons_dir = tools_dir / "import_jsons"
sys.path.insert(0, str(import_jsons_dir))

db_path = "./data/mobypark.db"
data_dir = "./data"

try:
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    # Create database file if it doesn't exist
    if not os.path.exists(db_path):
        open(db_path, 'a').close()
        print(f"Created new database at {db_path}")

    # Read and execute SQL schema
    sql_path = "./tools/init.sql"
    if not os.path.exists(sql_path):
        print(f"ERROR: SQL schema file not found at {sql_path}")
        sys.exit(1)

    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    conn = sqlite3.connect(db_path)
    conn.executescript(sql)
    conn.commit()
    print("Database schema initialized successfully.")

    # Verify that tables were created
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Created tables: {', '.join([t[0] for t in tables])}")

    if len(tables) == 0:
        print("ERROR: No tables were created!")
        conn.close()
        sys.exit(1)

except Exception as e:
    print(f"ERROR during database initialization: {e}")
    sys.exit(1)

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
import_errors = []
for module_name, json_file in import_modules:
    try:
        json_path = f"./tools/import_jsons/data/{json_file}"
        if not os.path.exists(json_path):
            print(f"[{module_name}] Skipping - {json_file} not found")
            continue
        module = importlib.import_module(module_name)
        if not hasattr(module, "run"):
            print(f"[{module_name}] Skipping - no run() function found")
            continue

        module.run(conn)
        print(f"[{module_name}] Successfully imported data from {json_file}")
    except ModuleNotFoundError:
        print(f"[{module_name}] Skipping - module not found")
    except Exception as e:
        error_msg = f"[{module_name}] Error importing data: {e}"
        print(error_msg)
        import_errors.append(error_msg)

# Verify that at least some basic data was imported
try:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    user_count = cursor.fetchone()[0]
    print(f"\nVerification: {user_count} users in database")

    if user_count == 0:
        print("WARNING: No users were imported. Database may not be properly initialized.")
except Exception as e:
    print(f"WARNING: Could not verify database contents: {e}")

conn.close()

if import_errors:
    print(f"\n⚠ Database initialized with {len(import_errors)} import errors")
else:
    print("\n✓ Database initialized successfully at ./data/mobypark.db")