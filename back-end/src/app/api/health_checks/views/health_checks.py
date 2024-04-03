from flask.views import MethodView
from flask import jsonify


class HealthChecksView(MethodView):

    def get(self):
        return jsonify({"status": "OK"}), 200
