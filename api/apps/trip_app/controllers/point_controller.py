from flask import current_app


class PointController:

    @staticmethod
    def create_point(data):
        point = current_app.models.Point.create_point(data)
        return point
