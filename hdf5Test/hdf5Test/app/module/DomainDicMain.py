import sys
from .DomainDictionaryTrans import DomainDicTrans

#도메인 사전 번역

def run(sentence):
    ddt = DomainDicTrans()
    str = sentence

    str = str.encode('euc_kr','replace')
    str = str.decode('euc_kr')
    return ddt.lookup(str.split())