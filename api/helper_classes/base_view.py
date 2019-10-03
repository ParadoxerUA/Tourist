from flask.views import MethodView
from flask import jsonify
from datetime import datetime


class BaseView(MethodView):
    def _get_response(self, data):
        response = {
            'status': 200,
            'data': self._serialize(data),
            'date': datetime.now().__str__(),
        }
        
        return jsonify(response)

    def _serialize(self, data): 
        if isinstance(data, list): 
            return [self._serialize(item) for item in data] 
        elif isinstance(data, dict): 
            return data 
        else: 
            return data.__dict__      
