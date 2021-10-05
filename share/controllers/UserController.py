# User controllers
from flask import Flask,request,jsonify
from flask_restful import Resource
from share.models import UserDB
from share.db import db
import json


class User(Resource):

    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        usrName = str(data['name'])
        usr = None
        if(UserDB.exist_name(db.session.query, usrName)):
            usr = UserDB.query.filter(UserDB.name == usrName).first()
        else:
            usr = UserDB(str(data['name']))
            db.session.add(usr)
            db.session.commit()

        return jsonify({'data': usr.to_dict()})
