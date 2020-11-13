from flask import Flask
from v2.config import Config

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(Config)

from v2 import routes