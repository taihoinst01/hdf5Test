import sys
from DomainDictionaryTrans import DomainDicTrans

#도메인 사전 번역
ddt = DomainDicTrans()
str = "DYNAPRO ATM RF10"

str = str.encode('euc_kr','replace')
str = str.decode('euc_kr')
print(ddt.lookup(str.split()))