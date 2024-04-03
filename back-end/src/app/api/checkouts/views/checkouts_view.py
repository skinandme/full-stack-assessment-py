from flask.views import MethodView
from flask import abort, jsonify
from app.api.checkouts.services.checkouts_service import CheckoutsService
from app.core.errors import NotFoundError


class CheckoutsView(MethodView):
    init_every_request = False

    def __init__(self, service: CheckoutsService):
        self.service = service

    def get(self, id: int):
        try:
            item = self.service.get_or_raise(id)
            return jsonify(item.as_dict())
        except NotFoundError as e:
            return jsonify({"error": {"message": str(e)}}), 404
