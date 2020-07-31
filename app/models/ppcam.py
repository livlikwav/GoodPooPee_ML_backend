from datetime import datetime
from .. import db

class Ppcam(db.Model):
    __tablename__ = 'ppcam'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    serial_num = db.Column(db.String(250), unique = True, nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('user',
        backref=db.backref('ppcams', lazy = True))

    # def __repr__(self):
    #     return f"<Ppcam : {self.id}, {self.serial_num}>"
