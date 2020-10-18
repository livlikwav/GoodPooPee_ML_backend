import datetime
import logging
from app import db, ma

class Pad(db.Model):
    '''
        Dog size = 224 * 224
        Ppcam(raspb cam) size = 800 * 600
        So,
        0 <= x <= 800
        0 <= y <= 600
    '''
    __tablename__ = 'pad'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ppcam_id = db.Column(db.Integer, db.ForeignKey('ppcam.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ldx = db.Column(db.Integer, nullable = False)
    ldy = db.Column(db.Integer, nullable = False)
    lux = db.Column(db.Integer, nullable = False)
    luy = db.Column(db.Integer, nullable = False)
    rdx = db.Column(db.Integer, nullable = False)
    rdy = db.Column(db.Integer, nullable = False)
    rux = db.Column(db.Integer, nullable = False)
    ruy = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    ppcam = db.relationship('Ppcam',
        backref = db.backref('pads'), lazy = True)

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake pads for testing
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        from faker import Faker

        fake = Faker()
        
        seed()
        for i in range(count):
            p = Pad(
                # 0 <= x <= 800
                lux = randint(0, 800),
                ldx = randint(0, 800),
                rux = randint(0, 800),
                rdx = randint(0, 800),
                # 0 <= y <= 600
                luy = randint(0, 600),
                ldy = randint(0, 600),
                ruy = randint(0, 600),
                rdy = randint(0, 600),

                # match one foreign_key by one user
                # id start from 1
                ppcam_id=i+1,
                user_id=i+1
            )
            try:
                db.session.add(p)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        
        logging.info('Successed to set fake pads')

class PadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pad
        include_fk = True