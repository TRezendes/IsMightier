from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from ismightier_app.models import LetterPartTbl, SentimentLevelTbl
from wtforms.validators import ValidationError
from flask_weasyprint import HTML, render_pdf
from sqlalchemy import and_, create_engine, or_
from .letters_forms import LetterOptionsForm, PersonalForm
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
#     if form.validate_on_submit():
#
#
#         text=form.letter_text.data
#         html=render_template(
#             '/letters/letter-pdf.jhtml',
#             text=text
#         )
#         return render_pdf(HTML(string=html))



    name_form=PersonalForm()
    for col in namedRep.columns:
        try:
            if col.split('.')[1] in ['city','state','zip','line1','line2']:
                addressList.append(col)
        except:
            pass
        if col not in ['bioguide_id','fax_number','fax_zero_url','name','title'] and col not in addressList:
            fieldList.append(col)
    if name_form.validate_on_submit():
        included_template='letter'
    else:
        included_template='form'
    ########## This section for included template. For iFrame, remove this section and use separate route. #####
    if form.recipient_sentiment.data:
        recip_sent=form.recipient_sentiment.data
    else:
        recip_sent=default_sentiment
    if name_form.sender_name.data:
        sender_name=name_form.sender_name.data
    else:
        sender_name='[Your Name Here]'
    letterDefaultText=BuildLetter(namedRep, lookupAddress, sender_name, recip_sent)
    session['letter_text']=letterDefaultText
    ##################################################
    form.letter_text.data=letterDefaultText
    return render_template(
        '/letters/rep-info.jhtml',
        name=name,
        form=form,
        namedRep=namedRep,
        fieldList=fieldList,
        name_form=name_form,
        addressList=addressList,
        lookupState=lookupState,
        default_sentiment=default_sentiment,
        included_template=included_template,
        ###########
        #letterDict=letterDict,
        letterDefaultText=letterDefaultText
        ###########
    )

@letters.route('/letter-pdf')
def pdf_html():
    text=session['letter_text']
    return render_template(
        '/letters/letter-pdf.jhtml',
        text=text
    )

@letters.route('/pdf')
def pdf_print(letter_text):
    text=form.letter_text.data
    html=render_template(
        '/letters/letter-pdf.jhtml',
        text=text
    )
    return render_pdf(HTML(string=html))

