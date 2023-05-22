from flask import Blueprint


letters = Blueprint('letters', __name__, template_folder='templates', static_folder='static')

from . import letters_routes
