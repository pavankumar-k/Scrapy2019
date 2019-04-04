#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:47:52 2018

@author: pavan
"""
import sys
import json_lines
import pandas as pd
#from geotext import GeoText
from pandas import ExcelWriter
import re

'''
def isloc(loc):
    place = GeoText(loc)
    if len(place.cities)>0:
        return True
    return False
'''
rows = []
filename = 'ESMOWCGC18'
with json_lines.open(filename+'.jl') as f:
    for item in f:
        temp = item.copy()
        t = item['author'].split('Author Affiliations/')
        #temp['affli'] = t[1].strip()
        temp['topics'] = item['topics'].replace(';Topics;;;','').replace(';;',';')
        li = t[0].replace('Authors','').split(',')
        for a in li:
            row = temp.copy()
            print(row['text'])
            row['author']=a.strip()
            rows.append(row)
        
        
        
df17 = pd.DataFrame(rows,columns=['author','url','title','date','session','event','topics'])
print(df17.head())
writer = ExcelWriter(filename+'.xlsx')
df17.to_excel(writer,'Sheet1')
writer.save()

#print(rows)
