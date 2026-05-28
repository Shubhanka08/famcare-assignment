# famcare-assignment
# FamCare Backend – Multi-Service Booking System

## Overview
A FastAPI backend for a healthcare booking system that supports multi-service checkout with strict scheduling constraints and atomic booking guarantees.

---

## What This System Does

- Manages healthcare services with fixed durations
- Generates real-time 15-minute slot availability
- Prevents caregiver double booking
- Prevents patient schedule overlap
- Supports multi-service cart checkout
- Ensures atomic booking (all-or-nothing)

---

## Core Engineering Logic

- Overlap detection using full service duration (start → end time)
- Conflict validation for both caregiver and patient
- Slot filtering based on existing bookings
- Atomic checkout using staging (`temp_bookings`)
- If any validation fails → entire transaction is rolled back

---

## API Endpoints

- `GET /services` → List all services  
- `GET /slots/available?service_id=` → Get available time slots  
- `POST /cart/checkout` → Atomic multi-service booking  
<img width="2856" height="1650" alt="image" src="https://github.com/user-attachments/assets/5c1b93c5-4a67-4109-8f1c-b501fa71dddb" />

---

## Atomic Checkout Guarantee

This system ensures **no partial bookings ever occur**:

1. Validate all booking requests
2. Temporarily store valid bookings
3. Commit only if all validations pass
4. Otherwise reject entire request

---
# FamCare Backend – Multi-Service Booking System

## Overview

FamCare Backend is a FastAPI-based scheduling system for a home healthcare platform.

It allows patients to book multiple healthcare services in a single checkout while ensuring strict scheduling constraints and conflict-free appointments.

The system focuses on real-world booking reliability using atomic transactions and full-duration overlap validation.

---

## Core Features

- Multi-service booking in a single checkout
- Real-time 15-minute slot generation
- Caregiver availability management
- Patient conflict prevention
- Atomic checkout (all-or-nothing booking)
- Full duration-based overlap detection

---

## Problem It Solves

In healthcare scheduling, multiple bookings can overlap across caregivers and patients.

This system ensures:
- No caregiver is double-booked
- No patient has overlapping services
- No partial booking failures in checkout
- Accurate time-slot allocation based on service duration

---

## API Endpoints

### 1. Get Services
GET /services

Returns all available healthcare services.

---

### 2. Get Available Slots
GET /slots/available?service_id=


Returns 15-minute interval slots excluding conflicts.

---

### 3. Atomic Checkout

POST /cart/checkout


Request:
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

---

Behavior:

Validates all requests
Checks caregiver + patient conflicts
Uses full-duration overlap logic
Commits only if all items are valid
Fails entire request if any conflict exists
Conflict Detection Logic

A booking is considered conflicting if:

start_time < existing_end AND end_time > existing_start

This ensures accurate real-world overlap prevention.

Atomic Checkout Guarantee

The system ensures strict atomicity:

All bookings are validated first
Temporary staging of valid bookings
Final commit only if all checks pass
Any failure → entire transaction rejected

No partial bookings are ever allowed.

Tech Stack
FastAPI
Python
Pytest
In-memory data structures (assignment scope)
Testing

---

Run tests:

python -m pytest tests -v

Expected result:

3/3 tests passed
<img width="2294" height="542" alt="image" src="https://github.com/user-attachments/assets/7c8f914a-5d40-4056-8988-fe5dad06a4d6" />

---

Key Highlights
Production-style booking system design
Real-world scheduling conflict handling
Clean atomic transaction logic
Duration-based overlap detection (not naive slot matching)
Scalable architecture ready for database integration
Notes

This project is built as a backend engineering assignment demonstrating system design thinking, correctness in scheduling logic, and API reliability under constraints.


---

# Done

Now just run:

```bash
git add README.md
git commit -m "final shortlisting README"
git push origin main

---


## Testing

```bash
python -m pytest tests -v

