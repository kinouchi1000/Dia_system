# Dialogue controllers

from flask import Flask, request, jsonify
from flask_restful import Resource
from share.db import db
import json

#models
from share.models import DialogueDB
from Dia_system import DialogueSystem

class DialogueStart(Resource):
    def post(self, user_id):
        dialogueNo = DialogueDB.preDialogueNo(db.session.query, user_id)
        dia = DialogueDB(user_id, dialogueNo + 1, "SYS", "こんにちは", None)
        db.session.add(dia)
        db.session.commit()
        return {"message": "こんにちは"}


class Dialogue(Resource):

    # 直近のすべてのデータを取得
    def get(self, user_id):
        dialogueNo = DialogueDB.preDialogueNo(db.session.query, user_id)
        return jsonify(DialogueDB.to_dicts(db.session.query, user_id, dialogueNo))

    def post(self, user_id):
        data = request.data.decode("utf-8")
        data = json.loads(data)
        dialogueNo = DialogueDB.preDialogueNo(db.session.query, user_id)
        dia = DialogueDB(user_id, dialogueNo, "USER", str(data["sentence"]), None)
        db.session.add(dia)

        # launch Dialogue system

        history = DialogueDB.query.filter(DialogueDB.userId == user_id).all()
        preUser = history[-2].sentence
        Sys = history[-1].sentence
        print(data["sentence"] + str(preUser) + str(Sys))
        output = DialogueSystem.main(str(data["sentence"]), preUser, Sys)

        dia = DialogueDB(user_id, dialogueNo, "SYSTEM", output, None)
        db.session.add(dia)
        db.session.commit()

        return jsonify(DialogueDB.to_dicts(db.session.query, user_id, dialogueNo))
