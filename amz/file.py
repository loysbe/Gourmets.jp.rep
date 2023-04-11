from calendar import monthrange
from datetime import datetime
import os

reportYear = '2020'
dirPath = 'C:\\Users\\Loys\\Downloads\\'
outFile = dirPath + 'rak-' + reportYear + '.csv'

f = open(outFile,'w',encoding='shift-jis')

for m in range(1,13):
    fromDate =  reportYear + '-' + str(m).zfill(2) + '-01'
    days = monthrange(int(reportYear),int(m))
    toDate = reportYear + '-' + str(m).zfill(2) +  '-' + str(days[1]).zfill(2)
    fileName = dirPath + 'rak-' + fromDate + '-' + toDate + '.csv'
    g = open(fileName, 'r',encoding='shift-jis')
    contenu = g.readlines()
    g.close()
    for s in contenu:
        f.write("%s\n" % s)