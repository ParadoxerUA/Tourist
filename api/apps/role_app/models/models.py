from database import db


class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'))

    def __repr__(self):
        return f'<Role: {self.name}>'

    @classmethod
    def create_role(cls, data):
        role = cls(**data)
        db.session.add(role)
        db.session.commit()
        return role

    @classmethod
    def delete_role(cls, name, trip_id):
        role = cls.query.filter_by(name=name, trip_id=trip_id).first()
        db.session.delete(role)
        db.session.commit()
        return role

    @classmethod
    def get_all_roles(cls):
        return cls.query.all()
