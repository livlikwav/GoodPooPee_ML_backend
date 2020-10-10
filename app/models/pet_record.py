from app.utils.datetime import string_to_datetime
import logging
from flask import request
from app.models.dailystatistics import DailyStatistics
from app.models.monthlystatistics import MonthlyStatistics
from app.utils.s3 import upload_fileobj, delete_file
from app import db
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
    def generate_fake(id):
        '''
        user_id and pet_id is same (id)
        number of records == count var
        '''
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker
        
        fake = Faker()
        delta_samples = [
            datetime.timedelta(hours = 0),
            datetime.timedelta(hours = 1),
            datetime.timedelta(hours = 2),
            datetime.timedelta(hours = 3),
            datetime.timedelta(days = 1),
            datetime.timedelta(days = 1, hours = 1),
            datetime.timedelta(days = 2),
            datetime.timedelta(days = 2, hours = 1),
            datetime.timedelta(weeks = 1),
            datetime.timedelta(weeks = 1, hours = 1),
            datetime.timedelta(weeks = 2),
            datetime.timedelta(weeks = 2, hours = 1),
            datetime.timedelta(days = 31),
            datetime.timedelta(days = 31, hours = 1),
            datetime.timedelta(days = 31 * 2),
            datetime.timedelta(days = 31 * 2, hours = 1),
        ]

        seed()
        # get random utc datetime
        datetime_now = datetime.datetime.utcnow()
        for i in range(len(delta_samples)):
            gen_time = datetime_now - delta_samples[i]
            logging.info(f'gen_time : {gen_time}')
            new_record = PetRecord(
                timestamp = gen_time,
                result = choice(['SUCCESS', 'FAIL']),
                image_uuid = '(FAKE)' + fake.uuid4(),

                # only for user 1 and pet 1
                pet_id=id,
                user_id=id
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