from flask import Flask
from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy
from share.controllers import User, Dialogue, DialogueStart
from share.db import db
# from Dia_system import Dia_system
# import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///share/DB/dialogues_20210930.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# router
api.add_resource(Dialogue, '/api/Dialogue/<int:user_id>')
api.add_resource(DialogueStart, '/api/Dialogue/<int:user_id>/start')
api.add_resource(User, '/api/User')

if __name__ == '__main__':
    app.run(debug=True)
