# Dialogue controllers

from flask import Flask, request, jsonify
from flask_restful import Resource
from share.db import db
from main import create_access_token, get_jwt_identity, jwt_required
import json

# models
from share.models import DialogueDB
from Dia_system import DialogueSystem


class DialogueStart(Resource):

    @jwt_required()
    def post(self):

        current_user = get_jwt_identity()
        dialogueNo = DialogueDB.preDialogueNo(
                db.session.query, current_user.name)
        dia = DialogueDB(current_user.name,
                         dialogueNo + 1, "SYS", "こんにちは", None)
        db.session.add(dia)
        db.session.commit()
        return jsonify({"message": "こんにちは"}), 200


class Dialogue(Resource):

    @jwt_requred()
    # 直近のすべてのデータを取得
    def get(self):
        #ログインしているユーザ
        current_user = get_jwt_identity()

        dialogueNo = DialogueDB.preDialogueNo(db.session.query, current_user.name)
        return jsonify(DialogueDB.to_dicts(db.session.query, current_user.name, dialogueNo))

    @jwt_requred()
    def post(self):
        # ログインしているユーザ
        current_user = get_jwt_identity()

        data = request.data.decode("utf-8")
        data = json.loads(data)
        dialogueNo = DialogueDB.preDialogueNo(db.session.query, current_user.name)
        dia = DialogueDB(current_user.name, dialogueNo, "USER", str(data["sentence"]), None)
        db.session.add(dia)

        # launch Dialogue system

        history = DialogueDB.query.filter(DialogueDB.userId == current_user.name).all()
        preUser = history[-2].sentence
        Sys = history[-1].sentence
        print(data["sentence"] + str(preUser) + str(Sys))
        output = DialogueSystem.main(str(data["sentence"]), preUser, Sys)

        dia = DialogueDB(current_user.name, dialogueNo, "SYSTEM", output, None)
        db.session.add(dia)
        db.session.commit()

        return jsonify(DialogueDB.to_dicts(db.session.query, current_user.name, dialogueNo)), 200
