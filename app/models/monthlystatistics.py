"""
statistical data of pet's train result per month
WARNING: 'pet_record' table's timestamp vals are base on UTC
But, this table 'monthly_stat' timestamp vals are based on KST
"""
from app.utils.datetime import get_utc_now
from .. import db

class MonthlyStatistics(db.Model):
    __tablename__ = 'monthly_stat'
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    progress = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default = get_utc_now())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default = get_utc_now())

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    pet = db.relationship('Pet',
        backref = db.backref('montly_stats'), lazy = True )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # def __repr__(self):
    #     return f"<MonthlyStatistics : {self.count}, {self.success}, {self.progress}>"

    # @staticmethod
    # def apply_new_record(timestamp, result, pet_id, user_id):
    #     """
    #     Apply new pet_record on monthly_stat tables
    #     """
    
    # @staticmethod
    # def apply_updated_record(timestamp, result, pet_id, user_id):
    #     """
    #     Apply updated pet_record(already existed) on monthly_stat tables 
    #     """