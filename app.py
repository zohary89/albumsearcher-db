import os

from albumsearcher import audiodb_api as api
from albumsearcher import crud_actions
from albumsearcher.db import db
import bcrypt
from flask import Flask, g, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "SECRET"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = crud_actions.get_user_by_id(db.session, session['user_id'])
        g.user = user


@app.route('/', methods=['GET'])
def index():
    if not g.user:
        return redirect(url_for("connect_page"))
    is_valid_artist = request.args.get('valid_artist', default='true') == 'true'
    top_rated_albums = crud_actions.get_top_likes_albums(db.session)
    return render_template('index.html', is_valid_artist=is_valid_artist, top_rated_albums=top_rated_albums)


@app.route('/connect-page', methods=['GET'])
def connect_page():
    session.pop('user_id', None)
    login_failed = request.args.get('login_failed', default='false') == 'true'
    return render_template('connect.html', login_failed=login_failed)


@app.route('/connect', methods=['POST'])
def connect():
    session.pop('user_id', None)
    username = request.form["user-name"]
    password = request.form["psw"].encode('utf-8')
    user = crud_actions.get_user_by_username(db.session, username)
    if user is not None and bcrypt.checkpw(password, user.password.encode('utf-8')):
        session['user_id'] = user.user_id
        return redirect(url_for("index"))
    else:
        return redirect(url_for("connect_page", login_failed='true'))


@app.route('/register-page', methods=["GET"])
def register_page():
    user_exist = request.args.get('user_exist', default='false') == 'true'
    return render_template('register.html', user_exist=user_exist)


@app.route('/register', methods=["POST"])
def register():
    username = request.form["user-name"]
    password = request.form["psw"]
    name = request.form["name"]
    birthday = request.form["birthday"]
    country = request.form["country"]
    if not username or not password or not name or not birthday or not country:
        return redirect(url_for("register_page"))
    if crud_actions.get_user_by_username(db.session, username) is None:
        crud_actions.add_user(db.session, username, password, name, birthday, country)
        return redirect(url_for("connect_page"))
    return redirect(url_for("register_page", user_exist='true'))


@app.route('/update', methods=["GET", 'POST'])
def update_profile():
    if not g.user:
        return redirect(url_for("connect_page"))
    old_username = g.user.username
    if request.method == 'POST':
        username = request.form['user-name']
        name = request.form['name']
        birthday = request.form['birthday']
        country = request.form['country']
        if old_username == username or crud_actions.get_user_by_username(db.session, username) is None:
            crud_actions.update_user(db.session, g.user.user_id, username, name, birthday, country)
            return redirect(url_for("index"))
        return redirect(url_for("update_profile", user_exist='true'))
    else:
        user_exist = request.args.get('user_exist', default='false') == 'true'
        return render_template('update.html', user_exist=user_exist)


@app.route('/albums', methods=['GET'])
def albums():
    if not g.user:
        return redirect(url_for("connect_page"))
    artist_name = request.args.get('artist').title()
    albums_resp_json = api.get_artist_albums(artist_name)
    artist_resp_json = api.get_artist_details(artist_name)
    if albums_resp_json['album'] is None:
        return redirect(url_for('index', valid_artist='false'))
    albums = albums_resp_json['album']
    artist = artist_resp_json['artists']
    sorted_albums = sorted(albums, key=lambda k: k["intYearReleased"], reverse=True) 
    return render_template(
        'results.html', 
        ARTIST_NAME=artist_name, 
        all_albums=sorted_albums, 
        artist_info=artist,
    )


def get_album_details_api(album_id):
    album_resp_json = api.get_album_details(album_id)
    if album_resp_json['album'] is None:
        return None
    return album_resp_json['album'][0]


def get_album_tracks_api(album_id):
    tracks_resp_json = api.get_album_tracks(album_id)
    return tracks_resp_json['track']


@app.route('/albums/<album_id>')
def album(album_id):
    if not g.user:
        return redirect(url_for("connect_page"))
    album_info = get_album_details_api(album_id)
    if album_info is None:
        return redirect(url_for('index'))
    tracks_info = get_album_tracks_api(album_id)
    like = request.args.get('like', default='false') == 'true'
    if crud_actions.get_like_data(db.session, g.user.user_id, album_id):
        like = 'true'
    total_likes = crud_actions.get_album_likes_amount(db.session, album_id)
    return render_template(
        'album.html',
        album_info=album_info,
        tracks_info=tracks_info, 
        like=like,
        total_likes=total_likes
    )


@app.route('/like', methods=['POST'])
def like():
    if not g.user:
        return redirect(url_for("connect_page"))
    album_id = request.form["idalbum"]
    album_info = get_album_details_api(album_id)
    name = album_info['strAlbum']
    artist = album_info['strArtist']
    year = album_info['intYearReleased']
    rate = album_info['intScore']
    image = album_info['strAlbumThumb']
    crud_actions.add_or_update_album(db.session, album_id, name, artist, year, rate, image)
    crud_actions.add_like_by_ids(db.session, g.user.user_id, album_id)
    return redirect(url_for('album', album_id=album_id, like="true"))


@app.route('/unlike', methods=['POST'])
def unlike():
    if not g.user:
        return redirect(url_for("connect_page"))
    album_id = request.form["idalbum"]
    crud_actions.delete_like(db.session, g.user.user_id, album_id)
    return redirect(url_for('album', album_id=album_id, like="false"))


@app.route('/favorites', methods=['GET'])
def favorites():
    if not g.user:
        return redirect(url_for("connect_page"))
    favorites = crud_actions.get_likes_albums_by_user_id(db.session, g.user.user_id)
    likes_amount = crud_actions.get_likes_per_user(db.session, g.user.user_id)
    return render_template('favorites.html', favorites=favorites, likes=likes_amount)  