# Login controllers
from flask import Flask,request,jsonify
from flask_restful import Resource
from share.models import UserDB
from share.db import db
from main import JWTManager,create_access_token,get_jwt_identity,jwt_required
import json


class Login(Resource):

    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        name = str(data['name'])
        email = str(data['email'])
        password = str(data['password'])

        User = UserDB.query.filter(
                UserDB.name == name,
                UserDB.email == email,
                UserDB.password == password
                ).first()

        if User is None:
            return jsonify({"message": "Bad username or password"}), 401

        access_token = create_access_token(identity=name)
        return jsonify(access_token = access_token)

