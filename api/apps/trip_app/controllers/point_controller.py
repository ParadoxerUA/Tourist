from ..models import Point


class PointController:

    @staticmethod
    def create_point(data):
        point = Point.create_point(data)
        return point.id
