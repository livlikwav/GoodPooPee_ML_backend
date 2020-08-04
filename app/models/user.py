from datetime import datetime
from .. import db
import bcrypt

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(250), unique = True, nullable = False)
    first_name = db.Column(db.String(250), nullable = False)
    last_name = db.Column(db.String(250), nullable = False)
    hashed_password = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    # def __repr__(self):
    #     return f"<User : {self.id}, {self.email}, {self.first_name}, {self.last_name}>"

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
                hashed_password='test_password'
            )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode('UTF-8'),
            self.hashed_password.encode('UTF-8')
        )