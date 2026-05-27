CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE caregivers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    duration_minutes INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(id),
    caregiver_id INT REFERENCES caregivers(id),
    service_id INT REFERENCES services(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);