import requests
from bs4 import BeautifulSoup
import re

url = "https://ktis.kookmin.ac.kr"

def parseInfoFromKTIS(st_id,st_passwd):
    ses = requests.session()
    res = ses.post(url + "/kmu/com.Login.do?",data={'txt_user_id':st_id,'txt_passwd':st_passwd})

    idx = res.text.find("msg")
    idx_end = res.text.find("';", idx)

    keys = ['user_id','name','ssn','college','school','time','major','date','status','grade']

    if idx == -1:
        res = ses.post(url+"/kmu/usa.Usa0209eFGet01.do",data={'ServiceID':st_id,'pFolder':'학적시스템'})
        bs = BeautifulSoup(res.text,"html5lib")
        td_content = bs.find_all('td','table_bg_white')
        default_info = {}

        for idx in range(len(td_content)):
            td_content[idx] = re.split(r"<*>", td_content[idx].get_text())[-1].strip()

        td_content = [x for x in td_content if x]

        for idx in range(10):
            if idx >= len(td_content):
                break
            key = keys[idx]
            value = td_content[idx]
            if td_content != '':
                 default_info[key] = value
        default_info['passwd'] = st_passwd
        return {'status':True,'content':default_info}

    else :
        return  {'status':False,'content':res.text[idx+7:idx_end]}






