from datetime import datetime, UTC
from sqlalchemy.orm import Session
from app.api.checkouts.models.checkout import Checkout
from app.api.discounts.models.discount import Discount
from app.core.errors import NotFoundError, ValidationError


class DiscountsService:
    def __init__(self, session: Session):
        self.session = session

    def validate_and_apply(self, checkout_id: int, code: str) -> Checkout:
        """Validate a discount code and apply it to a checkout.

        Checks that the code exists and is active, has not expired,
        has not exceeded its usage limit, and meets the minimum order value.
        If the checkout already has a discount applied, the old discount
        is removed first and its usage count is decremented.
        """
        checkout = self.session.get(Checkout, checkout_id)
        if checkout is None:
            raise NotFoundError("Checkout not found")

        # If a discount is already applied, remove it first
        if checkout.discount_id is not None:
            old_discount = self.session.get(Discount, checkout.discount_id)
            if old_discount is not None:
                old_discount.times_used = max(0, old_discount.times_used - 1)
                self.session.add(old_discount)

        discount = (
            self.session.query(Discount)
            .filter_by(code=code, active=True)
            .first()
        )

        if discount is None:
            raise NotFoundError("Discount code not found or inactive")

        # Check expiry
        if discount.expires_at is not None and discount.expires_at < datetime.now(UTC).replace(tzinfo=None):
            raise ValidationError("Discount code has expired")

        # Check usage limit
        if discount.usage_limit is not None and discount.times_used >= discount.usage_limit:
            raise ValidationError("Discount code usage limit reached")

        # Check minimum order value
        if discount.min_order_value is not None and checkout.sub_total < discount.min_order_value:
            raise ValidationError(
                f"Order subtotal must be at least {discount.min_order_value} to use this discount"
            )

        # Calculate discount amount
        if discount.discount_type == "percentage":
            discount_amount = checkout.sub_total * discount.amount // 100
        else:
            discount_amount = discount.amount

        # Apply discount to checkout
        checkout.discount_id = discount.id
        checkout.discount_code = discount.code
        checkout.discount_amount = discount_amount

        # Increment usage count
        discount.times_used += 1

        self.session.add(checkout)
        self.session.add(discount)
        self.session.commit()

        return checkout

