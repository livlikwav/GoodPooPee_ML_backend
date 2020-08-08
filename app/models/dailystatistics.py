"""
statistical data of pet's train result per day
WARNING: 'pet_record' table's Timestamp vals are base on UTC
But, this table 'daily_stat' Date vals are based on KST
"""
import datetime
from app.utils.datetime import get_kst_date
from .. import db
import sys

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
    def update(pet_record, last_timestamp):
        """
        update daily_stat by new pet record
        :Params: PetRecord(), datetime.datetime(naive, but UTC)
        :Return:
        """
        # check that date of record is changed
        last_kst_day = get_kst_date(last_timestamp)
        kst_day = get_kst_date(pet_record.timestamp)
        if last_kst_day == kst_day: # 1 day update
            DailyStatistics.update_day(pet_record.pet_id, pet_record.user_id, kst_day)
        else: # 2 day update
            DailyStatistics.update_day(pet_record.pet_id, pet_record.user_id, kst_day)
            DailyStatistics.update_day(pet_record.pet_id, pet_record.user_id, last_kst_day)

    @staticmethod
    def update_day(pet_id, user_id, kst_day):
        """
        Update one day_record by check all records of day
        :Params: Integer, Integer, datetime.date(naive, but KST)
        :Return:
        """
        from app.models.petrecord import PetRecord
        from sqlalchemy.exc import IntegrityError
        # find all pet records of the day
        kst_daytime_min = datetime.datetime.combine(kst_day, datetime.time.min)
        kst_daytime_max = datetime.datetime.combine(kst_day, datetime.time.max)
        pet_records = PetRecord.query.filter_by(pet_id=pet_id, user_id=user_id).\
            filter(PetRecord.timestamp >= kst_daytime_min).\
            filter(PetRecord.timestamp <= kst_daytime_max).\
            all()
        # find day record
        day_record = DailyStatistics.query.\
            filter_by(date=kst_day, pet_id=pet_id, user_id=user_id).first()
        # if last pet_record of the day deleted
        if len(pet_records) == 0:
            if day_record:
                db.session.delete(day_record)
                db.session.commit()
                return
        # update day record
        count = 0
        success = 0
        if day_record: # exists
            # update day record by all pet records
            for r in pet_records:
                count += 1
                if(r.result == 'SUCCESS'):
                    success += 1
            day_record.count = count
            day_record.success = success
            day_record.ratio = success/count
            day_record.last_modified_date = datetime.datetime.utcnow()
        else: # first day record
            for r in pet_records:
                count += 1
                if(r.result == 'SUCCESS'):
                    success += 1
            new_day_record = DailyStatistics(
                date = kst_day,
                pet_id = pet_id,
                user_id = user_id,
                count = count,
                success = success,
                ratio = success/count
            )
            db.session.add(new_day_record)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(str(e), file=sys.stderr)