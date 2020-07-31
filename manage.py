from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db
from app.model import *
# from config import config as Config
import os

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
    app.run()

@manager.command
def recreate_db():
    "Recreate a local db. do not use this on production"
    db.drop_all()
    db.create_all()
    db.session.commit()

# @manager.option(
#     '-n',
#     '--number-users',
#     default=10,
#     type=int,
#     help='Num of each model type to create',
#     dest='number_users'
# )
# def add_fake_data(number_users):
#     "Adds fake data to the db"
#     User.generate_fake(count=number_users)

@manager.command
def setup_prod():
    "Runs the set-up needed for local dev"
    setup_general()

def setup_general():
    "Runs the set-up needed for both local dev and production"
    
if __name__ == '__main__':
    manager.run()
