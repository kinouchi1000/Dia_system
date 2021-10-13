# Signup controllers
from flask import Flask, request, jsonify
from flask_restful import Resource
from share.models import UserDB
from share.db import db
import json


class Signup(Resource):

    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        name = str(data['name'])
        email = str(data['email'])
        password = str(data['password'])

        # search User from name and email
        if(UserDB.exist_user(db.session.query, name, email)):
            return jsonify({"message" : "Aleady Exist User"})

        # create User
        usr = UserDB(name,email,password)
        db.session.add(usr)
        db.session.commit()

        return jsonify({'message': "Created User successfly!!"})↲
