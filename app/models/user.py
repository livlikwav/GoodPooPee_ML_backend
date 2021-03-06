import datetime
import logging
from app import db, ma
from app.models.blacklist_user_token import BlacklistUserToken
import bcrypt
import jwt

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(250), unique = True, nullable = False)
    first_name = db.Column(db.String(250), nullable = False)
    last_name = db.Column(db.String(250), nullable = False)
    hashed_password = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.now())
    last_modified_date = db.Column(db.DateTime(timezone=True), nullable = False, default=datetime.datetime.now())

    #     return f"<User : {self.id}, {self.email}, {self.first_name}, {self.last_name}>"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.hashed_password = self.hash_password(password)

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(
            password.encode('UTF-8'),
            bcrypt.gensalt()
        )
        return hashed_password

    def encode_auth_token(self, user_id):
        # Generates the Auth token :return: string
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }
            from manage import app
            return jwt.encode(
                payload,
                app.config['JWT_SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            from manage import app
            payload = jwt.decode(auth_token, app.config['JWT_SECRET_KEY'])
            is_blacklisted_token = BlacklistUserToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'User token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode('UTF-8'),
            self.hashed_password.encode('UTF-8')
        )

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake users for testing.
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        
        seed()
        for i in range(count):
            u = User(
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='test'
            )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        
        logging.info('Successed to set fake users')


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    email = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()