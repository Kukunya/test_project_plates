from flask import Flask
from conf import FlaskConf
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(FlaskConf)
db = SQLAlchemy(app)

from . import views
