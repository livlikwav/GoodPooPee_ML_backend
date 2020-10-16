import logging
import pytz
import datetime
from .. import db, ma

class Pet(db.Model):
    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    name = db.Column(db.String(250), nullable = False)
    breed = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(250), nullable = False)
    birth = db.Column(db.DateTime(timezone=True), nullable = True)
    adoption = db.Column(db.DateTime(timezone=True), nullable = True)
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default = datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default = datetime.datetime.utcnow())

    user = db.relationship('User',
        backref = db.backref('pets'), lazy = True)

    def __repr__(self):
        return f"<Pet : {self.id}, {self.user_id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake pets for testing.
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker
        from .test_samples import dog_name_samples, breed_samples
        
        fake = Faker()

        seed()
        for i in range(count):
            # get random datetime
            timestamp = fake.date_time_between(start_date='-10y')
            date = timestamp.date()
            time = timestamp.time()
            # get utc random datetime
            temp_datetime = pytz.utc.localize(datetime.datetime.combine(date, time))
            p = Pet(
                name=choice(dog_name_samples),
                breed=choice(breed_samples),
                gender=choice(['male', 'female']),
                # get random datetime
                birth=temp_datetime,
                # be adopt after 8 weeks
                adoption=temp_datetime + datetime.timedelta(weeks = 8),
                
                # match one foreign_key by one user
                # user id start from 1
                user_id = i+1
            )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        logging.info('Successed to set fake pets')



class PetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pet
        include_fk = True

    id = ma.auto_field()
    user_id = ma.auto_field()
    name = ma.auto_field()
    breed = ma.auto_field()
    gender = ma.auto_field()
    birth = ma.auto_field()
    adoption = ma.auto_field()