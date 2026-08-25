from flask import Flask, jsonify
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
    ma.init_app(flask_app)  # ← Fixed: removed "chan"
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
    # ROUTES
    # ============================================================

    @flask_app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "BIGF API is running!",
            "endpoints": {
                "health": "/health",
                "api": "/api/"
            }
        })

    @flask_app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    @flask_app.route("/test", methods=["GET"])
    def test():
        return jsonify({"message": "Test route works!"})

    return flask_app