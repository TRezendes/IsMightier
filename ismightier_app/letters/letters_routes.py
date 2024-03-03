from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from ismightier_app.models import LetterPartTbl, SentimentLevelTbl
from wtforms.validators import ValidationError
from flask_weasyprint import HTML, render_pdf
from sqlalchemy import and_, create_engine, or_
from .letters_forms import LetterOptionsForm
from .letters_funcs import BuildLetter
from numpy.random import randint
from ismightier_app import db
from . import letters
import pandas as pd
import requests
import json


# @letters.after_request
# def add_security_headers(resp):
#     resp.headers['Content-Security-Policy']='default-src \'self\' fonts.gstatic.com *.googleapis.com kit.fontawesome.com'
#     return resp

@letters.route('/<name>', methods=['GET', 'POST'])
def rep_info(name):
    name=name
    repDF=session['repDF']
    repDF=pd.DataFrame.from_dict(repDF, orient='tight')
    repDF=repDF.replace({float("NaN"): None})
    namedRep=repDF.loc[repDF['name'] == name]
    # This section regards trans rights specifically, and makes the simple (and fairly naive) assumption that democrats support and republicans oppose. I intend to implement much more robust logic in this regard in the future, but for now I am working toward a minimum viable product.
    print(namedRep)
    if namedRep.iloc[0]['party'] == 'Democratic Party':
        default_sentiment=1
    elif namedRep.iloc[0]['party'] == 'Republican Party':
        default_sentiment=-1
    else:
        default_sentiment=0
    fieldList=[]
    addressList=[]
    lookupState=session['lookupState']
    lookupAddress=session['lookupAddress']
    form=LetterOptionsForm()
    for col in namedRep.columns:
        try:
            if col.split('.')[1] in ['city','state','zip','line1','line2']:
                addressList.append(col)
        except:
            pass
        if col not in ['bioguide_id','fax_number','fax_zero_url','name','title'] and col not in addressList:
            fieldList.append(col)

    ########## This section for included template. For iFrame, remove this section and use separate route. #####
    if form.recipient_sentiment.data:
        recip_sent=form.recipient_sentiment.data
    else:
        recip_sent=default_sentiment
    letterDefaultText=BuildLetter(namedRep, lookupAddress, recip_sent)
    session['letter_text']=letterDefaultText
    ##################################################
    form=LetterOptionsForm(default_value=letterDefaultText)
    return render_template(
        '/letters/rep-info.jhtml',
        name=name,
        form=form,
        namedRep=namedRep,
        fieldList=fieldList,
        addressList=addressList,
        lookupState=lookupState,
        default_sentiment=default_sentiment,
        ###########
        #letterDict=letterDict,
        letterDefaultText=letterDefaultText
        ###########
    )

@letters.route('/letter')
def letter():
    form=LetterOptionsForm()
    form.recipient_sentiment.data=0
    submit_worked='Nope!'
    if form.validate_on_submit():
        submit_worked='Yep!'
        return redirect(
        url_for('letters.letter')
    )
    return render_template(
        '/letters/construction-form.jhtml',
        form=form,
        submit_worked=submit_worked
    )


@letters.route('/letter-pdf')
def pdf_html():
    text=session['letter_text']
    return render_template(
        '/letters/letter-pdf.jhtml',
        text=text
    )

@letters.route('/pdf')
def pdf_print():
    text=session['letter_text']
    html=render_template(
        '/letters/letter.jhtml'
    )
    print(text)
    return render_pdf(HTML(string=html))

