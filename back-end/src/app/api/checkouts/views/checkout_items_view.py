from flask.views import MethodView
from flask import request, jsonify
from app.api.checkouts.services.checkout_items_service import CheckoutItemsService


class CheckoutItemsView(MethodView):
    init_every_request = False

    def __init__(self, service: CheckoutItemsService):
        self.service = service

    def put(self, id: int):
        item = self.service.update(
            item_id=id,
            **request.json,
        )
        return jsonify(item.checkout.as_dict()), 200
