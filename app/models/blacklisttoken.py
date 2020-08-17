import datetime
from app import db

class BlacklistToken(db.Model):
    # Token Model for sorting JWT tokens
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    
    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False