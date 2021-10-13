from flask import Flask
from flask_restful import Api
from share.controllers import Dialogue, DialogueStart, Login, Signup
from share.db import db
from share.middleware.token import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///share/DB/dialogues_20210930.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

api = Api(app)

db.init_app(app)
with app.app_context():
    db.create_all()

jwt.init_app(app)
#jwt._set_error_handler_callbacks(api)

# router
api.add_resource(Dialogue, '/api/Dialogue')
api.add_resource(DialogueStart, '/api/Dialogue/start')
api.add_resource(Login, '/api/Login')
api.add_resource(Signup, '/api/Signup')
if __name__ == '__main__':
    app.run(debug=True)
