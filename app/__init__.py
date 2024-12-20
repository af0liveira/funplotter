from flask import Flask
from flask_session import Session

from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['zip'] = zip
Session(app)

# NOTE: Keep this at the bottom, in order to avoid circular imports.
from app import routes


if __name__ == '__main__':
    app.run(debug=True)
