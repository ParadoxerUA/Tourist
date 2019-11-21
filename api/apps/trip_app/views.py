from helper_classes.base_view import BaseView
from flask import current_app, request, g
from .schemas.trip_schema import TripSchema
from marshmallow import ValidationError
from helper_classes.auth_decorator import login_required


class TripsView(BaseView):
    def __init__(self):
        self.trip_controller = current_app.blueprints['trip'].controllers.TripController

    @login_required
    def post(self):
        try:
            trip_data = TripSchema().load(request.json)
            data = self.trip_controller.create_trip(trip_data, g.user_id)
            # data = current_app.blueprints['trip'].controllers.TripController.create_trip(trip_data, g.user_id)
            return self._get_response(data, status_code=201)
        except (ValidationError, Exception) as err:
            data = [str(err)]
            return self._get_response(data, status_code=400)

    @login_required
    def get(self):
        trips_list = current_app.blueprints['trip'].controllers.\
            TripController.get_trips_details(g.user_id)
        return self._get_response(trips_list, status_code=200)


class SingleTripView(BaseView):
    def __init__(self):
        self.trip_controller = current_app.blueprints['trip'].controllers.TripController

    @login_required
    def put(self, trip_id):
        trip_data = request.json
        start_date = trip_data['start_date']
        end_date = trip_data['end_date']
        status = trip_data['status']
        current_app.blueprints['trip'].controllers.\
            TripController.update_trip_list_data(trip_id, start_date, end_date, status)
        return self._get_response('trip updated', status_code=200)


    @login_required
    def patch(self, trip_id):
        new_uuid = self.trip_controller.refresh_trip_uuid(trip_id, g.user_id )
        if new_uuid:
            return self._get_response(new_uuid, status_code=200)
        else:
            return self._get_response('You are not admin of given trip', status_code=400)

    @login_required
    def delete(self, trip_id):
        user_to_delete = request.args.get('user_id')
        if not user_to_delete:
            user_to_delete = g.user_id
        result = self.trip_controller.delete_user_from_trip(trip_id, user_to_delete)
        if result:
            return self._get_response(result, status_code=200)
        else:
            return self._get_response('User delete failed', status_code=400)

    @login_required
    def get(self, trip_id):
        fields = request.args.get('fields')
        if fields:
            fields = fields.split(',')
        trip_data = self.trip_controller.get_trip_data(trip_id, g.user_id, fields)
        if trip_data:
            return self._get_response(trip_data, status_code=200)
        else:
            return self._get_response('User not assign to requested trip', status_code=400)
