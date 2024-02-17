from ismightier_app.models import LetterPartTbl
from sqlalchemy import and_, create_engine, or_
from numpy.random import randint
from ismightier_app import db
from flask import current_app
from uuid import uuid4
import pandas as pd
import numpy as np
import requests
import json
import os


def BuildLetter(namedRep: pd.core.frame.DataFrame, address: str) -> str:
    ## Randomly determine how the letter will be built
    #letterType=randint(3)
    letterType=0 # Let's just use whole letters for now (7/28/23)
    if letterType==0:
        selectors=['whole']
    elif letterType==1:
        selectors=['intro','middle','conclusion']
    elif letterType==2:
        selectors=['intro','middle1','middle2','conclusion']
    letterDict={}
    ## For each piece of the letter required, select all matching pieces from the database and select one at random
    for selector in selectors:
        partDict={}
        records=db.session.execute(db.select(LetterPartTbl).where(LetterPartTbl.part_placement==selector)).scalars().all()
        numRecords=len(records)
        randIndex=randint(numRecords)
        partText=records[randIndex].part_text
        letterDict[selector]=partText
    ## Set salutationTitle based on the role of the representative addressee
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
    ## Set salutationName equal to the representative addressee's last name
    letterDict['salutationName']=namedRep.iloc[0]['name'].split(' ')[-1]
##### If the function builds the letter text, then storing the lookup address in the dictionary isn't necessary ####
    letterDict['address']=address
    ## Build the text of the letter from the parts saved in letterDict
    if letterDict['salutationTitle']:
        addressee=f"{letterDict['salutationTitle']} {letterDict['salutationName']}"
    else:
        addressee=f"{letterDict['salutationName']}"
    salutation=f"Dear {addressee},"
    parabreak=f'{os.linesep}{os.linesep}    '
    letterDefaultText=f"""[Your Name Here]{os.linesep}{address}{os.linesep}{os.linesep}{salutation}{parabreak}{parabreak.join({f'{letterDict[selector]}' for selector in selectors})}{os.linesep}{os.linesep}Sincerely,{os.linesep}[Your Name Here]"""
    print(letterDict)


    return letterDefaultText



