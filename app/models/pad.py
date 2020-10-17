import datetime
import logging
from app import db, ma

class Pad(db.Model):
    __tablename__ = 'pad'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ppcam_id = db.Column(db.Integer, db.ForeignKey('ppcam.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    lu = db.Column(db.Integer, nullable = False)
    ld = db.Column(db.Integer, nullable = False)
    ru = db.Column(db.Integer, nullable = False)
    rd = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    ppcam = db.relationship('Ppcam',
        backref = db.backref('pads'), lazy = True)

    # def __repr__(self):
    #     return f"<Pad : {self.id}, {self.iu}, {self.id}, {self.ru}, {self.rd}>"

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake pads for testing
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice, randint
        from faker import Faker

        fake = Faker()
        
        seed()
        for i in range(count):
            p = Pad(
                lu = randint(1, 100),
                ld = randint(1, 100),
                ru = randint(1, 100),
                rd = randint(1, 100),

                # match one foreign_key by one user
                # id start from 1
                ppcam_id=i+1,
                user_id=i+1
            )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        
        logging.info('Successed to set fake pads')

class PadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pad
        include_fk = True