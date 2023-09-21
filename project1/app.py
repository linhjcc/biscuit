from insertPicture import picture
from flask import Flask

app = Flask(__name__)

app.secret_key = "any random string"
urls = [picture]
for u in urls:
    app.register_blueprint(u)


if __name__ == "__main__":
    app.run()



