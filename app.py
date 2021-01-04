import os

from albumsearcher.app import create_app
from albumsearcher.db import db


if __name__ == '__main__':
    configs = {
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL') or 'sqlite://',
        'SECRET_KEY': os.environ.get('SECRET_KEY') or "SECRET"
    }
    app = create_app(**configs)
    with app.app_context():
        db.create_all()

    app.run()
    