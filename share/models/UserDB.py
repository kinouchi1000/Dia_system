# dialogue models __init__
from share.db import db


class UserDB(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='', nullable=False)

    def __init__(self, name=None):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @classmethod
    def to_dicts(cls, query, usrId):
        dicts = cls.to_dict(query(cls).filter(cls.id == usrId).first())
        return {'data': [dicts]}

    @classmethod
    def exist_name(cls, query, name):
        user = query(cls).filter(cls.name == name).first()
        if(user is None):
            return False
        else:
            return True

    def __repr__(self):
        return u'<User id={self.id}>'.format(self=self)
