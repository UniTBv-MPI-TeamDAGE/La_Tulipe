from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.category import Category
from app.models.product import Product, ProductSeason, ProductType
from app.services.product_service import (
    _resolve_color_stock_pairs,
    _validate_color_stock_total,
    create_product,
    delete_product,
    get_product_or_404,
    update_product_stock,
)


def test_resolve_color_stock_duplicate():
    with pytest.raises(HTTPException) as e:
        _resolve_color_stock_pairs(color_stocks=[(1, 5), (1, 3)])
    assert e.value.status_code == 400


def test_resolve_color_stock_negative():
    with pytest.raises(HTTPException):
        _resolve_color_stock_pairs(color_stocks=[(1, -1)])


def test_resolve_color_stock_success():
    result = _resolve_color_stock_pairs(color_stocks=[(1, 5), (2, 3)])
    assert result == [(1, 5), (2, 3)]


def test_validate_color_stock_exceeds_total():
    with pytest.raises(HTTPException):
        _validate_color_stock_total(
            total_stock=5,
            color_stock_pairs=[(1, 3), (2, 4)]
        )


def test_validate_color_stock_ok():
    _validate_color_stock_total(
        total_stock=10,
        color_stock_pairs=[(1, 3), (2, 4)]
    )    

def test_get_product_not_found():
    db = MagicMock()

    query = MagicMock()
    query.options.return_value = query
    query.filter.return_value = query
    query.first.return_value = None

    db.query.return_value = query

    with pytest.raises(HTTPException):
        get_product_or_404(1, db)


def test_get_product_success():
    db = MagicMock()

    product = Product(id=1)

    query = MagicMock()
    query.options.return_value = query
    query.filter.return_value = query
    query.first.return_value = product

    db.query.return_value = query

    result = get_product_or_404(1, db)

    assert result == product

def test_create_product_category_not_found():
    db = MagicMock()

    query = MagicMock()
    query.filter.return_value = query
    query.first.return_value = None

    db.query.return_value = query

    with pytest.raises(HTTPException):
        create_product(
            name="Rose",
            description="desc",
            price=10,
            stock=5,
            image_url=None,
            is_featured=False,
            season=ProductSeason.ALL_SEASON,
            product_type=ProductType.INDIVIDUAL,
            color_stocks=[],
            category_id=1,
            db=db
        )


def test_create_product_success():
    db = MagicMock()

    category = Category(id=1)

    category_query = MagicMock()
    category_query.filter.return_value = category_query
    category_query.first.return_value = category

    product = Product(id=1)

    product_query = MagicMock()
    product_query.options.return_value = product_query
    product_query.filter.return_value = product_query
    product_query.first.return_value = product

    def query_side_effect(model):
        if model == Category:
            return category_query
        return product_query

    db.query.side_effect = query_side_effect

    result = create_product(
        name="Rose",
        description="desc",
        price=10,
        stock=5,
        image_url=None,
        is_featured=False,
        season=ProductSeason.ALL_SEASON,
        product_type=ProductType.INDIVIDUAL,
        color_stocks=[],
        category_id=1,
        db=db
    )

    assert result == product
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_update_product_stock_negative():
    db = MagicMock()

    with pytest.raises(HTTPException):
        update_product_stock(product_id=1, stock=-1, db=db)


def test_update_product_stock_not_found():
    db = MagicMock()

    query = MagicMock()
    query.filter.return_value = query
    query.first.return_value = None

    db.query.return_value = query

    with pytest.raises(HTTPException):
        update_product_stock(product_id=1, stock=5, db=db)


def test_update_product_stock_success():
    db = MagicMock()

    product = Product(id=1, stock=5)

    query = MagicMock()
    query.options.return_value = query
    query.filter.return_value = query
    query.first.return_value = product

    db.query.return_value = query

    result = update_product_stock(product_id=1, stock=10, db=db)

    assert result.stock == 10
    db.commit.assert_called_once()


def test_delete_product_not_found():
    db = MagicMock()

    query = MagicMock()
    query.filter.return_value = query
    query.first.return_value = None

    db.query.return_value = query

    with pytest.raises(HTTPException):
        delete_product(1, db)


def test_delete_product_success():
    db = MagicMock()

    product = Product(id=1)

    query = MagicMock()
    query.filter.return_value = query
    query.first.return_value = product

    db.query.return_value = query

    delete_product(1, db)

    db.delete.assert_called_once_with(product)
    db.commit.assert_called_once()