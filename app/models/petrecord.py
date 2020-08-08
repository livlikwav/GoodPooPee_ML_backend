from app.models.dailystatistics import DailyStatistics
from app.models.monthlystatistics import MonthlyStatistics
from app.utils.datetime import get_kst_date
import datetime
from .. import db

class PetRecord(db.Model):
    __tablename__ = 'pet_record'
    timestamp = db.Column(db.DateTime(timezone=True), primary_key = True)
    result = db.Column(db.String(250), nullable = False)
    photo_url = db.Column(db.String(250), nullable = False)
    # (timezone=True) make DATETIME to TIMESTAMP in Mysql
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    pet = db.relationship('Pet',
        backref = db.backref('records'), lazy = True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f"<PetRecord : {self.timestamp}, {self.pet_id}, {self.user_id},\
             {self.result}, {self.photo_url}>"

    def update_stats_by_post(self):
        """
        By new pet record, Update daily_stat and monthly_stat tables
        :Param:
        :Return:
        """
        # change UTC.datetime to KST.date
        kst_date = get_kst_date(self.timestamp)
        # update daily_stat first
        DailyStatistics.update_by_post(kst_date, self.pet_id, self.user_id, self.result)
        MonthlyStatistics.update_by_post(kst_date, self.pet_id, self.user_id)

    def update_stats_by_put(self, last_timestamp):
        """
        By updated pet record, Update daily_stat and monthly_stat tables
        :Param: last_timestamp
        :Return:
        """
        # change UTC to KST
        # kst_date = utc_to_kst_date(self.timestamp)
        
        

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
                photo_url = fake.image_url(),

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