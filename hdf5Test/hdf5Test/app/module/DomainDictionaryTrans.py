import numpy as np
import os
import sys
import re
import json
import cx_Oracle

id = "ocr"
pw = "taiho123"
sid = "ocrservice"
# ip = "10.10.20.205"
ip = "192.168.0.251"
port = "1521"
connInfo = id + "/" + pw + "@" + ip + ":" + port + "/" + sid

conn = cx_Oracle.connect(connInfo, encoding="UTF-8", nencoding="UTF-8")
curs = conn.cursor()

class DomainDicTrans():
    def lookup(self, phrase):
        originword = ''
        frontword = ''
        rearword = ''
        returnsentence = ''
        sql = "SELECT CORRECTEDWORDS FROM TBL_OCR_DOMAIN_DIC_TRANS WHERE ORIGINWORD = :orign AND FRONTWORD = :front  AND REARWORD = :rear"
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

            params = [originword, frontword, rearword]
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
