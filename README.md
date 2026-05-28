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
