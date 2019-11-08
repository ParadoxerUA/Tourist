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
    status = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), nullable=False)
    # Need tofix CASCADE parametr
    admin = db.relationship('apps.user_app.models.user_model.User', cascade='save-update, merge, delete')
    points = db.relationship('apps.trip_app.models.point_model.Point', cascade='save-update, merge, delete')
    trip_uuid = db.Column(db.String(36), unique=True)
    users = db.relationship('User', secondary=trip_user_table, lazy=True,
        backref=db.backref('trips', lazy=True))
    eq = db.relationship('apps.eq_app.models.eq_model.Eq',
                         backref=db.backref('trip'),
                         cascade='all, delete, delete-orphan',
                         single_parent=True)

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
