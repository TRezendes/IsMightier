from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from ismightier_app.models import LetterPartTbl
from wtforms.validators import ValidationError
## WeasyPrint does not work under Windows 10. Stupid Windows. ##
#from flask_weasyprint import HTML, render_pdf   
from sqlalchemy import and_,create_engine,or_
from numpy.random import randint
from .letters_forms import LetterOptionsForm
from ismightier_app import db
from . import letters
import pandas as pd
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

    ########## This section for included template. For iFrame, remove this section and use separate route. #####
    letterType=randint(3)
    if letterType==0:
        selectors=['whole']
    elif letterType==1:
        selectors=['intro','middle','conclusion']
    elif letterType==2:
        selectors=['intro','middle1','middle2','conclusion']
    letterDict={}
    for selector in selectors:
        partDict={}
        records=db.session.execute(db.select(LetterPartTbl).where(LetterPartTbl.part_placement==selector)).scalars().all()
        numRecords=len(records)
        randIndex=randint(numRecords)
        partText=records[randIndex].part_text
        partColor=records[randIndex].color
        partDict['text']=partText
        partDict['color']=partColor + '50'
        letterDict[selector]=partDict
    if 'Senator' in namedRep.iloc[0]['title']:
        salutationTitle='Senator'
    elif 'Representative' in namedRep.iloc[0]['title']:
        salutationTitle='Representative'
    elif 'Vice President' in namedRep.iloc[0]['title']:
        salutationTitle='Vice President'
    elif 'President' in namedRep.iloc[0]['title']:
        salutationTitle='President'
    elif 'Lieutenant Governor' in namedRep.iloc[0]['title']:
        salutationTitle='Lieutenant Governor'
    elif 'Governor' in namedRep.iloc[0]['title']:
        salutationTitle='Governor'
    elif 'Commissioner' in namedRep.iloc[0]['title']:
        salutationTitle='Commissioner'
    elif 'Mayor' in namedRep.iloc[0]['title']:
        salutationTitle='Mayor'
    else:
        salutationTitle=None
    salutationName=namedRep.iloc[0]['name'].split(' ')[-1]
    lookupAddress=session['lookupAddress']
    ##################################################

    return render_template(
        '/letters/rep-info.html',
        namedRep=namedRep,
        fieldList=fieldList,
        addressList=addressList,
        lookupState=lookupState,
        ###########
        selectors=selectors,
        letterDict=letterDict,
        salutationTitle=salutationTitle,
        salutationName=salutationName,
        lookupAddress=lookupAddress
        ###########
    )



@letters.route('/letter')
def letter():
    letterType=randint(3)
    if letterType==0:
        selectors=['whole']
    elif letterType==1:
        selectors=['intro','middle','conclusion']
    elif letterType==2:
        selectors=['intro','middle1','middle2','conclusion']
    letterDict={}
    for selector in selectors:
        partDict={}
        records=db.session.execute(db.select(LetterPartTbl).where(LetterPartTbl.part_placement==selector)).scalars().all()
        numRecords=len(records)
        randIndex=randint(numRecords)
        partText=records[randIndex].part_text
        partColor=records[randIndex].color
        partDict['text']=partText
        partDict['color']=partColor + '50'
        letterDict[selector]=partDict
    return render_template(
        '/letters/letter.html',
        selectors=selectors,
        letterDict=letterDict
    )

@letters.route('<name>/pdf')
def pdf_print(name):
    html = render_template('/letters/letter.html')
    return render_pdf(HTML(string=html))
