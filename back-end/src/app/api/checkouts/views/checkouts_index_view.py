from flask.views import MethodView
from flask import request, jsonify
from app.api.checkouts.services.checkouts_service import CheckoutsService


class CheckoutsIndexView(MethodView):
    init_every_request = False

    def __init__(self, service: CheckoutsService):
        self.service = service

    def post(self):
        item = self.service.create(**request.json)
        return jsonify(item.as_dict()), 201
