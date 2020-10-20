from app.utils.datetime import string_to_date
import logging
from flask import request
from flask_restful import Resource
import datetime

from app.models.dailystatistics import DailyStatSchema, DailyStatistics
from app.models.monthlystatistics import MonthlyStatSchema, MonthlyStatistics
from app.utils.decorators import confirm_account

# make instances of schemas
daily_stat_schema = DailyStatSchema()
weekly_stat_schema = DailyStatSchema(many = True)
monthly_stat_schema = MonthlyStatSchema()
total_month_stat_schema = MonthlyStatSchema(many = True)

class DailyStatApi(Resource):
    @confirm_account
    def get(self, pet_id):
        date = string_to_date(request.args.get("date"))
        selected_record = DailyStatistics.query.filter_by(pet_id = pet_id, date = date).first()
        if(selected_record is None):
            logging.info('Daily statistics record not found')
            return {
                "msg" : "Daily stat record not found"
            }, 404
        else:
            return daily_stat_schema.dump(selected_record), 200

class WeeklyStatApi(Resource):
    @confirm_account
    def get(self, pet_id):
        today_date = string_to_date(request.args.get("date"))
        start_date = today_date - datetime.timedelta(days = 6)
        date_max = datetime.datetime.combine(today_date, datetime.time.max)
        date_min = datetime.datetime.combine(start_date, datetime.time.min)
        # Find week records (7 days)
        day_stat_records = DailyStatistics.query.filter_by(pet_id=pet_id).\
            filter(DailyStatistics.date <= date_max).\
            filter(DailyStatistics.date >= date_min).\
            all()
        # check 404
        if len(day_stat_records) == 0:
            return {
                "msg" : "Daily records not found"
            }, 404
        else:
            return weekly_stat_schema.dump(day_stat_records), 200
        


class MonthlyStatApi(Resource):
    @confirm_account
    def get(self, pet_id):
        month_date = string_to_date(request.args.get("date")).replace(day = 1)
        selected_record = MonthlyStatistics.query.filter_by(pet_id = pet_id, date = month_date).first()
        # check 404
        if(selected_record is None):
            logging.info('Monthly statistics record not found')
            return {
                "msg" : "Monthly stat record not found"
            },404
        else:
            return monthly_stat_schema.dump(selected_record), 200

class TotalMonthStatApi(Resource):
    @confirm_account
    def get(self, pet_id: int) -> str:
        records = MonthlyStatistics.query.filter_by(pet_id = pet_id).all()
        # check 404
        if len(records) == 0:
            logging.info('Monthly statistic records not found')
            return {
                "msg" : "Monthly stat records not found"
            }, 404
        else:
            return total_month_stat_schema.dump(records), 200