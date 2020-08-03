from datetime import datetime
from .. import db

class DailyStatistics(db.Model):
    __tablename__ = 'daily_stat'

    timestamp = db.Column(db.DateTime, primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    ratio = db.Column(db.Integer, nullable = False)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable = False)
    pet = db.relationship('Pet',
        backref = db.backref('daily_stats'), lazy = True )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


    # def __repr__(self):
    #     return f"<DailyStatistics : {self.count}, {self.success}, {self.fail}>"
