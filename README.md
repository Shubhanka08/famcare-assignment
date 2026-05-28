# FamCare Backend – Multi-Service Booking System

## Overview

FamCare Backend is a FastAPI-based scheduling system for a home healthcare platform.

The system allows patients to book multiple healthcare services in a single checkout while ensuring:
- No caregiver double booking
- No patient scheduling conflicts
- Atomic booking behavior (all-or-nothing)
- Accurate time-slot management using full service duration

The focus of this assignment is backend correctness, scheduling reliability, and transaction safety.

---

## Core Features

- Multi-service booking in a single checkout
- Real-time 15-minute slot generation
- Caregiver availability management
- Patient overlap prevention
- Atomic checkout handling
- Full duration-based conflict detection

---

## Problem It Solves

Healthcare appointments can overlap across caregivers and patients if scheduling is not validated correctly.

This system ensures:
- A caregiver cannot be booked for overlapping services
- A patient cannot have overlapping appointments
- Partial booking failures never occur
- Time slots are validated using complete service duration

---
<img width="2856" height="1650" alt="Screenshot 2026-05-27 114349" src="https://github.com/user-attachments/assets/c6b8ada7-bbf0-4a64-881b-a7b53e25a0f3" />


## API Endpoints

### 1. Get Services

`GET /services`

Returns all available healthcare services with duration and pricing details.

---

### 2. Get Available Slots

`GET /slots/available?service_id=`

Returns available 15-minute aligned slots after filtering conflicting bookings.

---

### 3. Atomic Checkout

`POST /cart/checkout`

Example Request:

```json
[
  {
    "service_id": 1,
    "caregiver_id": 101,
    "patient_id": 1,
    "date": "2026-05-30",
    "start_time": "10:00"
  }
]
Checkout Behavior
Validates all booking requests
Checks caregiver conflicts
Checks patient conflicts
Uses full-duration overlap logic
Commits bookings only if all validations pass
Rejects the entire request if any conflict exists
Conflict Detection Logic

A booking is considered conflicting if:

start_time < existing_end AND end_time > existing_start

This ensures proper real-world overlap prevention instead of checking only start times.

Atomic Checkout Guarantee

The system guarantees strict atomic behavior:

Validate all booking requests
Temporarily stage valid bookings
Commit only if all validations pass
Reject the entire transaction if any validation fails

This prevents partial bookings under all scenarios.

Tech Stack
FastAPI
Python
Pytest
Testing

Run tests using:

python -m pytest tests -v

Expected Result:

3/3 tests passed
API Documentation

FastAPI Swagger documentation is available at:

http://127.0.0.1:8000/docs
Project Structure
famcare-backend/
│
├── main.py
├── schema.sql
├── README.md
└── tests/
    └── test_booking.py
Key Highlights
Production-style booking logic
Full duration-based overlap validation
Atomic multi-service checkout flow
Conflict-safe scheduling system
Clean and extensible backend architecture
Notes

This project was built as a backend engineering assignment focused on:

Scheduling correctness
Conflict-safe booking
Atomic transaction behavior
Backend system design thinking

The current implementation uses in-memory storage for simplicity and assignment scope, but the architecture can be extended easily to PostgreSQL-backed persistence.

# FamCare Backend – Multi-Service Booking System

## Overview

FamCare Backend is a FastAPI-based healthcare booking engine designed for a home healthcare platform where patients can book multiple healthcare services across multiple days in a single checkout.

The system focuses on scheduling correctness, conflict prevention, and reliable transaction behavior while supporting multi-service booking workflows.

### Example Scenario

A patient can book:

- Physiotherapy (60 min) → Monday 10:00 AM  
- Wound Dressing (30 min) → Monday 3:00 PM  
- Physiotherapy (60 min) → Wednesday 10:00 AM  

All bookings are processed in **one transaction**.

---

## Core Features

✅ Multi-service booking support  
✅ 15-minute aligned slot generation  
✅ Caregiver conflict detection  
✅ Patient overlap prevention  
✅ Full duration-based booking validation  
✅ Atomic checkout (all-or-nothing booking)  
✅ Pytest-based backend testing  
✅ Database-ready backend architecture  

---

## Backend APIs

### 1. Get Services

`GET /services`

Returns available healthcare services with duration and pricing information.

---

### 2. Get Available Slots

`GET /slots/available?service_id=`

Returns available time slots for a selected service.

The system:

- generates 15-minute aligned slots
- excludes overlapping bookings
- checks caregiver conflicts
- validates availability using full service duration

---

### 3. Checkout Booking

`POST /cart/checkout`

Accepts booking items:

```json
[
  {
    "service_id": 1,
    "caregiver_id": 101,
    "patient_id": 1,
    "date": "2026-05-30",
    "start_time": "10:00"
  }
]
```

Checkout behavior:

- validates all cart items
- checks caregiver conflicts
- checks patient overlap
- validates booking duration
- commits only if every booking succeeds

If any booking fails, the full checkout is rejected.

No partial bookings are allowed.

---

## Design Decisions

### 1. Atomic Checkout

The system uses a temporary booking staging approach (`temp_bookings`) to simulate transactional behavior.

Flow:

1. Validate all requests  
2. Temporarily stage valid bookings  
3. Commit only after every validation passes  
4. Reject the entire request if any slot fails  

This guarantees **all-or-nothing booking behavior**.

In a production PostgreSQL implementation, this would be replaced using database transactions.

---

### 2. Conflict Detection Logic

Overlap validation uses **full service duration**, not start time only.

Logic:

```text
start_time < existing_end_time
AND
end_time > existing_start_time
```

Example:

A 60-minute appointment starting at **10:00 AM** blocks scheduling until **11:00 AM**.

This prevents caregiver double-booking and patient overlap.

---

### 3. Service Duration Handling

Durations are retrieved from service definitions and used dynamically during validation.

The scheduling logic is designed to avoid hardcoded booking duration assumptions.

---

## Database Design (PostgreSQL Ready)

For assignment scope, the current implementation uses in-memory storage to focus on scheduling correctness and backend behavior.

The system is designed to be migrated easily to PostgreSQL using tables such as:

- `services`
- `bookings`
- `patients`
- `caregivers`

Included:

- `schema.sql` for database structure reference

Production systems would use:

- PostgreSQL transactions
- row locking / optimistic locking
- indexed booking queries

---

## Testing

Pytest tests are included for:

- Atomic checkout behavior
- Patient conflict detection
- Checkout validation

Run tests:

```bash
python -m pytest tests -v
```

Expected result:

```text
3 passed
```

---

## API Documentation

FastAPI Swagger UI:

`http://127.0.0.1:8000/docs`

---

## Project Structure

```text
famcare-backend/
│
├── main.py
├── schema.sql
├── README.md
└── tests/
    └── test_booking.py
```

---

## Tech Stack

- FastAPI
- Python
- Pytest
- PostgreSQL-ready schema design

---

## Tradeoffs & Future Improvements

With more time, the system can be extended with:

- Full PostgreSQL persistence
- Flutter frontend integration
- Caregiver auto-assignment
- Optimistic locking / DB transactions
- Concurrent booking protection
- Authentication and patient management

---

## Key Engineering Highlights

- Conflict-safe scheduling system  
- Full duration-based overlap validation  
- Atomic multi-service booking flow  
- Backend-first architecture design  
- Clean API-driven scheduling logic  

---

## Notes

This project was built for the FamCare backend assignment with focus on:

- scheduling correctness  
- conflict prevention  
- atomic booking guarantees  
- API reliability  
- backend system design
