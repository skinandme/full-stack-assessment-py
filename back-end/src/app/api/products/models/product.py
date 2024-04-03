from sqlalchemy import Column, Integer, String
from app.core.models.base_model import BaseModel


class Product(BaseModel):
    sku = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="A unique business identifier for this product",
    )
    name = Column(String(255), nullable=False, comment="The product name")
    unit_price = Column(
        Integer,
        nullable=False,
        comment="The price of a single unit of this product as an integer e.g. £1.00 == 100",
    )
    currency = Column(
        String(3),
        nullable=False,
        default="GBP",
        comment="Currency the unit_price is defined in. Format: ISO 4217 currency code",
    )

    def as_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "unit_price": self.unit_price,
            "currency": self.currency,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
