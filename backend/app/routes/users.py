from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.auth import UpdateMeRequest, UserMeResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "nume": current_user.nume,
        "email": current_user.email,
        "telefon": current_user.telefon,
    }


@router.put("/me", response_model=UserMeResponse)
def update_me(
    data: UpdateMeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.nume is not None:
        current_user.nume = data.nume

    if data.telefon is not None:
        current_user.telefon = data.telefon

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {
        "nume": current_user.nume,
        "email": current_user.email,
        "telefon": current_user.telefon,
    }
