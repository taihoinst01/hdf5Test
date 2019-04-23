import numpy as np
import os
import sys
import re
import json
import psycopg2 as pg2 #DB연동

DB_CONN_INFO = "host=192.168.0.183 dbname=crawler user=taihoinst password=taiho123 port=5432";

conn = pg2.connect(DB_CONN_INFO)
curs = conn.cursor()

class DomainDicTrans():
    def lookup(self, phrase):
        originword = ''
        frontword = ''
        rearword = ''
        returnsentence = ''
        sql = 'SELECT CORRECTEDWORDS FROM public."TBL_CRAWLER_DOMAIN_DIC_TRANS" WHERE ORIGINWORD = %s AND FRONTWORD = %s  AND REARWORD = %s'
        for i in range(len(phrase)):
            if i == 0:
                frontword = '<<N>>'
            else:
                frontword = phrase[i-1]
            if i == len(phrase) - 1:
                rearword = '<<N>>'
            else:
                rearword = phrase[i+1]
            originword = phrase[i]

            params = (originword, frontword, rearword)
            #print(dbConnection.selectDDT(sql, params).get('CORRECTEDWORDS'))

            if (returnsentence != ''):
                returnsentence = returnsentence + ' '
            curs.execute(sql, params)
            corretedwords = curs.fetchall()
            if (len(corretedwords) > 0):
                if (corretedwords[0][0] == '<<N>>'):
                    returnsentence = returnsentence[0:-1]
                else:
                    returnsentence = returnsentence + corretedwords[0][0]
            else:
                returnsentence = returnsentence + originword

        return returnsentence
