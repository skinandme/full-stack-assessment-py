import pytest
from sqlalchemy.orm import Session
from flask.testing import FlaskClient
from app.api.checkouts.models.checkout import Checkout
from app.api.checkouts.models.checkout_item import CheckoutItem
from app.api.products.models.product import Product


@pytest.fixture
def checkout() -> Checkout:
    return Checkout(currency="GBP")


@pytest.fixture()
def product() -> Product:
    return Product(
        sku="NIACINAMIDE_NIGHT_CREAM",
        name="Niacinamide-powered night cream",
        unit_price=2000,
        currency="GBP",
    )


def test_create_checkout_item(
    client: FlaskClient, session: Session, checkout: Checkout, product: Product
):
    session.add(checkout)
    session.add(product)
    session.commit()

    res = client.post(
        "/checkout_items",
        json={"checkout_id": checkout.id, "product_id": product.id, "quantity": 1},
    )

    assert res.status_code == 201
    assert res.json["items"][0]["product"]["sku"] == "NIACINAMIDE_NIGHT_CREAM"


def test_missing_checkout_raises_404(
    client: FlaskClient, session: Session, product: Product
):
    session.add(product)
    session.commit()

    res = client.post(
        "/checkout_items",
        json={"checkout_id": 88888, "product_id": product.id, "quantity": 2},
    )
    assert res.status_code == 404
    assert res.json["error"]["message"] == "Checkout not found"


def test_missing_product_raises_404(
    client: FlaskClient, session: Session, checkout: Checkout
):
    session.add(checkout)
    session.commit()

    res = client.post(
        "/checkout_items",
        json={"checkout_id": checkout.id, "product_id": 88888, "quantity": 2},
    )

    assert res.status_code == 404
    assert res.json["error"]["message"] == "Product not found"


def test_update_checkout_item(
    client: FlaskClient, checkout: Checkout, product: Product, session: Session
):
    checkout_item = CheckoutItem(
        checkout=checkout,
        product=product,
        quantity=2,
    )

    session.add(checkout)
    session.add(product)
    session.add(checkout_item)
    session.commit()

    res = client.put(f"/checkout_items/{checkout_item.id}", json={"quantity": 9})

    assert res.status_code == 200
    assert res.json["items"][0]["product"]["sku"] == "NIACINAMIDE_NIGHT_CREAM"
    assert res.json["items"][0]["quantity"] == 9
    assert res.json["items"][0]["sub_total"] == 18000
