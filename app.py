import os

from albumsearcher.app import create_app
from albumsearcher.db import db

configs = {
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    'SECRET_KEY': os.environ.get('SECRET_KEY')
}

app = create_app(**configs)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()