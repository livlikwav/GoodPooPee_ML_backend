from flask import request, jsonify
from flask_restful import Resource
import datetime

from app import db, ma
from app.models.dailystatistics import DailyStatistics
from app.models.monthlystatistics import MonthlyStatistics
from app.utils.datetime import get_kst_date
from app.utils.decorators import confirm_account

class DailyStatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyStatistics
        include_fk = True

class MonthlyStatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MonthlyStatistics
        include_fk = True

# make instances of schemas
daily_stat_schema = DailyStatSchema()
monthly_stat_schema = MonthlyStatSchema()

class DailyStatApi(Resource):
    @confirm_account
    def get(self, pet_id):
        date = get_kst_date(request.args.get("date"))
        selected_record = DailyStatistics.query.filter_by(pet_id = pet_id, date = date).first()
        return daily_stat_schema.dump(selected_record)

class MonthlyStatApi(Resource):
    @confirm_account
    def get(self, pet_id):
        month_date = get_kst_date(request.args.get("date")).replace(day = 1)
        selected_record = MonthlyStatistics.query.filter_by(pet_id = pet_id, date = month_date).first()
        return monthly_stat_schema.dump(selected_record)

# class WeeklyStatApi(Resource):
#     def get(self, pet_id):
#         date = get_kst_date(request.args.get("date"))
#         # how to define that week
        