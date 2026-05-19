from fastapi import FastAPI, HTTPException

STUDENT_N = 7
app = FastAPI(title=f"Hairdresser Service Catalog N{STUDENT_N}")

# Персоналізовані ID (100 * 7 + 1...) та послуги перукарні
SERVICES = {
    701: {"id": 701, "name": "Чоловіча стрижка", "price": 300.0, "available": True},
    702: {"id": 702, "name": "Жіноче фарбування", "price": 1200.0, "available": True},
    703: {"id": 703, "name": "Вечірня зачіска", "price": 800.0, "available": False}
}

@app.get("/services")
def get_all_services():
    """Повертає список усіх перукарських послуг"""
    return {"student_id": STUDENT_N, "services": list(SERVICES.values())}

@app.get("/services/{service_id}")
def get_service(service_id: int):
    """Повертає інформацію про конкретную послугу за ID"""
    if service_id not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"student_id": STUDENT_N, "data": SERVICES[service_id]}
