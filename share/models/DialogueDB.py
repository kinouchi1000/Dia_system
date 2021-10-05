# dialogue models __init__
from share.db import db
import datetime


class DialogueDB(db.Model):
    __tablename__ = 'flask_table'

    dialogueId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=False, nullable=False)
    dialogueNo = db.Column(db.Integer, unique=False, nullable=False)
    speaker = db.Column(db.String(10), unique=False, nullable=False)
    sentence = db.Column(db.String(256), unique=False, nullable=True)
    evaluation = db.Column(db.Float, unique=False, nullable=True)
    insertDate = db.Column(db.DateTime, unique=False, nullable=False)

    def to_dict(self):
        return {
            'dialogueId': self.dialogueId,
            'userId': self.userId,
            'dialogueNo': self.dialogueNo,
            'speaker': self.speaker,
            'sentence': self.sentence,
            'evaluation': self.evaluation,
        }

    @classmethod
    def to_dicts(cls, query, user_id, dialogueNo):
        dicts = []
        cls_list = query(cls).filter(cls.userId == user_id, cls.dialogueNo == dialogueNo).all()
        for c in cls_list:
            dicts.append(cls.to_dict(c))
        return {
            'data': dicts
        }

    @classmethod
    def preDialogueNo(cls, query, user_id):
        data = query(cls).filter(cls.userId == user_id).all()
        if(len(data) > 0):
            print(data[-1].dialogueNo)
            return int(data[-1].dialogueNo)
        else:
            return 0

    def __init__(self, userId=None, dialogueNo=None, speaker=None, sentence=None, evaluation=None):
        self.userId = userId
        self.dialogueNo = dialogueNo
        self.speaker = speaker
        self.sentence = sentence
        self.evaluation = evaluation
        self.insertDate = datetime.datetime.now()

    def __repr__(self):
        return 'Dialogue %d' % self.dialogueId
