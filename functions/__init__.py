import flask

from .insert_picture import picture


def register_functions(app: flask.Flask) -> None:
    app.register_blueprint(picture)
