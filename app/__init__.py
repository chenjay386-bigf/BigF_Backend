
from flask import Flask
from flask_restful import Api

from app.config import Config
from app.extensions import cors, db, jwt, ma, migrate


def create_app(test_config=None):
    flask_app = Flask(__name__)

    # ============================================================
    # CONFIGURATION
    # ============================================================

    flask_app.config.from_object(Config)

    if test_config:
        flask_app.config.update(test_config)

    # ============================================================
    # INITIALIZE EXTENSIONS
    # ============================================================

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    ma.init_app(flask_app)
    jwt.init_app(flask_app)
    cors.init_app(flask_app)

    # ============================================================
    # LOAD MODELS
    # ============================================================

    with flask_app.app_context():
        from app import models

    # ============================================================
    # FLASK-RESTFUL
    # ============================================================

    api = Api(flask_app)

    # ============================================================
    # REGISTER API RESOURCES
    # ============================================================

    from app.resources import register_resources

    register_resources(api)

    # ============================================================
    # HEALTH CHECK
    # ============================================================

    @flask_app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return flask_app

