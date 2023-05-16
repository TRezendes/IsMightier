from ismightier_app.models import USCongressTbl
from sqlalchemy import and_,create_engine,or_
from flask import current_app, db
from uuid import uuid4
import pandas as pd
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
    return repDF


'''
def RepDFSave(repDF):
    tempTableName='#'+str(uuid4()).replace('-','')
    engine=create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    rowsWritten=repDF.to_sql(tempTableName,engine)
    return rowsWritten, tempTableName
'''
def GetBgID(df):
    bioGuidesToGet = []
    for index, row in df.iterrows():
        if 'U.S. ' in row['title']:
            bioGuidesToGet.append(row['name'])
    bioGuideIDs={}
    for name in bioGuidesToGet:
        splits=name.split(' ')
        obj=db.session.execute(db.select(USCongressTbl.bioguide_id).where(or_(and_((USCongressTbl.first_name==splits[0]),USCongressTbl.last_name==splits[1]),and_((USCongressTbl.nickname==splits[0]),USCongressTbl.last_name==splits[1]))))
        for row in obj:
            bgID=row.bioguide_id
        bioGuideIDs[name]=bgID
    return bioGuideIDs


def AddBgID(df,IDdict):
    for i, row in df.iterrows():
        name=row['name']
        if name in IDdict:
            df['bioguide_id'][i]=IDdict[name]
        else:
            df['bioguide_id'][i]=None
    return df
