from datetime import datetime
from .. import db

class Pet(db.Model):
    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(250), nullable = False)
    breed = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(250), nullable = False)
    birth = db.Column(db.DateTime, nullable = False)
    adoption = db.Column(db.DateTime, nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User',
        backref = db.backref('pets'), lazy = True)

    # def __repr__(self):
    #     return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"
