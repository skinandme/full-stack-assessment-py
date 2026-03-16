from datetime import datetime
from app.api.discounts.models import Discount

data = [
    Discount(
        code="WELCOME10",
        discount_type="percentage",
        amount=10,
        usage_limit=100,
        times_used=0,
        active=True,
        expires_at=datetime(2030, 12, 31, 23, 59, 59),
    ),
    Discount(
        code="FLAT500",
        discount_type="fixed",
        amount=500,
        usage_limit=50,
        times_used=0,
        active=True,
        expires_at=None,
    ),
    Discount(
        code="EXPIRED2024",
        discount_type="percentage",
        amount=15,
        usage_limit=None,
        times_used=0,
        active=True,
        expires_at=datetime(2024, 1, 1, 0, 0, 0),
    ),
    Discount(
        code="MAXEDOUT",
        discount_type="fixed",
        amount=300,
        usage_limit=1,
        times_used=1,
        active=True,
        expires_at=None,
    ),
]
