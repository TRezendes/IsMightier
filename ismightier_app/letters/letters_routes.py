from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from ismightier_app.models import USCongressTbl
from wtforms.validators import ValidationError
from sqlalchemy import and_,create_engine,or_
import pandas as pd
#from .letters_forms import 
from ismightier_app import db
from . import letters
import requests
import json


@letters.route('/<name>', methods=['GET', 'POST'])
def rep_info(name):
    repDF=session['repDF']
    repDF=pd.DataFrame.from_dict(repDF, orient='tight')
    namedRep=repDF.loc[repDF['name'] == name]
    fieldList=[]
    addressList=[]
    lookupState=session['lookupState']
    for col in namedRep.columns:
        try: 
            if col.split('.')[1] in ['city','state','zip','line1','line2']:
                addressList.append(col)
        except:
            pass
        if col not in ['bioguide_id','fax_number','fax_zero_url','name','title'] and col not in addressList:
            fieldList.append(col)
    return render_template(
        '/letters/rep-info.html',
        namedRep=namedRep,
        fieldList=fieldList,
        addressList=addressList,
        lookupState=lookupState
    )

@letters.route('/letter')
def letter():
    return render_template(
        '/letters/letter.html'
    )
