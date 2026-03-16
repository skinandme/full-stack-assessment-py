from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.models.base_model import BaseModel


class Discount(BaseModel):
    """Discounts represent promotional codes that can be applied to checkouts.

    Supports both percentage-based and fixed-amount discount types.
    """

    code = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        comment="The unique discount code customers enter to apply the discount",
    )
    discount_type = Column(
        String(20),
        nullable=False,
        comment="The type of discount: 'percentage' or 'fixed'",
    )
    amount = Column(
        Integer,
        nullable=False,
        comment="The discount value. For 'percentage': the percentage (e.g. 10 for 10%%). "
        "For 'fixed': the amount in smallest currency unit (e.g. 500 for £5.00)",
    )
    usage_limit = Column(
        Integer,
        nullable=True,
        comment="Maximum number of times this code can be used. NULL means unlimited.",
    )
    times_used = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of times this discount code has been used",
    )
    min_order_value = Column(
        Integer,
        nullable=True,
        comment="Minimum order subtotal (in smallest currency unit) required to use this discount",
    )
    active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Whether this discount code is currently active",
    )
    expires_at = Column(
        DateTime,
        nullable=True,
        comment="When this discount code expires. NULL means no expiry.",
    )

    def as_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "discount_type": self.discount_type,
            "amount": self.amount,
            "usage_limit": self.usage_limit,
            "times_used": self.times_used,
            "min_order_value": self.min_order_value,
            "active": self.active,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
