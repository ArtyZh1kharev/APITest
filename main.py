from fastapi import FastAPI
import uvicorn

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, ForeignKey, CheckConstraint

#Creating tables for buidling + area 
Base = declarative_base()

class Building(Base):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), unique=True)
    
class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key = True)
    name = Column(String(255))
    light_value = Column(Integer, CheckConstraint('lightvalue >= 0 AND lighvalue <= 100'))
    temp_value = Column(Integer, CheckConstraint('temp_value >= 0 AND temp_value <= 40'))

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
def get_building(building_id: int):
    return {"message":"Buidling with building id"}

@app.get("/buildings/{building_id}/areas")
def get_building_areas(building_id: int):
    return {"message":"Building areas"}

@app.get("/buildings/{building_id}/areas/{area_id}")
def get_building_area(building_id: int, area_id: int):
    return {"message":"Building area with area id"}

#ADD 
@app.post("/buildings")
def create_building():
    return {"message":"Create buidling"}

@app.post("/buildings/{building_id}/areas")
def create_building_area():
    return {"message":"Create buidling area"}

#UPDATE
@app.put("/buildings/{building_id}")
def update_building(building_id: int):
    return {"message ":"Update building info"}

@app.put("/buildings/{building_id}/areas/{area_id}")
def update_area(building_id: int):
    return {"message":"Update building area info"}

#DELETE 
@app.delete("/buildings/{building_id}")
def delete_building(building_id: int):
    return {"message":"Delete buidling"}

@app.delete("/buildings/{building_id}/area/{area_id}")
def delete_building_area(building_id: int):
    return {"message":"Delete buidling area"}