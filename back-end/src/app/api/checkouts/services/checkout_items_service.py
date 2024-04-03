from sqlalchemy.orm import Session
from app.api.checkouts.models.checkout import Checkout
from app.api.checkouts.models.checkout_item import CheckoutItem
from app.api.products.models.product import Product
from app.core.errors import NotFoundError


class CheckoutItemsService:
    def __init__(self, session: Session):
        self.session = session

    def get(self, checkout_item_id: int) -> CheckoutItem | None:
        return self.session.query(CheckoutItem).get(checkout_item_id)

    def get_or_raise(self, checkout_item_id: int):
        checkout_item = self.get(checkout_item_id)
        if checkout_item is None:
            raise NotFoundError("CheckoutItem not found")
        return checkout_item

    def create(
        self,
        checkout_id: int,
        product_id: int,
        quantity: int,
    ) -> CheckoutItem:
        checkout = self._get_checkout_or_raise(checkout_id)
        product = self._get_product_or_raise(product_id)
        checkout_item = CheckoutItem(
            checkout=checkout, product=product, quantity=quantity
        )
        self.session.add(checkout_item)
        self.session.commit()
        return checkout_item

    def update(self, item_id: int, quantity: int) -> CheckoutItem:
        checkout_item = self.get_or_raise(item_id)
        checkout_item.quantity = quantity
        self.session.add(checkout_item)
        self.session.commit()
        return checkout_item

    def _get_checkout_or_raise(self, checkout_id: int) -> Checkout | None:
        checkout = self.session.query(Checkout).get(checkout_id)
        if checkout is None:
            raise NotFoundError("Checkout not found")
        return checkout

    def _get_product_or_raise(self, product_id: int) -> Product:
        product = self.session.query(Product).get(product_id)
        if product is None:
            raise NotFoundError("Product not found")
        return product
