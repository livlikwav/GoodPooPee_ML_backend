"""
statistical data of pet's train result per day
WARNING: 'pet_record' table's Timestamp vals are base on UTC
But, this table 'daily_stat' Date vals are based on KST
"""
import datetime
from .. import db

class DailyStatistics(db.Model):
    __tablename__ = 'daily_stat'
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
        backref = db.backref('daily_stats'), lazy = True )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # def __repr__(self):
    #     return f"<DailyStatistics : {self.count}, {self.success}, {self.fail}>"

    @staticmethod
    def update_by_post(kst_date, pet_id, user_id, result):
        """
        update daily_stat by new pet record
        :Params: datetime.date(naive, but actually KST), Integer, Integer, String
        :Return:
        """
        day_record = DailyStatistics.query.filter_by(date=kst_date, pet_id=pet_id, user_id=user_id).first()
        if day_record:
            if result == 'SUCCESS':
                day_record.count = day_record.count + 1
                day_record.success = day_record.success + 1
                day_record.ratio = day_record.success/day_record.count
                day_record.last_modified_date = datetime.datetime.utcnow()
            else:  # Fail
                day_record.count = day_record.count + 1
                day_record.ratio = day_record.success/day_record.count
                day_record.last_modified_date = datetime.datetime.utcnow()
        else: # first day record
            new_day_record = DailyStatistics(
                date = kst_date,
                pet_id = pet_id,
                user_id = user_id,
                count = 1,
                success = 0,
                ratio = 0
            )
            if result == 'SUCCESS':
                new_day_record.success = new_day_record.success + 1
            else: # Fail
                pass
            new_day_record.ratio = new_day_record.success/new_day_record.count
            db.session.add(new_day_record)
        db.session.commit()