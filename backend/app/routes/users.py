from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.user import UpdateMeRequest, UserMeResponse
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return user_service.get_me(current_user=current_user)


@router.put("/me", response_model=UserMeResponse)
def update_me(
    data: UpdateMeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_me(data=data, db=db, current_user=current_user)
