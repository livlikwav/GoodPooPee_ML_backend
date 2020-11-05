from app.models.pet import Pet
from pytz import timezone, utc
import logging
from flask import request
from app.models.dailystatistics import DailyStatistics
from app.models.monthlystatistics import MonthlyStatistics
from app.utils.s3 import upload_fileobj, delete_file
from app import db, ma
import datetime
import uuid

class PetRecord(db.Model):
    __tablename__ = 'pet_record'
    timestamp = db.Column(db.DateTime(timezone=True), primary_key = True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.String(250), nullable = False)
    image_uuid = db.Column(db.String(250), nullable = False)
    # (timezone=True) make DATETIME to TIMESTAMP in Mysql
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    pet = db.relationship('Pet',
        backref = db.backref('records'), lazy = True)

    def __repr__(self):
        return f"<PetRecord : {self.timestamp}, {self.pet_id}, {self.user_id}, {self.result}, {self.image_uuid}>"

    @staticmethod
    def update_stats(pet_id: int, user_id: int, new_datetime: datetime.datetime, old_datetime: datetime.datetime) -> None:
        """
        By new pet record, Update daily_stat and monthly_stat tables
        """
        # update daily_stat first
        try:
            DailyStatistics.update(pet_id, user_id, new_datetime, old_datetime)
            MonthlyStatistics.update(pet_id, user_id, new_datetime, old_datetime)
        except Exception as e:
            # bubbling for transaction
            raise e
    
    def upload_record_image(self, image_file):
        """
        Upload record image file to S3

        :Param image_file: image file stream
        :Return: image_uuid if file was uploaded, else None
        """
        image_uuid = str(uuid.uuid4())
        if upload_fileobj(image_file, image_uuid):
            return image_uuid
        else:
            return None
    
    def delete_record_image(self):
        """
        Delete record image file in S3

        :Return: True if successed, else False
        """
        if delete_file(self.image_uuid):
            return True
        else:
            return False
    
    @staticmethod
    def generate_fake(id: int, is_today:bool=False):
        '''
        :param: user_id
        '''
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        logging.info(f'PetRecord.generate_fake: id={id}, is_today={is_today}')
        
        fake = Faker()
        today_dt_deltas = [
            # today
            datetime.timedelta(hours = 0),
            datetime.timedelta(hours = 1),
            datetime.timedelta(hours = 2),
            datetime.timedelta(hours = 3),
        ]
        past_dt_deltas = [
            # weekdays
            datetime.timedelta(days = 1),
            datetime.timedelta(days = 1, hours = 1),
            datetime.timedelta(days = 2),
            datetime.timedelta(days = 2, hours = 1),
            datetime.timedelta(days = 3),
            datetime.timedelta(days = 3, hours = 1),
            datetime.timedelta(days = 4),
            datetime.timedelta(days = 4, hours = 1),
            datetime.timedelta(days = 5),
            datetime.timedelta(days = 5, hours = 1),
            # week
            datetime.timedelta(weeks = 1),
            datetime.timedelta(weeks = 1, hours = 1),
            datetime.timedelta(weeks = 2),
            datetime.timedelta(weeks = 2, hours = 1),
            # month
            datetime.timedelta(days = 31),
            datetime.timedelta(days = 31, hours = 1),
            datetime.timedelta(days = 31 * 2),
            datetime.timedelta(days = 31 * 2, hours = 1),
            datetime.timedelta(days = 31 * 3),
            datetime.timedelta(days = 31 * 3, hours = 1),
            datetime.timedelta(days = 31 * 4),
            datetime.timedelta(days = 31 * 4, hours = 1),
            datetime.timedelta(days = 31 * 5),
            datetime.timedelta(days = 31 * 5, hours = 1),
        ]

        seed()
        # get random kst datetime for test
        datetime_now = utc.localize(datetime.datetime.utcnow()).astimezone(timezone('Asia/Seoul'))
        logging.info(f'datetime_now = ${datetime_now}')
        # Check pet existency
        pet = Pet.query.filter_by(user_id = id).first()
        if(pet is None):
            raise Exception("Fake user doesn't have pet id")
        # Create fake records
        if(is_today):
            for i in range(len(today_dt_deltas)):
                gen_time = datetime_now - today_dt_deltas[i]
                logging.info(f'gen_time : {gen_time}')
                new_record = PetRecord(
                    timestamp = gen_time,
                    result = choice(['SUCCESS', 'FAIL']),
                    image_uuid = '(FAKE)' + fake.uuid4(),

                    # id param
                    user_id=id,
                    pet_id=pet.id
                )
                try:
                    db.session.add(new_record)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    logging.error(e)
                
                # update stat tables
                PetRecord.update_stats(id, id, gen_time, gen_time)
        else:
            for i in range(len(past_dt_deltas)):
                gen_time = datetime_now - past_dt_deltas[i]
                logging.info(f'gen_time : {gen_time}')
                new_record = PetRecord(
                    timestamp = gen_time,
                    result = choice(['SUCCESS', 'FAIL']),
                    image_uuid = '(FAKE)' + fake.uuid4(),

                    # id param
                    user_id=id,
                    pet_id=pet.id
                )
                try:
                    db.session.add(new_record)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    logging.error(e)
                
                # update stat tables
                PetRecord.update_stats(id, id, gen_time, gen_time)



        logging.info('Successed to set fake pet records')


class PetRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetRecord
        include_fk = True

class DelPetRecordSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PetRecord
    
    timestamp = ma.auto_field()
    pet_id = ma.auto_field()
    user_id = ma.auto_field()

class RecordQuerySchema(ma.Schema):
    class Meta:
        fields = ["timestamp"]