from datetime import datetime, timedelta
from .. import db

class PetRecord(db.Model):
    __tablename__ = 'pet_record'
    timestamp = db.Column(db.DateTime, primary_key = True)
    result = db.Column(db.String(250), nullable = False)
    photo_url = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('Pet',
        backref = db.backref('records'), lazy = True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # def __repr__(self):
    #     return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake pet records for testing
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker
        
        fake = Faker()

        seed()
        # generate random time from now
        time_now = datetime.utcnow() - timedelta(hours = count)
        for i in range(count):
            p = PetRecord(
                timestamp = time_now + (timedelta(hours=1)*i),
                result = choice(['SUCCESS', 'FAIL']),
                photo_url = fake.image_url(),

                # match one foreign_key by one user
                # id start from 1
                pet_id=i+1,
                user_id=i+1
            )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()