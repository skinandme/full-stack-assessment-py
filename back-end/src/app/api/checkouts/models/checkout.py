from sqlalchemy import Column, Integer, String, ForeignKey, func, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.core.models.base_model import BaseModel
from app.api.checkouts.models.checkout_item import CheckoutItem


class Checkout(BaseModel):
    """Checkouts act like a shopping basket for a customer.

    A customer can add/remove items to their checkout before
    placing an order.
    """

    currency = Column(
        String(3),
        nullable=False,
        comment="Currency for the checkout. Format: ISO 4217 currency code",
    )

    discount_id = Column(
        ForeignKey("discount.id"),
        nullable=True,
        comment="A reference to the applied discount",
    )
    discount_code = Column(
        String(255),
        nullable=True,
        comment="The discount code that was applied",
    )
    discount_amount = Column(
        Integer,
        nullable=False,
        default=0,
        comment="The discount amount in the smallest currency unit (e.g. pence)",
    )

    items = relationship("CheckoutItem", back_populates="checkout")
    discount = relationship("Discount")

    @hybrid_property
    def sub_total(self):
        """Calculates the sub total for a checkout instance"""
        return sum([item.sub_total for item in self.items])

    @sub_total.expression
    def sub_total(cls):
        """SQL query for the checkout sub total calculation"""
        return (
            select(func.sum(CheckoutItem.sub_total))
            .where(CheckoutItem.checkout_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )

    @hybrid_property
    def total(self):
        """Calculates the total checkout value"""
        return self.sub_total - self.discount_amount

    def as_dict(self):
        return {
            "id": self.id,
            "currency": self.currency,
            "items": [item.as_dict() for item in self.items],
            "sub_total": self.sub_total,
            "total": self.total,
            "discount_code": self.discount_code,
            "discount_amount": self.discount_amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
