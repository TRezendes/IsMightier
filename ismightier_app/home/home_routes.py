from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from .home_funcs import AddBgID,GetBgID,RepNormal
from ismightier_app.models import USCongressTbl
from wtforms.validators import ValidationError
from .home_forms import RepLookupForm
from ismightier_app import db
from . import home
import requests
import json


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
        '/home/index.html',
        form=form)

@home.route('/representatives')
def results():
    if session['lookupAddress']:
        civicKey = current_app.config['GOOGLE_CIVIC_INFORMATION_API_KEY']
        civicRoles = ['headOfState','headOfGovernment','deputyHeadOfGovernment','executiveCouncil','legislatorLowerBody','legislatorUpperBody','schoolBoard']
        civicPayload = {'key': civicKey,'roles': civicRoles,'address': session['lookupAddress']}
        session.pop('lookupAddress')
        civicResponse = requests.get('https://www.googleapis.com/civicinfo/v2/representatives', params=civicPayload)
        if civicResponse.reason == 'OK':
            repDF = RepNormal(civicResponse)
            IDdict = GetBgID(repDF)
            repDF = AddBgID(repDF,IDdict)


            '''
            rowsWritten = 0
            repDF = RepNormal(civicResponse)
            try:
                rowsWritten,tempTableName = RepDFSave(repDF)
            except ValueError:
                flash(f'The application attempted to create a table that already exists. No data was written to the database. Please try again.', category='red')
            if rowsWritten > 0:
                session['tempTable']=tempTableName
                return render_template(
                    '/home/representatives.html',
                    repDict=representativeDictionary
                    )
            '''
#            db.session.execute(db.select(UserInfoTbl.home_is_landing).filter_by(display_name=playerName)).scalar():
            
        else:
            responseError = str(civicResponse.status_code) + ': ' + civicResponse.reason
            flash(f'Address search failed. Error {responseError}', category='red')
    return redirect(
        url_for('home.homepage')
    )



# https://www.googleapis.com/civicinfo/v2/representatives?key=[API-KEY]&address=1035+wabank+st,+lancaster,+pa+17603&roles=headOfState&roles=headOfGovernment&roles=deputyHeadOfGovernment&roles=executiveCouncil&roles=legislatorLowerBody&roles=legislatorUpperBody&roles=schoolBoard





bioGuideIDs['name']=db.session.execute(db.select(USCongressTbl.bioguide_id).filter_by(or_(and_((USCongressTbl.first_name==splits[0]),USCongressTbl.last_name==splits[1]),and_((USCongressTbl.nickname==splits[0]),USCongressTbl.last_name==splits[1]))))


