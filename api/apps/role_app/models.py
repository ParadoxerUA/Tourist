from database import db

class Role(db.Model):

    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role: {self.name}>'

    @classmethod
    def new_role(cls, name):
        role = cls(name=name)
        db.session.add(role)
        db.session.commit()
        return role

    @classmethod
    def delete_role(cls, name):
        role = cls.query.filter_by(name=name).first()
        db.session.delete(role)
        db.session.commit()
        return role
