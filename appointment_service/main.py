from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

STUDENT_N = 7
app = FastAPI(title=f"Hairdresser Appointment Service N{STUDENT_N}")

# Звернення по внутрішній мережі Docker до сервісу послуг
CATALOG_SERVICE_URL = f"http://service-catalog-07:8000"

class AppointmentRequest(BaseModel):
    service_id: int
    client_name: str
    time_slot: str

APPOINTMENTS = []

@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    """Створює запис на візит, перевіряючи доступність послуги"""
    try:
        response = requests.get(f"{CATALOG_SERVICE_URL}/services/{req.service_id}")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Service Catalog is unavailable")
    
    if response.status_code == 404:
        raise HTTPException(status_code=400, detail="Service does not exist")
        
    res_data = response.json()
    service_data = res_data["data"]
    
    if not service_data["available"]:
        raise HTTPException(status_code=400, detail="This service is currently unavailable for booking")
        
    new_appointment = {
        "appointment_id": len(APPOINTMENTS) + 1,
        "service_id": req.service_id,
        "service_name": service_data["name"],
        "client_name": req.client_name,
        "time_slot": req.time_slot,
        "price": service_data["price"],
        "status": "Confirmed",
        "student_id": STUDENT_N
    }
    APPOINTMENTS.append(new_appointment)
    return new_appointment

@app.get("/appointments")
def get_all_appointments():
    """Повертає список усіх створених записів перукарні"""
    return {"student_id": STUDENT_N, "appointments": APPOINTMENTS}
