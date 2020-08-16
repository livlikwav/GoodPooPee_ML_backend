from flask import request
from app.models.dailystatistics import DailyStatistics
from app.models.monthlystatistics import MonthlyStatistics
from app.utils.datetime import get_kst_date
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

    def update_stats(self, last_timestamp):
        """
        By new pet record, Update daily_stat and monthly_stat tables
        :Param: datetime.datetime(naive, but UTC)
        :Return:
        """
        # update daily_stat first
        DailyStatistics.update(self, last_timestamp)
        MonthlyStatistics.update(self, last_timestamp)
    
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
    
    def delete_record_image(self, object_name):
        """
        Delete record image file in S3

        :Param object_name: String
        :Return: True if successed, else False
        """
        if delete_file(object_name):
            return True
        else:
            return False
        
        
        
    @staticmethod
    def generate_fake(count):
        # Generate a number of fake pet records for testing
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker
        
        fake = Faker()

        seed()
        # get random utc datetime
        time_now = datetime.datetime.utcnow() - datetime.timedelta(hours = count)
        for i in range(count):
            p = PetRecord(
                timestamp = time_now + (datetime.timedelta(hours=1)*i),
                result = choice(['SUCCESS', 'FAIL']),
                image_uuid = '(FAKE)' + fake.uuid4(),

                # match one foreign_key by one user
                # id start from 1
                pet_id=i+1,
                user_id=i+1
            )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

