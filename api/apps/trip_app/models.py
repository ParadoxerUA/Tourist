from api.database import db

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.Boolean)
    id_admin = db.Column(db.Integer, db.ForeignKey('user_profile.id'))

    @classmethod
    def create_trip(cls, data):
        trip = cls(**data)
        db.session.add(trip)
        db.session.commit()

    def __repr__(self):
        return f'<Trip {self.name}>'



