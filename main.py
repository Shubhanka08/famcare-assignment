from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta

app = FastAPI()

# Fake database
bookings = [
    {
        "service_id": 1,
        "caregiver_id": 101,
        "patient_id": 1,
        "date": "2026-05-26",
        "start_time": "10:00",
        "end_time": "11:00"
    }
]

# Services (IMPORTANT: used everywhere safely now)
services = {
    1: {"duration": 60},
    2: {"duration": 30}
}

# Home API
@app.get("/")
def home():
    return {"status": "FamCare running"}


# Services API
@app.get("/services")
def get_services():
    return [
        {
            "id": 1,
            "name": "Physiotherapy",
            "duration_minutes": 60,
            "price": 500
        },
        {
            "id": 2,
            "name": "Wound Dressing",
            "duration_minutes": 30,
            "price": 300
        }
    ]


# Available slots API
@app.get("/slots/available")
def available_slots(service_id: int):

    # FIX: safe validation
    if service_id not in services:
        raise HTTPException(status_code=400, detail="Invalid service_id")

    duration = services[service_id]["duration"]

    slots = []

    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")

    current = start_time

    while current < end_time:

        new_start = current
        new_end = current + timedelta(minutes=duration)

        conflict = False

        for booking in bookings:

            existing_start = datetime.strptime(booking["start_time"], "%H:%M")
            existing_end = datetime.strptime(booking["end_time"], "%H:%M")

            overlap = (new_start < existing_end and new_end > existing_start)

            if overlap:
                conflict = True
                break

        if not conflict:
            slots.append({
                "slot": current.strftime("%H:%M"),
                "duration_minutes": duration
            })

        current += timedelta(minutes=15)

    return slots


# Atomic checkout API
@app.post("/cart/checkout")
def checkout(cart: list[dict]):

    temp_bookings = []

    for item in cart:

        service_id = item["service_id"]
        caregiver_id = item["caregiver_id"]
        patient_id = item["patient_id"]
        date = item["date"]
        start_time = item["start_time"]

        # ✅ FIX: prevent KeyError crash (IMPORTANT)
        if service_id not in services:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid service_id {service_id}"
            )

        duration = services[service_id]["duration"]

        start = datetime.strptime(start_time, "%H:%M")
        end = start + timedelta(minutes=duration)

        for booking in bookings:

            existing_start = datetime.strptime(booking["start_time"], "%H:%M")
            existing_end = datetime.strptime(booking["end_time"], "%H:%M")

            caregiver_conflict = (caregiver_id == booking["caregiver_id"])
            patient_conflict = (patient_id == booking["patient_id"])

            overlap = (start < existing_end and end > existing_start)

            if overlap and caregiver_conflict:
                raise HTTPException(
                    status_code=400,
                    detail=f"Caregiver unavailable at {start_time}"
                )

            if overlap and patient_conflict:
                raise HTTPException(
                    status_code=400,
                    detail=f"Patient has overlapping service at {start_time}"
                )

        temp_bookings.append({
            "service_id": service_id,
            "caregiver_id": caregiver_id,
            "patient_id": patient_id,
            "date": date,
            "start_time": start_time,
            "end_time": end.strftime("%H:%M")
        })

    # Atomic commit
    bookings.extend(temp_bookings)

    return {
        "message": "Checkout successful",
        "bookings": temp_bookings
    }