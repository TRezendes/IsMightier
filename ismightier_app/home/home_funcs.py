from ismightier_app.models import USCongressTbl
from sqlalchemy import and_,create_engine,or_
from ismightier_app import db
from flask import current_app
from uuid import uuid4
import pandas as pd
import numpy as np
import requests
import json


def RepNormal(response):
    repJSON=response.json()
    indexDict={}
    repList=[]
    keysToKeep=['address','name','party','phones','title','urls']
    for unit in repJSON['offices']:
        indexDict[unit['name']]=unit['officialIndices']
    for idKey in indexDict:
        for i in range(len(indexDict[idKey])):
            officialDict=repJSON['officials'][indexDict[idKey][i]]
            officialDict['title']=idKey
            oDkeyLs=list(officialDict.keys())
            for j in range(len(oDkeyLs)):
                if oDkeyLs[j] not in keysToKeep:
                    del officialDict[oDkeyLs[j]]
            repList.append(officialDict)
    for l in range(len(repList)):
        for rlKey in list(repList[l].keys()):
            if type(repList[l][rlKey]) is list:
                for m in range(len(repList[l][rlKey])):
                    repList[l][rlKey + '_' + str(m+1)]=repList[l][rlKey][m]
                del repList[l][rlKey]
    repDF=pd.json_normalize(repList)
    columns=list(repDF.columns)
    columns.append('bioguide_id')
    columns.append('fax_number')
    columns.append('fax_zero_url')
    repDF=repDF.reindex(columns=columns)
    return repDF

def AddFedRepInfo(df,IDdict,numDict,URLdict):
    for i, row in df.iterrows():
        name=row['name']
        if name in IDdict:
            df.loc[i:i,('bioguide_id')]=IDdict[name]#['bioguide_id'][i]=IDdict[name]
        else:
            df.loc[i:i,('bioguide_id')]=None#['bioguide_id'][i]=None
        if name in numDict:
            df.loc[i:i,('fax_number')]=numDict[name]#['fax_number'][i]=numDict[name]
        else:
            df.loc[i:i,('fax_number')]=None#['fax_number'][i]=None
        if name in URLdict:
            df.loc[i:i,('fax_zero_url')]=URLdict[name]#['fax_zero_url'][i]=URLdict[name]
        else:
            df.loc[i:i,('fax_zero_url')]=None#['fax_zero_url'][i]=None
    return df

def GetFedRepInfo(df):
    repsToGet = []
    for index, row in df.iterrows():
        if 'U.S. ' in row['title']:
            repsToGet.append(row['name'])
    bioGuideIDs={}
    faxNumbers={}
    faxURLs={}
    bgID=None
    faxNum=None
    faxURL=None
    for name in repsToGet:
        obj=None
        row=None

        # All of the print statements are debug nonsense. Remove them once you solve it. \/ \/ \/ \/ \/ \/ \/ \/
        print(name)
        splits=name.split(' ')
        obj=db.session.execute(db.select(USCongressTbl).where(or_(and_(USCongressTbl.first_name==splits[0],USCongressTbl.last_name==splits[1]),and_((USCongressTbl.nickname==splits[0]),USCongressTbl.last_name==splits[1])))).scalars()
        print(obj)
        for row in obj:
            bgID=None
            faxNum=None
            faxURL=None
            print(name)
            print(row.bioguide_id)
            print(row.fax_number)
            print(row.fax_zero_url)
            print(row,'\n')

            # All of the print statements are debug nonsense. Remove them once you solve it. /\ /\ /\ /\ /\ /\ /\ /\
            bgID=row.bioguide_id
            faxNum=row.fax_number
            faxURL=row.fax_zero_url
        if bgID:
            bioGuideIDs[name]=bgID
        if faxNum:
            faxNumbers[name]=faxNum
        if faxURL:
            faxURLs[name]=faxURL
    AddFedRepInfo(df,bioGuideIDs,faxNumbers,faxURLs)
    df=df.where(df.notnull(),None)
    return df
