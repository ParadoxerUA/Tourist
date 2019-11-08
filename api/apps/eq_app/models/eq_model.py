from database import db


class Eq(db.Model):
    """Model for equipment"""

    __tablename__ = 'eq'
    __table_args__ = {'extend_existing': True}

    eq_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), nullable=False)

    @classmethod
    def create_eq(cls, data):
        """Create new equipment in the item list"""

        eq = cls(**data)
        db.session.add(eq)
        db.session.commit()
        return eq

    @classmethod
    def get_eq_by_id(cls, id):
        """Return the equipment by id"""

        return cls.query.filter_by(eq_id=id).first()

    @classmethod
    def update_eq(cls, id, updated_data):
        """Update equipment data in the list of items"""

        eq = cls.get_eq_by_id(id)
        eq.name = updated_data['name']
        eq.weight = updated_data['weight']
        eq.quantity = updated_data['quantity']
        db.session.commit()

    @classmethod
    def delete_eq(cls, id):
        """Delete equipment from the list of items"""

        eq = cls.get_eq_by_id(id)
        db.session.delete(eq)
        db.session.commit()
        return eq

    def __repr__(self):
        return f'Equipment: {self.name}'
