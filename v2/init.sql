-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT DEFAULT 'USER' CHECK(role IN ('USER', 'ADMIN')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create parking_lots table
CREATE TABLE IF NOT EXISTS parking_lots (
    lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    postal_code TEXT,
    latitude REAL,
    longitude REAL,
    total_capacity INTEGER NOT NULL,
    available_spots INTEGER NOT NULL,
    hourly_rate REAL NOT NULL,
    daily_rate REAL NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    license_plate TEXT UNIQUE NOT NULL,
    vehicle_name TEXT,
    brand TEXT,
    model TEXT,
    color TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create parking_sessions table
CREATE TABLE IF NOT EXISTS parking_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lot_id INTEGER NOT NULL,
    vehicle_id INTEGER NULL,
    license_plate TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL,
    duration_minutes INTEGER,
    hourly_rate REAL NOT NULL DEFAULT 0.00,
    calculated_amount REAL DEFAULT 0.00,
    status TEXT DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'COMPLETED', 'CANCELLED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (lot_id) REFERENCES parking_lots(lot_id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE SET NULL
);

-- Create reservations table
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lot_id INTEGER NOT NULL,
    vehicle_id INTEGER NULL,
    license_plate TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'CONFIRMED', 'ACTIVE', 'COMPLETED', 'CANCELLED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (lot_id) REFERENCES parking_lots(lot_id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE SET NULL
);

-- Create payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id INTEGER NULL,
    reservation_id INTEGER NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'EUR',
    payment_method TEXT,
    transaction_id TEXT,
    status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED')),
    payment_date TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES parking_sessions(session_id) ON DELETE SET NULL,
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id) ON DELETE SET NULL
);

-- Insert sample data
-- Default admin user
INSERT OR IGNORE INTO users (user_id, username, email, password_hash, full_name, role) VALUES
(1, 'admin', 'admin@mobypark.com', 'admin123', 'Administrator', 'ADMIN'),
(2, 'testuser', 'test@mobypark.com', 'password123', 'Test User', 'USER');

-- Sample parking lots
INSERT OR IGNORE INTO parking_lots (name, address, city, total_capacity, available_spots, hourly_rate, daily_rate) VALUES
('Central Station Parking', 'Stationsplein 1', 'Amsterdam', 200, 200, 3.50, 25.00),
('Airport Parking P1', 'Schiphol Airport', 'Amsterdam', 500, 500, 4.00, 30.00),
('City Center Mall', 'Dam Square 10', 'Amsterdam', 150, 150, 2.50, 20.00),
('Rotterdam Centraal', 'Stationsplein 1', 'Rotterdam', 300, 300, 3.00, 22.00),
('Utrecht CS Parking', 'Stationsplein 14', 'Utrecht', 250, 250, 3.25, 24.00);

-- Sample vehicles
INSERT OR IGNORE INTO vehicles (user_id, license_plate, vehicle_name, brand, model, color) VALUES
(2, '12-ABC-3', 'My Car', 'Toyota', 'Corolla', 'Blue'),
(2, '45-DEF-6', 'Work Van', 'Ford', 'Transit', 'White');