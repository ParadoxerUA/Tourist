from database import db


class Equipment(db.Model):
    """Model for equipment"""

    __tablename__ = 'equipment'
    __table_args__ = {'extend_existing': True}

    equipment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'),
        nullable=True)
    owner = db.relationship('User', backref='personal_stuff')

    @classmethod
    def create_equipment(cls, data):
        """Create new equipment in the item list"""

        equipment = cls(**data)
        db.session.add(equipment)
        db.session.commit()
        return equipment

    @classmethod
    def get_equipment_by_id(cls, id):
        """Return the equipment by id"""

        return cls.query.filter_by(equipment_id=id).first()

    @classmethod
    def update_equipment(cls, id, updated_data):
        """Update equipment data in the list of items"""

        equipment = cls.get_equipment_by_id(id)
        equipment.name = updated_data['name']
        equipment.weight = updated_data['weight']
        equipment.quantity = updated_data['quantity']
        db.session.commit()

    @classmethod
    def delete_equipment(cls, id):
        """Delete equipment from the list of items"""

        equipment = cls.get_equipment_by_id(id)
        db.session.delete(equipment)
        db.session.commit()

    def get_public_data(self):
        if not self.owner_id:
            return self

    def __repr__(self):
        return f'Equipment: {self.name}'
