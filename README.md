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

## Testing

```bash
python -m pytest tests -v
