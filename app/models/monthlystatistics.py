"""
statistical data of pet's train result per month
WARNING: 'pet_record' table's Timestamp vals are base on UTC
But, this table 'monthly_stat' Date vals are based on KST
"""
import datetime
from dateutil.relativedelta import *
from app.utils.datetime import get_kst_date
from app.models.dailystatistics import DailyStatistics
from flask import jsonify
from .. import db
import sys

class MonthlyStatistics(db.Model):
    __tablename__ = 'monthly_stat'
    # naive Date(tzinfo=None, but actually KST)
    date = db.Column(db.Date, primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    ratio = db.Column(db.Float, nullable = False)
    # (timezone=True) make DATETIME to TIMESTAMP in Mysql
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    pet = db.relationship('Pet',
        backref = db.backref('montly_stats'), lazy = True )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # def __repr__(self):
    #     return f"<MonthlyStatistics : {self.count}, {self.success}, {self.progress}>"

    @staticmethod
    def update(pet_record, last_timestamp):
        """
        update monthly_stat by new pet record
        :Params: PetRecord(), datetime.datetime(naive, but UTC)
        :Return:
        """
        # check that month value of record is changed
        last_kst_month = get_kst_date(last_timestamp).replace(day=1)
        kst_month = get_kst_date(pet_record.timestamp).replace(day=1)
        if(last_kst_month == kst_month): # 1 month update
            MonthlyStatistics.update_month(pet_record.pet_id, pet_record.user_id, kst_month)
        else: # 2 month update
            MonthlyStatistics.update_month(pet_record.pet_id, pet_record.user_id, kst_month)
            MonthlyStatistics.update_month(pet_record.pet_id, pet_record.user_id, last_kst_month)

    @staticmethod
    def update_month(pet_id, user_id, kst_month):
        """
        Update one month_record by check all records of month
        :Params: Integer, Integer, datetime.date(naive, but KST)
        :Return:
        """
        from sqlalchemy.exc import IntegrityError
        # find all day records of the month
        daily_records = DailyStatistics.query.\
            filter_by(pet_id=pet_id, user_id=user_id).\
            filter(DailyStatistics.date >= kst_month).\
            filter(DailyStatistics.date < (kst_month + relativedelta(months=+1))).\
            all()
        if daily_records is None:
            return jsonify({
                "status" : "Fail",
                "msg" : "No record in daily_stat table, maybe not updated yet"
            })
        # update month record
        month_record = MonthlyStatistics.query.\
            filter_by(date=kst_month, pet_id=pet_id, user_id=user_id).first()
        if month_record:
            count = 0
            success = 0
            # update month_record by all records of month
            for day in daily_records:
                count += day.count
                success += day.success
            month_record.count = count
            month_record.success = success
            month_record.ratio = success/count
            month_record.last_modified_date = datetime.datetime.utcnow()
        # first month record
        else:
            count = 0
            success = 0
            for day in daily_records:
                count += day.count
                success += day.success
            new_month_record = MonthlyStatistics(
                date = kst_month,
                pet_id = pet_id,
                user_id = user_id,
                count = count,
                success = success,
                ratio = success/count
            )
            db.session.add(new_month_record)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(str(e), file=sys.stderr)