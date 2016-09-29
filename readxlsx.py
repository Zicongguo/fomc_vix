# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 07:05:54 2016

@author: henry
"""

import xlrd
from numpy import *
import operator
import datetime
path ='VXX.xlsx'

workbook = xlrd.open_workbook(path)
sheetname='VIX'
worksheet = workbook.sheet_by_name(sheetname)

# Change this depending on how many header rows are present
# Set to 0 if you want to include the header data.
offset = 0

rows = []
for i, row in enumerate(range(worksheet.nrows)):
    if i <= offset:  # (Optionally) skip headers
        continue
    r = []
    for j, col in enumerate(range(worksheet.ncols)):
        r.append(worksheet.cell_value(i, j))
    rows.append(r)

print('Got %d rows' % (len(rows) - offset))
print(rows[0])  # Print column headings
print(rows[offset])  # Print first data row sample

product=rows

if sheetname=="VXX":
    filtered1=[]
    tagged_art1=[]
    for i in product:
        if i[0] in dates:
            idx=dates.index(i[0])
            entry=[i[0],float(i[3])]
            if entry[1]>0:
                tagged_art1.append([arttrim[idx],'up',i[0]])
            elif entry[1]<=0:
                tagged_art1.append([arttrim[idx],'down',i[0]])
            filtered1.append(entry)
    tagged_art1=sorted(tagged_art1,key=lambda x: datetime.datetime.strptime(x[2], '%Y/%m/%d'))
    
    temp=[]
    for i in tagged_art1:
        temp.append(list(i[0:2]))
    tagged_art1=temp 
    Date_sorted1=sorted(dates,key=lambda x: datetime.datetime.strptime(x, '%Y/%m/%d'))

else:
    filtered=[]
    jump=[]
    tagged_art=[]
    for i in product:
        if i[0] in dates:
            idx=dates.index(i[0])
            entry=[i[0],float(i[3])]
            if entry[1]>0:
                tagged_art.append([arttrim[idx],'up',i[0]])
            elif entry[1]<=0:
                tagged_art.append([arttrim[idx],'down',i[0]])
            filtered.append(entry)
            jump.append(abs(float(i[3])))
    tagged_art=sorted(tagged_art,key=lambda x: datetime.datetime.strptime(x[2], '%Y/%m/%d'))
    
    temp=[]
    for i in tagged_art:
        temp.append(list(i[0:2]))
    tagged_art=temp 
    Date_sorted=sorted(dates,key=lambda x: datetime.datetime.strptime(x, '%Y/%m/%d'))





