from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Ope_sqlit:
    def get_ex_name(self):
        data = User.query.with_entities(User.username)
        return [_[0] for _ in data]