from flask import Flask, render_template, url_for, redirect, request
from rikeripsum.rikeripsum import generate_paragraph as RikerIpsum
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

import json

db = SQLAlchemy()
csrf = CSRFProtect()

def bad_request_error(e):
    return render_template('400.html'), 400
def forbidden_error(e):
    return render_template('403.html'), 403
def page_not_found_error(e):
    return render_template('404.html'), 404
def method_not_allowed_error(e):
    return render_template('405.html'), 405
def server_error(e):
    return render_template('500.html'), 500

def create_app():
    app = Flask(__name__)
    
    config_path = 'config.json'
    with open(config_path) as config_file:
        config = json.load(config_file)

    # General configuration
    app.config['SECRET_KEY'] = config.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DEV_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.get('SQLALCHEMY_TRACK_MODIFICATIONS')  

    db.init_app(app)
    db.app = app

    csrf.init_app(app)
    csrf.app = app


    with app.app_context():
        # Register blueprints
#        from .ticketing import ticketing as ticketing
        
#        app.register_blueprint(ticketing, url_prefix='/ticketing')
        
    
        # Register error handlers
        '''
        app.register_error_handler(400, bad_request_error)
        app.register_error_handler(403, forbidden_error)
        app.register_error_handler(404, page_not_found_error)
        app.register_error_handler(405, method_not_allowed_error)
        app.register_error_handler(500, server_error)
        '''

    # Add RikerIpsum template global
    @app.template_global('RikerIpsum')
    def riker_ipsum(sentences):
        return RikerIpsum(sentences)
    
    # Is this thing on?
    @app.route('/232')
    def its_alive():
        return render_template('itsAlive.html')

    @app.route('/page_check/<page>')
    def page_check(page):
        return render_template(page)

    @app.route('/')
    def home():
        return render_template('index.html')
        
    # @app.route('/favicon-folder/<icon>')
    # def favicon():
    #     return redirect(url_for('static', filename='images/favicon-folder/<icon>'))



    return app
