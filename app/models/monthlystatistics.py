from datetime import datetime
from .. import db

class MonthlyStatistics(db.Model):
    __tablename__ = 'monthly_stat'
    timestamp = db.Column(db.DateTime, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    progress = db.Column(db.Integer, nullable = False)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable = False)
    pet = db.relationship('Pet',
        backref = db.backref('montly_stats'), lazy = True )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    # def __repr__(self):
    #     return f"<MonthlyStatistics : {self.count}, {self.success}, {self.progress}>"
