# Run:
# (to open) flask run
# (close)   ctrl+C

# Migrations:
# (init)            flask db init
# (make migrations) flask db migrate
# (apply migration) flask db upgrade

# Run continuously with docker:
# (create img)  docker build -t flask-smorest-api .
# (as daemon)   docker run -dp 5000:5000 -w //app -v "$(Get-Location)://app" flask-smorest-api
# (in terminal) docker run -p 5000:5000 -w //app -v "$(Get-Location)://app" flask-smorest-api
# (to see id)   docker container ls
# (to kill)     docker container kill <container-id>

# Swagger interactive documentation:
# http://localhost:5000/swagger-ui

# -----------------------------------

import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate  # flask migrate es la conexión entre Alembic y Flask
from flask_jwt_extended import JWTManager

from db import db
import models
from blocklist import BLOCKLIST

from resources.user import blp as UserBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"

    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    # no muy seguro, puedes cambiar "jose" por str(secrets.SystemRandom().getrandbits(128))
    app.config["JWT_SECRET_KEY"] = "jose"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if (
            identity == 1
        ):  # aquí asumimos que el usuario con id 1 es el admin, esto no necesariamente es cierto, normalmente se lee desde un config file o de la base de datos
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    # DEPRECATED
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()
    # So...
    # ------------------------
    # ahora que usamos flask migrate, no necesitamos a SQLAlchemy para inicializar la db
    # with app.app_context():
    #    db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
