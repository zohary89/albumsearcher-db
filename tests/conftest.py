from albumsearcher import crud_actions
from albumsearcher.app import app
from albumsearcher.db import db
from albumsearcher.mapping import Album, Like 
from datetime import datetime
import pytest


# הבדיקות מבוססות על דטה בייס בזיכרון
# Using the following line in app.py:
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite://'
@pytest.fixture
def client():
    app.config["TESTING"] = True

    ctx = app.test_request_context()
    ctx.push()

    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

    db.drop_all()
    ctx.pop()


@pytest.fixture
def db_session():
    yield db.session


@pytest.fixture
def user():
    user = crud_actions.add_user(db.session, 'dani', '1234', 'dani', '01.11.1990', 'Israel')
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture
def album():
    album = Album(
        album_id="2115888", album_name="Echoes of Silence", artist="The Weeknd", year="2011", rate="9", image_path="https://www.theaudiodb.com/images/media/album/thumb/xwvwvp1342551819.jpg"
        )
    db.session.add(album)
    db.session.commit()
    yield album
    db.session.delete(album)
    db.session.commit()


@pytest.fixture
def like(user, album):
    like = Like(
            user_id=user.user_id, album_id=album.album_id, like_time=datetime.now())
    db.session.add(like)
    db.session.commit()
    yield like
    db.session.delete(like)
    db.session.commit()


@pytest.fixture
def album2():
    album = Album(
        album_id="2115777", album_name="Trilogy", artist="The Weeknd", year="2012", rate="8", image_path=None
        )
    db.session.add(album)
    db.session.commit()
    yield album
    db.session.delete(album)
    db.session.commit()


@pytest.fixture
def like2(user, album2):
    like = Like(
            user_id=user.user_id, album_id=album2.album_id, like_time=datetime.now())
    db.session.add(like)
    db.session.commit()
    yield like
    db.session.delete(like)
    db.session.commit()

