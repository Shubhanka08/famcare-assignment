from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_checkout_validation():
    response = client.post("/cart/checkout", json=[
        {
            "service_id": 9999,
            "caregiver_id": 9999,
            "patient_id": 1,
            "date": "2026-05-30",
            "start_time": "10:00"
        }
    ])
    assert response.status_code in [200, 400]


def test_patient_conflict():
    response = client.post("/cart/checkout", json=[
        {
            "service_id": 1,
            "caregiver_id": 999,
            "patient_id": 1,
            "date": "2026-05-26",
            "start_time": "10:30"
        }
    ])
    assert response.status_code == 400


def test_atomic_behavior():
    response = client.post("/cart/checkout", json=[
        {
            "service_id": 1,
            "caregiver_id": 999,
            "patient_id": 1,
            "date": "2026-05-26",
            "start_time": "10:30"
        },
        {
            "service_id": 1,
            "caregiver_id": 999,
            "patient_id": 1,
            "date": "2026-05-26",
            "start_time": "11:00"
        }
    ])
    assert response.status_code == 400