# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 18:33:15 2018

@author: pgood
"""



def get_sd(date):
    from datetime import datetime, timedelta
    import requests
    from datetime import datetime, timedelta
    import pandas as pd
    import numpy as np
    
    end = date.date()
    
    start = (date.date() - timedelta(days = 200))
    
    url = 'https://api.gdax.com/products/BTC-USD/candles?start={}&end={}&granularity=86400'.format(start,end)
    obj = requests.get(url).json()
    print(url)
    df = pd.DataFrame(obj, columns = ['time', 'low', 'high', 'open', 'close', 'volume'])   
    df['prev'] = df.close.shift(1)
    df['change'] = df.close/df.prev - 1
    return np.std(df.change.values[1:])*np.sqrt(365)

def insert_sds():
    from pymongo import MongoClient
    from datetime import datetime, timedelta
    import time
    
    connection = MongoClient('ds149279.mlab.com', 49279)
    db = connection['data602final']
    db.authenticate('me', 'mypass')
    
    
    #get most recent sd in collection
    for item in db.sds.aggregate([{ '$group' : { '_id': 'null', 'max': { '$max' : "$date" }}}]):
        max_date = item['max']
        

    standard_devs = []
    for i in range(1, (datetime.today() - max_date).days):
        date = max_date + timedelta(days = i)
        standard_devs.append({'date': date, 'sd': get_sd(date)})
        time.sleep(.5)
    if standard_devs:
        db.sds.insert_many(standard_devs)
    return