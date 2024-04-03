from sqlalchemy.orm import Session
from app.api.checkouts.models.checkout import Checkout
from app.core.errors import NotFoundError


class CheckoutsService:
    def __init__(self, session: Session):
        self.session = session

    def get(self, checkout_id: int) -> Checkout | None:
        return self.session.query(Checkout).get(checkout_id)

    def get_or_raise(self, checkout_id: int) -> Checkout:
        rv = self.get(checkout_id)
        if rv is None:
            raise NotFoundError("Checkout not found")
        return rv

    def create(self, currency: str) -> Checkout:
        checkout = Checkout(currency=currency)
        self.session.add(checkout)
        self.session.commit()
        return checkout
