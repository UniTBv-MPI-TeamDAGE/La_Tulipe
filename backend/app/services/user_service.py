from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UpdateMeRequest


def get_me(current_user: User) -> dict[str, str | None]:
    return {
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
    }


def update_me(
    data: UpdateMeRequest,
    db: Session,
    current_user: User,
) -> dict[str, str | None]:
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
