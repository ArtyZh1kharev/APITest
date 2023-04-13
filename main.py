#API TEST SCRIPT FOR SIMPLE MODELLING OF TEMPREATURE + LIGHT ADJUSTMENT IN BUILDINGS
#------------
#LANGUAGE: PYTHON3 
#ORM: SQLALCHEMY
#DATABASE: SQLITE
#------------
#BEFORE RUNNING THE APPLICATION:
# pip install fastapi 
# pip install fastapi.exceptions
# pip install sqlalchemy
# pip install sqlalchemy.orm
# pip isntall pydantic
# pip install uvicorn
#------------
#RUNNING THE APPLICATION: uvicorn main:app --reload 
#POSTMAN TESTING: JSON FORMAT FOR POST/PATCH REQUESTS, USING SCHEMA
#------------
#FULL DOCUMENTATION AVAILABLE AT http://127.0.0.1:8000/docs or http://localhost:8000/docs 


from fastapi import FastAPI
import uvicorn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.exceptions import HTTPException
#Creating classes for buidling + area 
Base = declarative_base()

class Building(Base):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), unique=True)
    areas = relationship("Area", back_populates='building')
    
class Area(Base):
    __tablename__ = 'areas'
    id = Column(Integer, primary_key = True)
    name = Column(String(255))
    light_value = Column(Integer, CheckConstraint('light_value >= 0 AND light_value <= 100'))
    temp_value = Column(Integer, CheckConstraint('temp_value >= 0 AND temp_value <= 40'))
    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship("Building", back_populates='areas')

#Creating the tables
database_url = 'sqlite:///./building.db'
engine = create_engine(database_url)
Base.metadata.create_all(bind=engine)

#Creating session factory 
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

#Setting up the dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

#Creating pydantic schema for request and responce 
class CreateBuilding(BaseModel):
    name: str

class CreateArea(BaseModel):
    name: str
    light_value: int
    temp_value: int
    building_id: int

class AreaLightTemp(BaseModel):
    light_value: int
    temp_value: int
    

#Creating the fastapi app side
app = FastAPI()

#ADD 
@app.post("/buildings", response_model=CreateBuilding)
def create_building(building: CreateBuilding, db: Session = Depends(get_db)):
    db_building = Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return CreateBuilding(**db_building.__dict__)

@app.post("/buildings/{building_id}/areas", response_model=CreateArea)
def create_building_area(area: CreateArea, db: Session = Depends(get_db)):
    db_area = Area(**area.dict())
    if db_area is None:
        raise HTTPException(status_code=404)
    if db_area.temp_value >= 40 or db_area.temp_value < -1:
        raise ValueError("Invalid value. Expected 40 >= value >= 0.")
    if db_area.light_value > 100 or db_area.light_value < -1:
        raise ValueError("Invalid value. Expected 100 >= value >= 0.")
    db.add_all([db_area])
    db.commit()
    db.refresh(db_area)
    return CreateArea(**db_area.__dict__)

#GET
@app.get("/")
def root():
    return {"message":"Main Page for APITest app."}

@app.get("/buildings")
def get_buildings(db: Session = Depends(get_db)):
    buildings = db.query(Building).all()
    return buildings

@app.get("/buildings/{building_id}")
def get_building(building_id: int,db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.id == building_id).first()
    if building is None:
        raise HTTPException(status_code=404)
    return building

@app.get("/buildings/{building_id}/areas")
def get_building_areas(building_id: int, db: Session = Depends(get_db)):
    areas = db.query(Area).filter(Area.building_id==building_id).all()
    return areas

@app.get("/buildings/{building_id}/areas/{area_id}")
def get_building_area(building_id: int, area_id: int,db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.id == area_id, Area.building_id==building_id).first()
    if area is None:
        raise HTTPException(status_code=404)
    return area


#UPDATE the light and temp values
@app.patch("/buildings/{building_id}/areas/{area_id}")
def update_area(building_id: int, area_id: int,area: AreaLightTemp, db: Session = Depends(get_db)):
    db_area = db.query(Area).filter(Area.id == area_id, Area.building_id == building_id).first()
    if db_area is None:
        raise HTTPException(status_code=404)
    if db_area.light_value >= 100 or db_area.light_value < -1:
        raise ValueError("Invalid value. Expected 100 >= int(value) >= 0.")
    if db_area.temp_value >= 40 or db_area.temp_value < -1:
        raise ValueError("Invalid value. Expected 40 >= int(value) >= 0.")
    db_area.temp_value = area.temp_value
    db_area.light_value = area.light_value
    db.commit()
    db.refresh(db_area)
    return db_area

#DELETE 
@app.delete("/buildings/{building_id}")
def delete_building(building_id: int, db: Session = Depends(get_db)):
    db_building = db.query(Building).filter(Building.id == building_id).first()
    if db_building is None:
        raise HTTPException(status_code=404)
    db.delete(db_building)
    db.commit()
    db.flush()
    return {"message":f"Deleted building {building_id}."}

@app.delete("/buildings/{building_id}/areas/{area_id}")
def delete_building_area(building_id: int, area_id:int, db: Session = Depends(get_db)):
    db_area = db.query(Area).filter(Area.id == area_id, Area.building_id == building_id).first()
    if db_area is None:
        raise HTTPException(status_code=404)
    else:
        db.delete(db_area)
        db.commit()
        db.flush()
        return {"message":f"Deleted area {area_id} in building {building_id}."}
