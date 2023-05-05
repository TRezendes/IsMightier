from flask import Blueprint


thepen = Blueprint('thepen', __name__, subdomain='thepen', template_folder='templates', static_folder='static')

from . import thepen_routes
