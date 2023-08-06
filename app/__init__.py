from flask import Flask

app = Flask(__name__)

# Register the routes
from app.routes import *
