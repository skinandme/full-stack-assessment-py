from flask import request, jsonify, abort
from flask.views import MethodView
from app.api.checkouts.services.checkout_items_service import CheckoutItemsService
from app.core.errors import NotFoundError


class CheckoutItemsIndexView(MethodView):
    init_every_request = False

    def __init__(self, service: CheckoutItemsService):
        self.service = service

    def post(self):
        try:
            item = self.service.create(**request.json)
            return jsonify(item.checkout.as_dict()), 201
        except NotFoundError as e:
            return jsonify({"error": {"message": str(e)}}), 404
