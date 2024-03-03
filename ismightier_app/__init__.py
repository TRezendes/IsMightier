from flask import Flask, render_template, url_for, redirect, session
from rikeripsum.rikeripsum import generate_paragraph as RikerIpsum
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import json

db = SQLAlchemy()
csrf = CSRFProtect()

def bad_request_error(e):
    return render_template('400.jhtml'), 400
def forbidden_error(e):
    return render_template('403.jhtml'), 403
def page_not_found_error(e):
    return render_template('404.jhtml'), 404
def method_not_allowed_error(e):
    return render_template('405.jhtml'), 405
def im_a_teapot_error(e):
    return render_template('418.jhtml'), 418
def server_error(e):
    return render_template('500.jhtml'), 500

def debug(text):
  print(text)
  return ''

def create_app():
    app = Flask(__name__, subdomain_matching=True)
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.filters['debug']=debug

    config_path = 'config.json'
    with open(config_path) as config_file:
        config = json.load(config_file)

    # General configuration
    app.config['SECRET_KEY'] = config.get('SECRET_KEY')
    app.config['SERVER_NAME'] = config.get('SERVER_NAME')
    app.config['OPENSTATES_API_KEY'] = config.get('OPENSTATES_API_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DEV_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['GOOGLE_CIVIC_INFORMATION_API_KEY'] = config.get('GOOGLE_CIVIC_INFORMATION_API_KEY')

    db.init_app(app)
    db.app = app

    csrf.init_app(app)
    csrf.app = app


    with app.app_context():
        # Register blueprints
        from .thepen import thepen as thepen
        from .home import home as home
        from .letters import letters as letters
        app.register_blueprint(thepen, subdomain='thepen')
        app.register_blueprint(home)
        app.register_blueprint(letters, url_prefix='/letters')


        # Register error handlers
        app.register_error_handler(400, bad_request_error)
        app.register_error_handler(403, forbidden_error)
        app.register_error_handler(404, page_not_found_error)
        app.register_error_handler(405, method_not_allowed_error)
        app.register_error_handler(418, im_a_teapot_error)
        app.register_error_handler(500, server_error)

    # Add RikerIpsum template global
    @app.template_global('RikerIpsum')
    def riker_ipsum(sentences):
        return RikerIpsum(sentences)

    # Is this thing on?
    @app.route('/232')
    def its_alive():
        return render_template('itsAlive.jhtml')

    @app.route('/page_check/<page>')
    def page_check(page):
        return render_template(page)

    @app.route('/')
    def home():
        return redirect(
            url_for('home.homepage')
        )

    # @app.route('/favicon-folder/<icon>')
    # def favicon():
    #     return redirect(url_for('static', filename='images/favicon-folder/<icon>'))



    return app
