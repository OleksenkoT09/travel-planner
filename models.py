# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    # Зв'язок з місцями
    places = relationship("ProjectPlace", back_populates="project")


class ProjectPlace(Base):
    __tablename__ = "project_places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    external_id = Column(String, index=True, nullable=False)     # наприклад, ID з API музею/галереї
    notes = Column(String, nullable=True)
    visited = Column(Boolean, default=False)

    # Зворотний зв'язок
    project = relationship("Project", back_populates="places")
