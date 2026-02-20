# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    places: Optional[List[str]] = None      # список external_id, які хочемо додати одразу


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(ProjectBase):
    id: int
    completed: bool
    places: List["PlaceResponse"] = []      # forward ref — буде працювати з from_attributes

    model_config = ConfigDict(from_attributes=True)


class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None


class PlaceResponse(PlaceBase):
    id: int
    project_id: int
    visited: bool = False

    model_config = ConfigDict(from_attributes=True)


# Для уникнення помилок forward reference (якщо використовуєш старий pydantic <2.0 — можна залишити orm_mode=True)
ProjectResponse.model_rebuild()
