from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.core.models.base_model import BaseModel


class CheckoutItem(BaseModel):
    """CheckoutItems record the quantity of a product ordered within a checkout"""

    checkout_id = Column(
        ForeignKey("checkout.id"),
        comment="A reference to the checkout containing the checkout item",
    )
    product_id = Column(
        ForeignKey("product.id"), comment="A reference to the product being ordered"
    )
    quantity = Column(
        Integer, nullable=False, comment="The quantity of the product in this checkout"
    )

    product = relationship("Product")
    checkout = relationship("Checkout", back_populates="items")

    @hybrid_property
    def sub_total(self):
        """Calculates the sub total for a checkout item"""
        return self.quantity * self.product.unit_price

    @sub_total.expression
    def sub_total(cls):
        """SQL query for the checkout item sub total calculation"""
        return cls.quantity * cls.product.unit_price

    def as_dict(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "sub_total": self.sub_total,
            "product": self.product.as_dict(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
