from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.user import UpdateMeRequest, UserMeResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
    }


@router.put("/me", response_model=UserMeResponse)
def update_me(
    data: UpdateMeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.name is not None:
        current_user.name = data.name

    if data.phone is not None:
        current_user.phone = data.phone

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
    }
