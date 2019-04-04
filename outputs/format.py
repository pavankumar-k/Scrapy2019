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
filename = sys.argv[1]
with json_lines.open(filename+'.jl') as f:
    for item in f:
        row={}
        temp = item.copy()
        temp.pop('auth')
        temp.pop('affli')
        al = re.split(',(?![0-9])',item['auth'].replace('\n',''))
        afl = re.split(r', (?=[0-9])',item['affli'].replace('\n',''))
        s = re.findall(r'[0-9]+',item['auth'])
        if s:
            for a in al:
                print(a)
                nums = re.findall('[0-9]+',a)
                a = re.sub(r'[0-9]+','',a).replace(',','')
                row = temp.copy()
                row['auth']=a
                row['affli'] = ''
                print(nums)
                for n in nums:
                    for aff in afl:
                        if n in re.findall(r'[0-9]+',aff):
                            row['affli']+=re.sub(r'[0-9]+','',aff)+'; '
                print(row['affli'])
                rows.append(row)
        else:
            for a in al:
                row = temp.copy()
                row['auth'] = a
                row['affli']=item['affli'].replace('\n','')
                rows.append(row)
        
        
        
df17 = pd.DataFrame(rows,columns=['auth','affli','url','title','data'])
print(df17.head())
writer = ExcelWriter(filename+'.xlsx')
df17.to_excel(writer,'Sheet1')
writer.save()

#print(rows)
