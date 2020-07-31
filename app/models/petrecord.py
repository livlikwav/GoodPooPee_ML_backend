from datetime import datetime
from .. import db

class PetRecord(db.Model):
    __tablename__ = 'pet_record'
    timestamp = db.Column(db.DateTime, primary_key = True)
    result = db.Column(db.String(250), nullable = False)
    photo_url = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('pet',
        backref = db.backref('records'), lazy = True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # def __repr__(self):
    #     return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"
