from flask import jsonify
from datetime import datetime
from .. import db

class Ppcam(db.Model):
    __tablename__ = 'ppcam'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    serial_num = db.Column(db.String(250), unique = True, nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User',
        backref=db.backref('ppcams', lazy = True))

    # def __repr__(self):
    #     return f"<Ppcam : {self.id}, {self.serial_num}>"

    def get_ppsnack(self, test=False):
        """
        request ppcam to get method for ppsnack
        params Boolean
        returns JSON(ppsnack data)
        """
        if(test):
            # FAKE DATA FOR TESTING
            return jsonify({
                "serial_num":"thisisfakedata",
                "connection":"True",
                "power":"True",
                "feedback_ratio":"1"
            })
        else:
            pass

    def put_ppsnack(self, feedback_ratio, test=False):
        """
        request ppcam to put method for ppsnack
        params Float, Boolean
        returns Boolean
        """
        if(test):
            # FAKE SUCCESS MSG TEMPLATE
            {
                "status":"FAKESUCCESS",
                "msg":"this is fake success"
            }
            return True
        else:
            pass

    def get_ppsnack_feeding(self, test=False):
        """
        request ppsnack to feed dog via ppcam
        params Boolean
        returns Boolean
        """
        if(test):
            # FAKE SUCCESS MSG TEMPLATE
            {
                "status":"FAKESUCCESS",
                "msg":"this is fake success"
            }
            return True
        else:
            pass

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake ppcams for testing
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()

        seed()
        for i in range(count):
            p = Ppcam(
                serial_num = fake.ean(),
                # match one foreign_key by one user
                # user id start from 1
                user_id = i+1
            )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()