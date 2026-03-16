import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from flask.testing import FlaskClient
from app.api.checkouts.models.checkout import Checkout
from app.api.checkouts.models.checkout_item import CheckoutItem
from app.api.products.models.product import Product
from app.api.discounts.models.discount import Discount


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


@pytest.fixture
def percentage_discount() -> Discount:
    return Discount(
        code="WELCOME10",
        discount_type="percentage",
        amount=10,
        usage_limit=100,
        times_used=0,
        active=True,
        expires_at=datetime(2030, 12, 31, 23, 59, 59),
    )


@pytest.fixture
def fixed_discount() -> Discount:
    return Discount(
        code="FLAT500",
        discount_type="fixed",
        amount=500,
        usage_limit=50,
        times_used=0,
        active=True,
    )


def test_apply_valid_percentage_discount(
    client: FlaskClient,
    session: Session,
    checkout: Checkout,
    product: Product,
    percentage_discount: Discount,
):
    session.add(product)
    session.add(checkout)
    session.add(percentage_discount)
    checkout_item = CheckoutItem(product=product, checkout=checkout, quantity=2)
    session.add(checkout_item)
    session.commit()

    res = client.post(
        f"/checkouts/{checkout.id}/discount",
        json={"code": "WELCOME10"},
    )

    assert res.status_code == 200
    assert res.json["discount_code"] == "WELCOME10"
    assert res.json["discount_amount"] > 0


def test_apply_invalid_discount_code_returns_404(
    client: FlaskClient,
    session: Session,
    checkout: Checkout,
    product: Product,
):
    session.add(product)
    session.add(checkout)
    checkout_item = CheckoutItem(product=product, checkout=checkout, quantity=1)
    session.add(checkout_item)
    session.commit()

    res = client.post(
        f"/checkouts/{checkout.id}/discount",
        json={"code": "DOESNOTEXIST"},
    )

    assert res.status_code == 404
    assert "not found" in res.json["error"]["message"].lower()


def test_apply_valid_fixed_discount(
    client: FlaskClient,
    session: Session,
    checkout: Checkout,
    product: Product,
    fixed_discount: Discount,
):
    session.add(product)
    session.add(checkout)
    session.add(fixed_discount)
    checkout_item = CheckoutItem(product=product, checkout=checkout, quantity=2)
    session.add(checkout_item)
    session.commit()

    res = client.post(
        f"/checkouts/{checkout.id}/discount",
        json={"code": "FLAT500"},
    )

    assert res.status_code == 200
    assert res.json["discount_code"] == "FLAT500"
    assert res.json["discount_amount"] == 500


def test_apply_discount_to_nonexistent_checkout(client: FlaskClient):
    res = client.post(
        "/checkouts/999999/discount",
        json={"code": "WELCOME10"},
    )

    assert res.status_code == 404
