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
    print(namedRep)
    return render_template(
        '/letters/rep-info.html'
    )
