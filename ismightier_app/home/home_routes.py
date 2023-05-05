from .home_forms import RepLookupForm
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
#from ismightier_app.models 
from ismightier_app import db
from wtforms.validators import ValidationError
import requests
import json
from . import home



def GetRepDict(civicResponse):
    repJSON = civicResponse.json()
    indexDict = {}
    repDict = {}
    for unit in repJSON['offices']:
        indexDict[unit['name']]=unit['officialIndices']
    for key in indexDict:
        repList=[]
        for i in range(len(indexDict[key])):
            repList.append(repJSON['officials'][indexDict[key][i]])
        repDict[key]=repList
    return repDict

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
        representativeDictionary=GetRepDict(civicResponse)
        return render_template(
            '/home/representatives.html',
            repDict=representativeDictionary
            )
    return redirect(
        url_for('home.homepage')
    )



# https://www.googleapis.com/civicinfo/v2/representatives?key=AIzaSyBvRsxkN-1OgK4BcQMgcH7dnVdDAOsUwYo&address=1035+wabank+st,+lancaster,+pa+17603&roles=headOfState&roles=headOfGovernment&roles=deputyHeadOfGovernment&roles=executiveCouncil&roles=legislatorLowerBody&roles=legislatorUpperBody&roles=schoolBoard
