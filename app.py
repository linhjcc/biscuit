from functions import picture
from flask import Flask

# https://stackoverflow.com/a/30873279
app = Flask(__name__, instance_relative_config=True)
# default value during development
app.secret_key = "dev"
# overridden if this file exists in the instance folder
app.config.from_pyfile("config.py", silent=True)

urls = [picture]
for u in urls:
    app.register_blueprint(u)


if __name__ == "__main__":
    app.run()
