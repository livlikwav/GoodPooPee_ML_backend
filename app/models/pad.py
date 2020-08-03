from datetime import datetime
from .. import db

class Pad(db.Model):
    __tablename__ = 'pad'

    id = db.Column(db.Integer, primary_key = True)
    lu = db.Column(db.Integer, nullable = False)
    ld = db.Column(db.Integer, nullable = False)
    ru = db.Column(db.Integer, nullable = False)
    rd = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    ppcam_id = db.Column(db.Integer, db.ForeignKey('ppcam.id'), nullable = False)
    ppcam = db.relationship('Ppcam',
        backref = db.backref('pads'), lazy = True)
        
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    # def __repr__(self):
    #     return f"<Pad : {self.id}, {self.iu}, {self.id}, {self.ru}, {self.rd}>"
