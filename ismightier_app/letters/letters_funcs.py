from ismightier_app.models import USCongressTbl,LetterPartTbl,RepresentativeSentimentTbl,SentimentLevelTbl,FederalSponsorTbl,StateSponsorTbl
from sqlalchemy import and_,create_engine,or_
from ismightier_app import db
from flask import current_app
from uuid import uuid4
import pandas as pd
import numpy as np
import requests
import json


def BuildLetter():
    