from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db
from app.models import *
# from config import config as Config
import os
import logging

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# flask-script and migrate be initialized out of __init__
manager = Manager(app)
migrate = Migrate(app, db)

# def make_shell_context():
#     return dict(app=app, db=db)

# manager.add_command('shell', Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', port='80')
    logging.info('Flask app run')

@manager.command
def recreate_db():
    "Recreate a local db. do not use this on production"
    db.drop_all()
    db.create_all()
    db.session.commit()
    logging.warning('DB was recreated')


@manager.command
def set_test_env_1():
    User.generate_fake(count=10)
    Pet.generate_fake(count=10)
    PetRecord.generate_fake(id=1)
    PpcamSerialNums.generate_fake()

@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Num of each model type to create',
    dest='number_users'
)
def add_fake_data(number_users):
    "Adds fake data to the db"
    User.generate_fake(count=number_users)
    Pet.generate_fake(count=number_users)

    # Dont need to make these fake datas
    # Pad.generate_fake(count=number_users)
    # Ppcam.generate_fake(count=number_users)
    # Ppsnack.generate_fake(count=number_users)

@manager.option(
    '-i'
    '--ids',
    default=1,
    type=int,
    help='define user_id and pet_id (same)',
    dest='id'
)
def add_fake_pet_records(id):
    "Adds fake pet records to db"
    PetRecord.generate_fake(id=id)

@manager.command
def add_fake_serial_nums():
    "Adds fake ppcam serial nums to db"
    PpcamSerialNums.generate_fake()

@manager.command
def setup_prod():
    "Runs the set-up needed for local dev"
    setup_general()

def setup_general():
    "Runs the set-up needed for both local dev and production"
    
if __name__ == '__main__':
    manager.run()
