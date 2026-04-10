from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.category import Category
from app.models.product import Product
from app.services.category_service import (
    create_category,
    delete_category,
    get_category_or_404,
    get_products_by_category,
    update_category,
)


def test_get_category_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as e:
        get_category_or_404(1, db)

    assert e.value.status_code == 404

def test_get_category_success():
    db = MagicMock()
    category = Category(id=1, name="Roses")
    db.query().filter().first.return_value = category

    result = get_category_or_404(1, db)

    assert result == category    

def test_create_category_duplicate():
    db = MagicMock()
    db.query().filter().first.return_value = Category()

    with pytest.raises(HTTPException) as e:
        create_category("Roses", db)

    assert e.value.status_code == 409  
    
def test_create_category_success():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = create_category("Tulips", db)

    assert result.name == "Tulips"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()      

def test_update_category_name():
    db = MagicMock()
    category = Category(id=1, name="Old")
    db.query().filter().first.return_value = category

    result = update_category(1, "New", db)

    assert result.name == "New"
    db.commit.assert_called_once()   
    
def test_delete_category():
    db = MagicMock()
    category = Category(id=1, name="Delete me")
    db.query().filter().first.return_value = category

    delete_category(1, db)

    db.delete.assert_called_once_with(category)
    db.commit.assert_called_once()    

def test_delete_category_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as e:
        delete_category(1, db)

    assert e.value.status_code == 404     

def test_get_products_by_category_success():
    db = MagicMock()

    category = Category(id=1, name="Roses")
    db.query().filter().first.return_value = category

    products = [Product(id=1), Product(id=2)]

    db.query().options().filter().order_by().all.return_value = products

    result = get_products_by_category(1, db)

    assert result == products

def test_get_products_by_category_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as e:
        get_products_by_category(1, db)

    assert e.value.status_code == 404    