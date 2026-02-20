# crud.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Project, ProjectPlace
from schemas import ProjectCreate, ProjectUpdate, PlaceCreate, PlaceUpdate, ProjectResponse, PlaceResponse
from utils import validate_artwork  # припускаю, що validate_artwork в utils.py
from datetime import date

# Функція для отримання db-сесії (використовуватимемо в Depends)
def get_db():
    from database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create project (з можливістю додати places одразу)
def create_project(db: Session, project: ProjectCreate):
    db_project = Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    if project.places:
        for external_id in project.places:
            add_place_to_project(db, project_id=db_project.id, place=PlaceCreate(external_id=external_id))
    
    return db_project

# Update project
def update_project(db: Session, project_id: int, project_update: ProjectUpdate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project_update.name is not None:
        db_project.name = project_update.name
    if project_update.description is not None:
        db_project.description = project_update.description
    if project_update.start_date is not None:
        db_project.start_date = project_update.start_date
    
    db.commit()
    db.refresh(db_project)
    return db_project

# Delete project (з перевіркою на visited places)
def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    visited_count = db.query(ProjectPlace).filter(ProjectPlace.project_id == project_id, ProjectPlace.visited == True).count()
    if visited_count > 0:
        raise HTTPException(status_code=403, detail="Cannot delete project with visited places")
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}

# List projects
def get_projects(db: Session):
    return db.query(Project).all()

# Get single project
def get_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

# Add place to project
def add_place_to_project(db: Session, project_id: int, place: PlaceCreate):
    if not validate_artwork(place.external_id):
        raise HTTPException(status_code=400, detail="Invalid external ID: artwork does not exist")
    
    db_project = get_project(db, project_id)  # Перевірка існування проекту
    
    # Перевірка дублів
    existing = db.query(ProjectPlace).filter(ProjectPlace.project_id == project_id, ProjectPlace.external_id == place.external_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Place already added to this project")
    
    # Перевірка ліміту (max 10)
    places_count = db.query(ProjectPlace).filter(ProjectPlace.project_id == project_id).count()
    if places_count >= 10:
        raise HTTPException(status_code=400, detail="Maximum 10 places per project")
    
    db_place = ProjectPlace(
        project_id=project_id,
        external_id=place.external_id,
        notes=place.notes,
        visited=False
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

# Update place (notes/visited, і перевірка завершення проекту)
def update_place(db: Session, project_id: int, place_id: int, place_update: PlaceUpdate):
    db_place = db.query(ProjectPlace).filter(ProjectPlace.id == place_id, ProjectPlace.project_id == project_id).first()
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    if place_update.notes is not None:
        db_place.notes = place_update.notes
    if place_update.visited is not None:
        db_place.visited = place_update.visited
    
    db.commit()
    db.refresh(db_place)
    
    # Перевірка, чи всі places visited -> complete project
    all_places = db.query(ProjectPlace).filter(ProjectPlace.project_id == project_id).all()
    if all(place.visited for place in all_places) and len(all_places) > 0:
        db_project = get_project(db, project_id)
        db_project.completed = True
        db.commit()
    
    return db_place

# List places for project
def get_places_for_project(db: Session, project_id: int):
    get_project(db, project_id)  # Перевірка проекту
    return db.query(ProjectPlace).filter(ProjectPlace.project_id == project_id).all()

# Get single place
def get_place(db: Session, project_id: int, place_id: int):
    db_place = db.query(ProjectPlace).filter(ProjectPlace.id == place_id, ProjectPlace.project_id == project_id).first()
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")
    return db_place
