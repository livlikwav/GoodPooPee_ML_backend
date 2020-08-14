from app.models.dailystatistics import DailyStatistics
from app.models.monthlystatistics import MonthlyStatistics
from app.utils.datetime import get_kst_date
import datetime
from .. import db

class PetRecord(db.Model):
    __tablename__ = 'pet_record'
    timestamp = db.Column(db.DateTime(timezone=True), primary_key = True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.String(250), nullable = False)
    photo_url = db.Column(db.String(250), nullable = False)
    # (timezone=True) make DATETIME to TIMESTAMP in Mysql
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.utcnow())

    pet = db.relationship('Pet',
        backref = db.backref('records'), lazy = True)

    def __repr__(self):
        return f"<PetRecord : {self.timestamp}, {self.pet_id}, {self.user_id},\
             {self.result}, {self.photo_url}>"

    def update_stats(self, last_timestamp):
        """
        By new pet record, Update daily_stat and monthly_stat tables
        :Param: datetime.datetime(naive, but UTC)
        :Return:
        """
        # update daily_stat first
        DailyStatistics.update(self, last_timestamp)
        MonthlyStatistics.update(self, last_timestamp)

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

