import pytest
from sqlalchemy.orm import Session
from flask.testing import FlaskClient
from app.api.checkouts.models.checkout import Checkout
from app.api.products.models.product import Product
from app.api.checkouts.models.checkout_item import CheckoutItem


@pytest.fixture
def product() -> Product:
    return Product(
        sku="NIACINAMIDE_NIGHT_CREAM",
        name="Niacinamide-powered night cream",
        unit_price=2000,
        currency="GBP",
    )


@pytest.fixture
def checkout() -> Checkout:
    return Checkout(currency="GBP")


def test_get_or_404_checkout(client: FlaskClient):
    # Act
    res = client.get("/checkouts/100000")

    # Assert
    assert res.status_code == 404
    assert res.json["error"]["message"] == "Checkout not found"


def test_get_empty_checkout(client: FlaskClient, session: Session, checkout: Checkout):
    # Arrange
    session.add(checkout)
    session.commit()

    # Act
    res = client.get(f"/checkouts/{checkout.id}")

    # Assert
    assert res.status_code == 200
    assert res.json["id"] is not None
    assert res.json["currency"] == "GBP"
    assert res.json["items"] == []
    assert res.json["sub_total"] == 0


def test_get_checkout_with_items(
    client: FlaskClient, session: Session, product: Product, checkout: Checkout
):
    # Arrange
    session.add(product)
    session.add(checkout)
    checkout_item = CheckoutItem(product=product, checkout=checkout, quantity=2)
    session.add(checkout_item)
    session.commit()

    # Act
    res = client.get(f"/checkouts/{checkout.id}")

    # Assert
    assert res.status_code == 200
    assert res.json["id"] is not None
    assert res.json["currency"] == "GBP"
    assert res.json["sub_total"] == 4000
    assert res.json["total"] == 4000
    assert len(res.json["items"]) == 1
    assert res.json["items"][0]["quantity"] == 2
    assert res.json["items"][0]["sub_total"] == 4000
    assert res.json["items"][0]["product"]["id"] == product.id
    assert res.json["items"][0]["product"]["name"] == "Niacinamide-powered night cream"
    assert res.json["items"][0]["product"]["sku"] == "NIACINAMIDE_NIGHT_CREAM"
    assert res.json["items"][0]["product"]["unit_price"] == 2000
    assert res.json["items"][0]["product"]["currency"] == "GBP"


def test_create_checkout(client: FlaskClient):
    # Act
    res = client.post("/checkouts", json={"currency": "GBP"})

    # Assert
    assert res.status_code == 201
    assert res.json["id"] is not None
    assert res.json["currency"] == "GBP"
    assert res.json["items"] == []
    assert res.json["sub_total"] == 0
    assert res.json["total"] == 0
