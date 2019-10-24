from database import db


class Trip(db.Model):
    __tablename__ = 'trip'
    __table_args__ = {'extend_existing': True}
    trip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'))
    points = db.relationship('api.apps.trip_app.models.Point')

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
    point_id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'))

    @classmethod
    def create_point(cls, data):
        point = cls(**data)
        db.session.add(point)
        db.session.commit()
        return point

    def __repr__(self):
        return f'<Trip lat: {self.latitude} long: {self.longitude}>'
