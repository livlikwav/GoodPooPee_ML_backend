"""
statistical data of pet's train result per day
WARNING: 'pet_record' table's timestamp vals are base on UTC
But, this table 'daily_stat' timestamp vals are based on KST
"""
from app.models.petrecord import PetRecord
from app.utils.datetime import get_utc_now
from .. import db

class DailyStatistics(db.Model):
    __tablename__ = 'daily_stat'

    timestamp = db.Column(db.DateTime, primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    ratio = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default = get_utc_now())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default = get_utc_now())

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    pet = db.relationship('Pet',
        backref = db.backref('daily_stats'), lazy = True )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


    # def __repr__(self):
    #     return f"<DailyStatistics : {self.count}, {self.success}, {self.fail}>"

    # @staticmethod
    # def apply_new_record(timestamp, result, pet_id, user_id):
    #     """
    #     Apply new pet_record on daily_stat table
    #     :Params: datetime.datetime, String, Integer, Integer
    #     :Return:
    #     """
    #     # check that already exists
    
    # @staticmethod
    # def apply_updated_record(timestamp, result, pet_id, user_id):
    #     """
    #     Apply updated pet_record(already existed) on daily_stat table
    #     :Params: datetime.datetime, String, Integer, Integer
    #     :Return:
    #     """

    # @staticmethod
    # def check_existence(timestamp, pet_id, user_id):
    #     """
    #     Check existence of record in table by primary keys
    #     :Params: datetime.datetime, Integer, Integer
    #     "Return: True|False
    #     """
        # if(DailyStatistics.query.filter_by(timestamp))
        # datetime.datetime.date().replace(day=1) >>> only month
        # datetime.datetime.date() >>> only date