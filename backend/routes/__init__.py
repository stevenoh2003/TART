from flask import Blueprint

bp = Blueprint('main', __name__)

from backend.routes import product  # Import your route modules here
