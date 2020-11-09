import datetime
from app import db

class BlacklistUserToken(db.Model):
    # Token Model for sorting JWT tokens
    __tablename__ = 'blacklist_user_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())
    
    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistUserToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False