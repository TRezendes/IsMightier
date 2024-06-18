from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from .home_funcs import GetFedRepInfo, RepNormal
from ismightier_app.models import USCongressTbl
from wtforms.validators import ValidationError
from sqlalchemy import and_,create_engine,or_
from .home_forms import RepLookupForm
from ismightier_app import db
import numpy as np
from . import home
import requests
import json


# @home.after_request
# def add_security_headers(resp):
#     resp.headers['Content-Security-Policy']='default-src \'self\' fonts.gstatic.com *.googleapis.com kit.fontawesome.com'
#     return resp


@home.route('/', methods=['GET', 'POST'])
def homepage():
    form=RepLookupForm()
    lookupAddress='string'
    if form.validate_on_submit():
        session['lookupAddress'] = form.address.data
        return redirect(
            url_for('home.results')
        )
    return render_template(
        '/home/index.jhtml',
        form=form
    )

@home.route('/representatives')
def results():
    try:
        lookupAddress=session['lookupAddress']
#        session.pop('lookupAddress')
        civicKey = current_app.config['GOOGLE_CIVIC_INFORMATION_API_KEY']
        civicRoles = ['headOfState','headOfGovernment','deputyHeadOfGovernment','executiveCouncil','legislatorLowerBody','legislatorUpperBody','schoolBoard']
        civicPayload = {'key': civicKey,'roles': civicRoles,'address': lookupAddress}
        civicResponse = requests.get('https://www.googleapis.com/civicinfo/v2/representatives', params=civicPayload)
        if civicResponse.reason == 'OK':
            lookupState = civicResponse.json()['normalizedInput']['state']
            session['lookupState'] = lookupState
            repDF = RepNormal(civicResponse)
            repDF = GetFedRepInfo(repDF)
            columnList=list(repDF.columns)
            shortCols=[column for column in columnList if column not in ['name','party','title','fax_zero_url']]
            session['repDF']=repDF.to_dict(orient='tight')
            return render_template(
                '/home/representatives.jhtml',
                lookupAddress=lookupAddress,
                columnList=columnList,
                shortCols=shortCols,
                repDF=repDF
            )
        else:
            responseError = str(civicResponse.status_code) + ': ' + civicResponse.reason
            flash(f'Address search failed. Error {responseError}', category='red')
            return redirect(
        url_for('home.homepage')
    )
    except KeyError:
        return redirect(
        url_for('home.homepage')
    )

@home.route('/inspect-session')
def inspect_session():
    sessionDict=session
    print(sessionDict)
    return render_template(
    '/home/inspect_session.jhtml',
    sessionDict=sessionDict
    )

@home.route('/pop-session')
def pop_session():
    sessionDict=session
    keyList=[]                  # Attempting to use
    for key in sessionDict:     # "for key in sessionDict:
        keyList.append(key)     #     session.pop(key)"
    for key in keyList:         # breaks with "RuntimeError: dictionary changed size during iteration"
        session.pop(key)        # so store the dictionary keys to a list first and then iterate over the list, not the dictionary itself.
    return redirect(
        url_for('home.inspect_session')
        )

@home.route('/privacy-policy')
def privacy_policy():
    return render_template('home/privacy.jhtml')

@home.route('/about')
def about():
    return render_template('home/about.jhtml')
