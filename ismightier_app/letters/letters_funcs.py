from ismightier_app.models import USCongressTbl,LetterPartTbl,RepresentativeSentimentTbl,SentimentLevelTbl,FederalSponsorTbl,StateSponsorTbl
from sqlalchemy import and_,create_engine,or_
from ismightier_app import db
from flask import current_app
from uuid import uuid4
import pandas as pd
import numpy as np
import requests
import json


def BuildLetter(namedRep: pandas.core.frame.DataFrame, address: string) -> dict:
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
        partDict[selector]=partText
        letterDict['parts']=partDict
    if 'Senator' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='Senator'
    elif 'Representative' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='Representative'
    elif 'Vice President' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='Vice President'
    elif 'President' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='President'
    elif 'Lieutenant Governor' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='Lieutenant Governor'
    elif 'Governor' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='Governor'
    elif 'Commissioner' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='Commissioner'
    elif 'Mayor' in namedRep.iloc[0]['title']:
        letterDict['salutationTitle']='Mayor'
    else:
        letterDict['salutationTitle']=None
    letterDict['salutationName']=namedRep.iloc[0]['name'].split(' ')[-1]
    letterDict['address']=address
    return letterDict
