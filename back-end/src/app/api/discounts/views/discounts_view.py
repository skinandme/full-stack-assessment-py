from flask import request, jsonify
from flask.views import MethodView
from app.api.discounts.services.discounts_service import DiscountsService
from app.core.errors import NotFoundError, ValidationError


class DiscountsView(MethodView):
    init_every_request = False

    def __init__(self, service: DiscountsService):
        self.service = service

    def post(self, checkout_id: int):
        """Apply a discount code to a checkout."""
        try:
            code = request.json.get("code")
            if not code:
                return jsonify({"error": {"message": "Discount code is required"}}), 400

            checkout = self.service.validate_and_apply(
                checkout_id=checkout_id,
                code=code,
            )
            return jsonify(checkout.as_dict()), 200

        except NotFoundError as e:
            return jsonify({"error": {"message": str(e)}}), 404
        except ValidationError as e:
            return jsonify({"error": {"message": str(e)}}), 422

    def delete(self, checkout_id: int):
        """Remove a discount from a checkout."""
        # TODO: implement remove discount endpoint
        return jsonify({"error": {"message": "Not implemented"}}), 501
