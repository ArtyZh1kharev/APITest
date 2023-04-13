from fastapi import FastAPI
import uvicorn

#Creating the fastapi app side

app = FastAPI()

#GET
@app.get("/")
def root():
    return {"message":"Main Page for APITest app."}

@app.get("/buildings")
def get_buildings():
    return {"message":"Buildings"}

@app.get("/buildings/{building_id}")
def get_building():
    return {"message":"Buidling with building id"}

@app.get("/buildings/{building_id}/areas")
def get_building_areas():
    return {"message":"Building areas"}

@app.get("/buildings/{building_id}/areas/{area_id}")
def get_buildiing_area():
    return {"message":"Building area with area id"}

#ADD 
@app.post("/buildings/{building_id}")
def create_building():
    return {"message":"Create buidling"}

@app.post("/buildings/{building_id}/areas/{area_id}")
def create_buidling_area():
    return {"message":"Create buidling area"}

#UPDATE
@app.put("/buildings/{building_id}")
def update_building(id: int):
    return {"message ":"Update building info"}

@app.put("/buildings/{building_id}/areas/{area_id}")
def update_area(id: int):
    return {"message":"Update building area info"}

#DELETE 
@app.delete("/buildings/{building_id}")
def delete_building(id: int):
    return {"message":"Delete buidling"}

@app.delete("/buildings/{building_id}/area/{area_id}")
def delete_building_area(id: int):
    return {"message":"Delete buidling area"}