from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from share.db import db

# models
from share.models import UserDB

# JWT認証処理の組み込み
# 認証
def authenticate(name, email, password):
    user = UserDB.query.filter(DialogueDB.userId == name
