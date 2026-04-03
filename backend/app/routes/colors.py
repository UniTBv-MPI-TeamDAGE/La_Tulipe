from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_admin
from app.models.user import User
from app.schemas.color import ColorCreate, ColorResponse, ColorUpdate
from app.services import color_service

router = APIRouter(prefix="/api/colors", tags=["colors"])


@router.get("", response_model=list[ColorResponse])
def get_colors(db: Session = Depends(get_db)):
    return color_service.get_all_colors(db=db)


@router.get("/{color_id}", response_model=ColorResponse)
def get_color(color_id: int, db: Session = Depends(get_db)):
    return color_service.get_color_or_404(color_id=color_id, db=db)


@router.post("", response_model=ColorResponse, status_code=201)
def create_color(
    data: ColorCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return color_service.create_color(
        name=data.name,
        hex_code=data.hex_code,
        db=db,
    )


@router.put("/{color_id}", response_model=ColorResponse)
def update_color(
    color_id: int,
    data: ColorUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return color_service.update_color(
        color_id=color_id,
        name=data.name,
        hex_code=data.hex_code,
        db=db,
    )


@router.delete("/{color_id}", status_code=204)
def delete_color(
    color_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    color_service.delete_color(color_id=color_id, db=db)
