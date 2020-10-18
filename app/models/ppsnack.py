import logging
import datetime
from app import db, ma

class Ppsnack(db.Model):
    __tablename__ = 'ppsnack'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ppcam_id = db.Column(db.Integer, db.ForeignKey('ppcam.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    serial_num = db.Column(db.String(250), unique = True, nullable = False)
    feedback = db.Column(db.Float, nullable = False)
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    ppcam = db.relationship('Ppcam',
        backref = db.backref('ppsnacks'), lazy = True)

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake ppcams for testing
        from sqlalchemy.exc import IntegrityError
        from random import seed
        from faker import Faker
        from app.statics.test_samples import ppsnack_samples
        import random

        fake = Faker()

        seed()
        for i in range(count):
            p = Ppsnack(
                serial_num = ppsnack_samples[(i % 10)], # 10 is number of samples
                feedback = random.random(), # 0.0 ~ 1.0
                # match one foreign_key by one user
                # user id start from 1
                user_id = i+1,
                ppcam_id = i+1
            )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            
        logging.info('Successed to set fake ppsnacks')


class PpsnackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ppsnack
        include_fk = True