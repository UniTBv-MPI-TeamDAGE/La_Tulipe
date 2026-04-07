import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.color_service import (
    get_all_colors,
    get_color_or_404,
    create_color,
    update_color,
    delete_color,
)
from app.models.color import Color


def test_get_all_colors():
    db = MagicMock()

    colors = [Color(id=1, name="Red"), Color(id=2, name="Blue")]
    db.query().order_by().all.return_value = colors

    result = get_all_colors(db)

    assert result == colors


def test_get_color_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException):
        get_color_or_404(1, db)


def test_get_color_success():
    db = MagicMock()
    color = Color(id=1, name="Red")
    db.query().filter().first.return_value = color

    result = get_color_or_404(1, db)

    assert result == color


def test_create_color_duplicate():
    db = MagicMock()
    db.query().filter().first.return_value = Color()

    with pytest.raises(HTTPException):
        create_color(name="Red", hex_code="#FF0000", db=db)


def test_create_color_success():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = create_color(name="Red", hex_code="#FF0000", db=db)

    assert result.name == "Red"
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_update_color_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException):
        update_color(color_id=1, name="New", hex_code=None, db=db)


def test_update_color_name_success():
    db = MagicMock()

    color = Color(id=1, name="Old", hex_code="#000000")

    db.query().filter().first.side_effect = [color, None]

    result = update_color(color_id=1, name="New", hex_code=None, db=db)

    assert result.name == "New"
    db.commit.assert_called_once()


def test_update_color_duplicate_name():
    db = MagicMock()

    color = Color(id=1, name="Old")

    db.query().filter().first.side_effect = [
        color,         
        Color()        
    ]

    with pytest.raises(HTTPException):
        update_color(color_id=1, name="Existing", hex_code=None, db=db)


def test_update_color_hex_only():
    db = MagicMock()

    color = Color(id=1, name="Red", hex_code="#000000")
    db.query().filter().first.return_value = color

    result = update_color(color_id=1, name=None, hex_code="#FF0000", db=db)

    assert result.hex_code == "#FF0000"
    db.commit.assert_called_once()


def test_delete_color_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException):
        delete_color(1, db)


def test_delete_color_success():
    db = MagicMock()

    color = Color(id=1, name="Red")
    db.query().filter().first.return_value = color

    delete_color(1, db)

    db.delete.assert_called_once_with(color)
    db.commit.assert_called_once()