from datetime import datetime
from .. import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(250), unique = True, nullable = False)
    first_name = db.Column(db.String(250), nullable = False)
    last_name = db.Column(db.String(250), nullable = False)
    password = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    # def __repr__(self):
    #     return f"<User : {self.id}, {self.email}, {self.first_name}, {self.last_name}>"
