from apps.eq_app.models import Eq
from flask import current_app


class EqController:

    @classmethod
    def get_eq_data(cls, eq_id):
        eq_data = Eq.get_eq_by_id(eq_id)
        return eq_data

    @classmethod
    def update_eq(cls, eq_id, data):
        new_eq = Eq.update_eq(eq_id, data)
        return new_eq

    @classmethod
    def delete_eq(cls, eq_id):
        eq_data = Eq.delete_eq(eq_id)
        return eq_data

    @classmethod
    def create_eq(cls, data):
        data = Eq.create_eq(data)
        return data
