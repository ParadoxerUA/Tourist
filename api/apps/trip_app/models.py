from database import db


class Trip(db.Model):
    __tablename__ = 'trip'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    id_admin = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    trip = db.relationship("UserProfile", foreign_keys=[id_admin])

    @classmethod
    def create_trip(cls, data):
        trip = cls(**data)
        db.session.add(trip)
        db.session.commit()
        return trip

    def __repr__(self):
        return f'<Trip {self.name}>'


class Point(db.Model):
    __tablename__ = 'point'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    id_trip = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    trip = db.relationship("Trip", foreign_keys=[id_trip])

    @classmethod
    def create_point(cls, data):
        point = cls(**data)
        db.session.add(point)
        db.session.commit()
        return point


    def __repr__(self):
        return f'<Trip lat: {self.latitude} long {self.longitude}>'
