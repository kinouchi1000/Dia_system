# DialogueStart controllers

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
                     dialogueNo  1, "SYS", "こんにちは", None)
    db.session.add(dia)
    db.session.commit()
    return jsonify({"message": "こんにちは"}), 200
