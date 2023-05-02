from .representatives_forms import RepLookupForm
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
#from ismightier_app.models import CharacterTbl, GameTbl, PlayerCharacterTbl, UserInfoTbl
from ismightier_app import db
from wtforms.validators import ValidationError
import requests
from . import representatives


@representatives.route('/')
def homepage():
    form=RepLookupForm()
    if form.validate_on_submit():
        lookupAddress = form.address.data
        return redirect(
            url_for('representatives.results')
        )
    return render_template('index.html')

@representatives.route('/results')
def results():
    lookupAddress = lookupAddress
    session.pop('address')

