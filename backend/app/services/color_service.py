from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.color import Color


def get_all_colors(db: Session) -> list[Color]:
    return db.query(Color).order_by(Color.id.asc()).all()


def get_color_or_404(color_id: int, db: Session) -> Color:
    color = db.query(Color).filter(Color.id == color_id).first()
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return color


def create_color(
    *,
    name: str,
    hex_code: str | None,
    db: Session,
) -> Color:
    existing_color = db.query(Color).filter(Color.name == name).first()
    if existing_color:
        raise HTTPException(
            status_code=400,
            detail=f"Color with name '{name}' already exists",
        )

    color = Color(
        name=name,
        hex_code=hex_code,
    )
    db.add(color)
    db.commit()
    db.refresh(color)
    return color


def update_color(
    *,
    color_id: int,
    name: str | None,
    hex_code: str | None,
    db: Session,
) -> Color:
    color = db.query(Color).filter(Color.id == color_id).first()
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")

    if name is not None and name != color.name:
        existing_color = db.query(Color).filter(Color.name == name).first()
        if existing_color:
            raise HTTPException(
                status_code=400,
                detail=f"Color with name '{name}' already exists",
            )
        color.name = name

    if hex_code is not None:
        color.hex_code = hex_code

    db.add(color)
    db.commit()
    db.refresh(color)
    return color


def delete_color(color_id: int, db: Session) -> None:
    color = db.query(Color).filter(Color.id == color_id).first()
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")

    db.delete(color)
    db.commit()
