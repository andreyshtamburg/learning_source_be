import os

from flask_script import Manager

from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'development'))
manager = Manager(app)


@manager.command
def run():
    """Run app server"""
    app.run()


@manager.command
def create_db():
    """
    create database schema
    """
    print('creating database schema')
    db.create_all()
    print('done creating database schema')


if __name__ == '__main__':
    manager.run()
