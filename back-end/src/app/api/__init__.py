from sqlalchemy.orm import Session
from flask import Blueprint
from app.api.health_checks.views import HealthChecksView

from app.api.checkouts.views import (
  CheckoutsIndexView,
  CheckoutsView,
  CheckoutItemsIndexView,
  CheckoutItemsView
)

from app.api.checkouts.services import (
  CheckoutsService,
  CheckoutItemsService
)

from app.api.discounts.views import DiscountsView
from app.api.discounts.services import DiscountsService

def create_api_blueprint(db_session: Session) -> Blueprint:
    bp = Blueprint('api', __name__)

    checkouts_service = CheckoutsService(session=db_session)
    checkout_items_service = CheckoutItemsService(session=db_session)
    discounts_service = DiscountsService(session=db_session)

    bp.add_url_rule('/health_checks', view_func=HealthChecksView.as_view('health_checks'))
    bp.add_url_rule('/checkouts', view_func=CheckoutsIndexView.as_view(name='checkouts_index', service=checkouts_service))
    bp.add_url_rule('/checkouts/<int:id>', view_func=CheckoutsView.as_view(name='checkouts', service=checkouts_service))
    bp.add_url_rule('/checkout_items', view_func=CheckoutItemsIndexView.as_view(name='checkout_items_index', service=checkout_items_service))
    bp.add_url_rule('/checkout_items/<int:id>', view_func=CheckoutItemsView.as_view('checkout_items', service=checkout_items_service))
    bp.add_url_rule(
        '/checkouts/<int:checkout_id>/discount',
        view_func=DiscountsView.as_view('discounts', service=discounts_service),
    )

    return bp
