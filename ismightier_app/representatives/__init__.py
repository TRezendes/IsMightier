from flask import Blueprint



representatives = Blueprint('representatives', __name__, template_folder='templates', static_folder='static')

from . import representatives_routes
