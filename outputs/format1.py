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
filename = 'AAOPT2018.jl'
with json_lines.open(filename) as f:
    for item in f:
        temp = item.copy()
        temp.pop('details')
        temp.pop('author')
        author = item['author']
        lis = item['details'].split('|#|')
        print(lis)
        temp['year'] = lis[0].replace('Year:','').strip()
        temp['ProgramNumber'] = lis[1].replace('Program Number:','').strip()
        temp['ResourceType'] = lis[2].replace('Resource Type:','').strip()
        affli = lis[3].replace('Author Affiliation:','').strip()
        coauths = lis[4].replace('Co-Authors:','').strip()
        coaffli = lis[5].replace('Co-Author Affiliation:','').strip()
        temp['Room'] = lis[6].replace('Room:','').strip()
        #########
        temp1 = temp.copy()
        temp1['author'] = author
        temp1['affli'] = affli
        rows.append(temp1)
        if coauths != 'n/a':
            lis = coauths.split(',')
            aflis = coaffli.split(',')
            if len(lis) == len(aflis):
                i=0
                while i<len(lis):
                    temp2 = temp.copy()
                    temp2['author'] = lis[i]
                    temp2['affli'] = aflis[i]
                    rows.append(temp2)
                    i=i+1
            else:
                for a in lis:
                    temp2 = temp.copy()
                    temp2['author'] = a
                    temp2['affli'] = coaffli
                    rows.append(temp2)

df17 = pd.DataFrame(rows,columns=['author','affli','url','title','year','ProgramNumber','ResourceType','Room','text'])
print(df17.head())
writer = ExcelWriter('AAO 2018.xlsx')
df17.to_excel(writer,'Sheet1')
writer.save()

#print(rows)
