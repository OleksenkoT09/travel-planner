# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    PlaceCreate, PlaceUpdate, PlaceResponse
)
from crud import (
    get_db, create_project, update_project, delete_project,
    get_projects, get_project,
    add_place_to_project, update_place, get_places_for_project, get_place
)
from models import Base
from database import engine

# Створення таблиць при запуску (можна прибрати, якщо використовуєш test_db.py)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Planner API",
    redirect_slashes=False
    )

# Ендпоінти для Projects
@app.post("/projects/", response_model=ProjectResponse)
def api_create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, project)

@app.put("/projects/{project_id}", response_model=ProjectResponse)
def api_update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    return update_project(db, project_id, project)

@app.delete("/projects/{project_id}")
def api_delete_project(project_id: int, db: Session = Depends(get_db)):
    return delete_project(db, project_id)

@app.get("/projects/", response_model=list[ProjectResponse])
def api_get_projects(db: Session = Depends(get_db)):
    return get_projects(db)

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def api_get_project(project_id: int, db: Session = Depends(get_db)):
    return get_project(db, project_id)

# Ендпоінти для Places в Project
@app.post("/projects/{project_id}/places/", response_model=PlaceResponse)
def api_add_place(project_id: int, place: PlaceCreate, db: Session = Depends(get_db)):
    return add_place_to_project(db, project_id, place)

@app.put("/projects/{project_id}/places/{place_id}", response_model=PlaceResponse)
def api_update_place(project_id: int, place_id: int, place: PlaceUpdate, db: Session = Depends(get_db)):
    return update_place(db, project_id, place_id, place)

@app.get("/projects/{project_id}/places/", response_model=list[PlaceResponse])
def api_get_places(project_id: int, db: Session = Depends(get_db)):
    return get_places_for_project(db, project_id)

@app.get("/projects/{project_id}/places/{place_id}", response_model=PlaceResponse)
def api_get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    return get_place(db, project_id, place_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
