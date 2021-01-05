from albumsearcher import routes
from albumsearcher.db import db
from flask import Flask


def create_app(**configs):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(**configs)
    db.init_app(app)
    app.register_blueprint(routes.bp)
    return app