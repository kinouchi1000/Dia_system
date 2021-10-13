# dialogue models __init__
from share.db import db


class UserDB(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='', nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column('password', db.String(256), default='', nullable=False)

    def __init__(self, name,email,password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    # @classmethod
    # def to_dicts(cls, query, usrId):
    #    dicts = cls.to_dict(query(cls).filter(cls.id == usrId).first())
    #    return {'data': [dicts]}

    @classmethod
    def exist_user(cls, query, name, email):
        user = query(cls).filter(
                cls.name == name,
                cls.email == email
                ).first()

        if(user is None):
            return False
        else:
            return True

    def __repr__(self):
        return u'<User id={self.id}>'.format(self=self)
