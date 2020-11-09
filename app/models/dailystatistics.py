import datetime
import logging
from app import db, ma

class DailyStatistics(db.Model):
    __tablename__ = 'daily_stat'
    # naive Date(tzinfo=None, but actually KST)
    date = db.Column(db.Date, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    ratio = db.Column(db.Float, nullable = False)
    # (timezone=True) make DATETIME to TIMESTAMP in Mysql
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.now())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.now())

    pet = db.relationship('Pet',
        backref = db.backref('daily_stats'), lazy = True )

    # def __repr__(self):
    #     return f"<DailyStatistics : {self.count}, {self.success}, {self.fail}>"

    @staticmethod
    def update(pet_id: int, user_id: int, new_datetime: datetime.datetime, old_datetime: datetime.datetime) -> None:
        """
        update daily_stat by new pet record
        """
        # check that date of record is changed
        old_day = old_datetime.date()
        new_day = new_datetime.date()
        try:
            if old_day == new_day: # 1 day update
                DailyStatistics.update_day(pet_id, user_id, new_day)
            else: # 2 day update
                DailyStatistics.update_day(pet_id, user_id, new_day)
                DailyStatistics.update_day(pet_id, user_id, old_day)
        except Exception as e:
            # bubbling for transaction
            raise e

    @staticmethod
    def update_day(pet_id: int, user_id: int, selected_day: datetime.date) -> None:
        """
        Update one day_record by check all records of day
        :Params: Integer, Integer, datetime.date
        :Return:
        """
        from app.models.pet_record import PetRecord
        from sqlalchemy.exc import IntegrityError
        # find all pet records of the day
        selected_daytime_min = datetime.datetime.combine(selected_day, datetime.time.min)
        selected_daytime_max = datetime.datetime.combine(selected_day, datetime.time.max)
        pet_records = PetRecord.query.filter_by(pet_id=pet_id).\
            filter(PetRecord.timestamp >= selected_daytime_min).\
            filter(PetRecord.timestamp <= selected_daytime_max).\
            all()
        # find day record
        day_record = DailyStatistics.query.\
            filter_by(date=selected_day, pet_id=pet_id).first()
        # if last pet_record of the day deleted
        if len(pet_records) == 0:
            if day_record:
                db.session.delete(day_record)
                db.session.commit()
                return
        # update day record
        total_count = 0
        total_success = 0
        if day_record: # exists
            # update day record by all pet records
            for r in pet_records:
                total_count += 1
                if(r.result == 'SUCCESS'):
                    total_success += 1
            day_record.count = total_count
            day_record.success = total_success
            logging.debug(f'not first: {total_success}, {total_count}')
            day_record.ratio = total_success/total_count
            day_record.last_modified_date = datetime.datetime.now()
        else: # first day record
            for r in pet_records:
                total_count += 1
                if(r.result == 'SUCCESS'):
                    total_success += 1
            logging.debug(f'first: {total_success}, {total_count}')
            selected_day_record = DailyStatistics(
                date = selected_day,
                pet_id = pet_id,
                user_id = user_id,
                count = total_count,
                success = total_success,
                ratio = total_success/total_count
            )
            db.session.add(selected_day_record)
        try:
            db.session.commit()
        except IntegrityError as e:
            # db.session.rollback()
            # bubbling for transaction
            raise e
    
class DailyStatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyStatistics
        include_fk = True