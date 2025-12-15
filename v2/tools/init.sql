-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    role TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    birth_year INTEGER,
    active BOOLEAN DEFAULT TRUE
);

-- Create parking_lots table
CREATE TABLE IF NOT EXISTS parking_lots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT,
    address TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    reserved INTEGER DEFAULT 0,
    tariff REAL,
    daytariff REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latitude REAL,
    longitude REAL
);

-- Create vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_id INTEGER NOT NULL,
    license_plate_clean TEXT,
    license_plate TEXT UNIQUE NOT NULL,
    make TEXT,
    model TEXT,
    color TEXT,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lot_id) REFERENCES parking_lots(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lot_id) REFERENCES parking_lots(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES parking_sessions(session_id) ON DELETE SET NULL,
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id) ON DELETE SET NULL
);

CREATE TABLE hotels (
	hotel_id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
    address TEXT,
	PRIMARY KEY (hotel_id)
);

-- Insert sample data
-- Default admin user
INSERT OR IGNORE INTO users (id, username, password_hash, name, email, phone, role, created_at, birth_year, active) VALUES
(1, 'admin', 'admin123', 'Administrator', 'admin@mobypark.com', NULL, 'admin', CURRENT_TIMESTAMP, NULL, TRUE),
(2, 'testuser', 'password123', 'Test User', 'test@mobypark.com', NULL, 'user', CURRENT_TIMESTAMP, NULL, TRUE);

-- Sample parking lots
INSERT OR IGNORE INTO parking_lots (name, location, address, capacity, reserved, tariff, daytariff, created_at, latitude, longitude) VALUES
('Central Station Parking', 'Amsterdam', 'Stationsplein 1', 200, 0, 3.50, 25.00, CURRENT_TIMESTAMP, NULL, NULL),
('Airport Parking P1', 'Amsterdam', 'Schiphol Airport', 500, 0, 4.00, 30.00, CURRENT_TIMESTAMP, NULL, NULL),
('City Center Mall', 'Amsterdam', 'Dam Square 10', 150, 0, 2.50, 20.00, CURRENT_TIMESTAMP, NULL, NULL),
('Rotterdam Centraal', 'Rotterdam', 'Stationsplein 1', 300, 0, 3.00, 22.00, CURRENT_TIMESTAMP, NULL, NULL),
('Utrecht CS Parking', 'Utrecht', 'Stationsplein 14', 250, 0, 3.25, 24.00, CURRENT_TIMESTAMP, NULL, NULL);

-- Sample vehicles
INSERT OR IGNORE INTO vehicles (users_id, license_plate_clean, license_plate, make, model, color, year, created_at) VALUES
(2, '12ABC3', '12-ABC-3', 'Toyota', 'Corolla', 'Blue', NULL, CURRENT_TIMESTAMP),
(2, '45DEF6', '45-DEF-6', 'Ford', 'Transit', 'White', NULL, CURRENT_TIMESTAMP);

-- Create user and hotel
INSERT OR IGNORE INTO users (id, username, password_hash, name, email, phone, role, created_at, birth_year, active) VALUES
(3, 'hotel_user', 'password1234', 'Test User', 'test2@mobypark.com', NULL, 'user', CURRENT_TIMESTAMP, NULL, TRUE);

INSERT OR IGNORE INTO hotels (hotel_id, name, address) VALUES
(1, 'hotel1', 'Naamlaan 156');