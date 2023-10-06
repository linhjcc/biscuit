from flask import Flask

from functions import register_functions

# https://stackoverflow.com/a/30873279
app = Flask(__name__, instance_relative_config=True)
# default value during development
app.secret_key = "dev"
# overridden if this file exists in the instance folder
app.config.from_pyfile("config.py", silent=True)

register_functions(app)


if __name__ == "__main__":
    app.run()
