"""
statistical data of pet's train result per month
WARNING: ' table's Timestamp vals are base on UTC
But, this table 'monthly_stat' Date vals are based on KST
"""
import datetime
import logging
from dateutil.relativedelta import *
from app.models.dailystatistics import DailyStatistics
from flask import jsonify
from .. import db
import sys

class MonthlyStatistics(db.Model):
    __tablename__ = 'monthly_stat'
    # naive Date(tzinfo=None, but actually KST)
    date = db.Column(db.Date, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    ratio = db.Column(db.Float, nullable = False)
    # (timezone=True) make DATETIME to TIMESTAMP in Mysql
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    pet = db.relationship('Pet',
        backref = db.backref('montly_stats'), lazy = True )
    

    # def __repr__(self):
    #     return f"<MonthlyStatistics : {self.count}, {self.success}, {self.progress}>"

    @staticmethod
    def update(pet_id: int, user_id: int, new_datetime: datetime.datetime, old_datetime: datetime.datetime) -> None:
        """
        update monthly_stat by new pet record
        """
        # check that month value of record is changed
        old_month = old_datetime.date().replace(day=1)
        new_month = new_datetime.date().replace(day=1)
        try:
            if(old_month == new_month): # 1 month update
                MonthlyStatistics.update_month(pet_id, user_id, new_month)
            else: # 2 month update
                MonthlyStatistics.update_month(pet_id, user_id, new_month)
                MonthlyStatistics.update_month(pet_id, user_id, old_month)
        except Exception as e:
            # bubbling for transaction
            raise e

    @staticmethod
    def update_month(pet_id, user_id, selected_month):
        """
        Update one month_record by check all records of month
        :Params: Integer, Integer, datetime.date(naive, but KST)
        :Return:
        """
        from sqlalchemy.exc import IntegrityError
        # find all day records of the month
        daily_records = DailyStatistics.query.\
            filter_by(pet_id=pet_id).\
            filter(DailyStatistics.date >= selected_month).\
            filter(DailyStatistics.date < (selected_month + relativedelta(months=+1))).\
            all()
        # find month record
        month_record = MonthlyStatistics.query.\
            filter_by(date=selected_month, pet_id=pet_id).first()
        # if last day_record of the month deleted
        if len(daily_records) == 0:
            if month_record:
                db.session.delete(month_record)
                db.session.commit()
            return
        # update month record
        count = 0
        success = 0
        if month_record: # exists
            # update month_record by all records of month
            for day in daily_records:
                count += day.count
                success += day.success
            month_record.count = count
            month_record.success = success
            month_record.ratio = success/count
            month_record.last_modified_date = datetime.datetime.utcnow()
        else: # first month record
            for day in daily_records:
                count += day.count
                success += day.success
            new_month_record = MonthlyStatistics(
                date = selected_month,
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
            # bubbling for transaction
            raise e