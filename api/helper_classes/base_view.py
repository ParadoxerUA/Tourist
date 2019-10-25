from flask.views import MethodView
from flask import jsonify, make_response
from datetime import datetime


class BaseView(MethodView):
    def _get_response(self, data, *, status_code=200):
        response = {
            'data': self._serialize(data),
            'date': datetime.now().__str__(),
        }
        
        return make_response(jsonify(response), status_code)

    def _serialize(self, data):
        if isinstance(data, list):
            return [self._serialize(item) for item in data]
        try:
            return data.__dict__
        except AttributeError:
            return data
