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
    admin = db.relationship('apps.user_app.models.user_model.User', cascade='save-update, merge, delete')
    points = db.relationship('apps.trip_app.models.point_model.Point', cascade='save-update, merge, delete')

    @classmethod
    def create_trip(cls, data):
        trip = cls(**data)
        db.session.add(trip)
        db.session.commit()
        return trip
    
    @classmethod
    def get_all_trips(cls):
        return cls.query.all()
    
    @classmethod
    def get_trip_by_id(cls, id):
        return cls.query.filter_by(trip_id=id).first()

    @classmethod
    def update_trip(cls, id, data):
        trip = cls.get_trip_by_id(id)
        trip.update(**data)

    def __repr__(self):
        return f'<Trip {self.name}>'