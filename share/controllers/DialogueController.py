# Dialogue controllers

from flask import Flask, request, jsonify
from flask_restful import Resource
from share.db import db
from share.middleware.token import create_access_token, get_jwt_identity, jwt_required
import json

# models
from share.models import DialogueDB
from Dia_system import DialogueSystem


class Dialogue(Resource):

    @jwt_required()
    # 直近のすべてのデータを取得
    def get(self):
        # ログインしているユーザ
        current_user = get_jwt_identity()

        dialogueNo = DialogueDB.preDialogueNo(db.session.query, current_user)
        return jsonify(DialogueDB.to_dicts(db.session.query, current_user, dialogueNo))

    @jwt_required()
    def post(self):
        # ログインしているユーザ
        current_user = get_jwt_identity()

        data = request.data.decode("utf-8")
        data = json.loads(data)
        dialogueNo = DialogueDB.preDialogueNo(db.session.query, current_user)
        dia = DialogueDB(current_user, dialogueNo, "USER", str(data["sentence"]), None)
        db.session.add(dia)

        # launch Dialogue system

        history = DialogueDB.query.filter(DialogueDB.userId == current_user).all()
        preUser = history[-2].sentence
        Sys = history[-1].sentence
        print(data["sentence"] + str(preUser) + str(Sys))
        output = DialogueSystem.main(str(data["sentence"]), preUser, Sys)

        dia = DialogueDB(current_user, dialogueNo, "SYSTEM", output, None)
        db.session.add(dia)
        db.session.commit()

        return DialogueDB.to_dicts(db.session.query, current_user, dialogueNo), 200
