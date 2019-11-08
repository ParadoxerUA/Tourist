from database import db


trip_user_table = db.Table('trip-user',
    db.Column('trip_id', db.Integer, db.ForeignKey('trip.trip_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user_profile.user_id'), primary_key=True)
)


class Trip(db.Model):
    __tablename__ = 'trip'
    __table_args__ = {'extend_existing': True}
    trip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Open')
    admin_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), nullable=False)
    admin = db.relationship('apps.user_app.models.user_model.User', backref=db.backref('tripss', cascade='all, delete, delete-orphan'))
    points = db.relationship('apps.trip_app.models.point_model.Point', cascade='all, delete, delete-orphan')
    trip_uuid = db.Column(db.String(36), unique=True)
    users = db.relationship('User', secondary=trip_user_table, lazy=True,
        backref=db.backref('trips', lazy=True))

    @classmethod
    def create_trip(cls, data):
        trip = cls(**data)
        trip.users.append(trip.admin)
        db.session.add(trip)
        db.session.commit()
        return trip

    @classmethod
    def get_all_trips(cls):
        return cls.query.all()

    @classmethod
    def update_trip(cls, id, data):
        trip = cls.query.filter_by(trip_id=id).first()
        trip.update(**data)

    @classmethod
    def get_trip_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_trip_by_uuid(cls, trip_uuid):
        return cls.query.filter_by(trip_uuid=trip_uuid).first()

    def set_uuid(self, trip_uuid):
        self.trip_uuid = trip_uuid
        db.session.add(self)
        db.session.commit()
        return self.trip_uuid

    def join_user(self, user):
        self.users.append(user)
        db.session.add(self)
        db.session.commit()
        return user

    # tofix
    def get_fields(self, *args):
        public_data = {}
        for field in args:
            if field in ['users', 'admin']:
                try:
                    public_data[field] = [field.get_public_data() for field in getattr(self, field)]
                except:
                    public_data[field] = getattr(self, field).get_public_data()
            else:
                public_data[field] = getattr(self, field)
        return public_data

    def __repr__(self):
        return f'<Trip {self.name}>'