import requests
from bs4 import BeautifulSoup
import re

url = "https://ktis.kookmin.ac.kr"


def parseInfo(st_id, st_passwd):
    ses = requests.session()
    res = ses.post(url + "/kmu/com.Login.do?", data={'txt_user_id': st_id, 'txt_passwd': st_passwd})

    idx = res.text.find("msg")
    idx_end = res.text.find("';", idx)

    keys = ['user_id', 'name', 'ssn', 'college', 'school', 'time', 'major', 'date', 'status', 'grade']

    if idx == -1:
        res = ses.post(url + "/kmu/usa.Usa0209eFGet01.do", data={'ServiceID': st_id, 'pFolder': '학적시스템'})
        bs = BeautifulSoup(res.text, "lxml")
        td_content = bs.find_all('td', 'table_bg_white')
        default_info = {}

        td_content = map(lambda content: re.split(r"<*>", content.get_text())[-1].strip(), td_content)
        td_content = [x for x in td_content if x]

        for idx in range(10):
            if idx >= len(td_content):
                break
            key = keys[idx]
            value = td_content[idx]
            if td_content != '':
                default_info[key] = value

        default_info['password'] = st_passwd
        return {'status': True, 'content': default_info}

    else:
        return {'status': False, 'content': res.text[idx + 7:idx_end]}


def parseSimpleGrade(st_id, st_passwd):
    ses = requests.session()
    res = ses.post(url + "/kmu/com.Login.do?", data={'txt_user_id': st_id, 'txt_passwd': st_passwd})
    idx = res.text.find("msg")
    idx_end = res.text.find("';", idx)
    keys = ['year', 'apply_grade', 'get_grade', 'avg', 'gpa', 'score', 'rank', 'warning', 'f_subject', 're_subject']

    if idx == -1:
        res = ses.post(url + '/kmu/usc.Usc0601qAGet01.do', data={'ServiceID': st_id})
        bs = BeautifulSoup(res.text, "lxml")
        info = bs.find_all('td', 'table_bg_white')
        simple_grade = bs.find_all('tr', 'table_bg_white')
        simple_total_grade = bs.find_all('td', 'table_color_bright')
        try:
            simple_total_grade = map(lambda content: float(re.split(r"<*>", content.get_text())[-1].strip()),
                                     simple_total_grade[21:26])
            total = {}

            for idx, data in enumerate(simple_total_grade):
                total[keys[idx + 1]] = data

            info = map(lambda content: re.split(r"<*>", content.get_text())[-1].strip(), info)
            info = [x for x in info if x][:-2]
            info_keys = ['user_id', 'name', 'grade', 'college', 'school', 'major', 'second_major', 'third_major']

            ret_info = {}
            for idx, data in enumerate(info):
                ret_info[info_keys[idx]] = data
            simple_grade = map(lambda d: BeautifulSoup(str(d), 'lxml').find_all('td'), simple_grade)

            grades = []
            for idx, data in enumerate(simple_grade):
                onclick = re.split(r"'*'", data[0].get('onclick'))
                grade = {"txt_year": onclick[1], "txt_smt": onclick[3]}
                for idx, key in enumerate(keys):
                    grade[key] = re.split(r"<*>", data[idx].get_text())[-1].strip()
                grades.append(grade)

            return {'status': True, 'content': {'total': total, 'info': ret_info, 'grades': grades}}

        except Exception as e:
            return {'status': False, 'content': str(e)}


def parseDetailGrade(st_id, st_passwd, txt_year, txt_smt):
    ses = requests.session()
    res = ses.post(url + "/kmu/com.Login.do?", data={'txt_user_id': st_id, 'txt_passwd': st_passwd})
    idx = res.text.find("msg")
    idx_end = res.text.find("';", idx)
    keys = ['code', 'subject_name', 'kind', 'credit', 'tear', 'grade_score', 'semi', 'second_semi', 'third_semi',
            'connect_semi', 'manner', 'score']

    if idx == -1:
        res = ses.post(url + '/kmu/usc.Usc0601qAGet01_1.do', data={'arg_student_cd': st_id, "txt_year": 2017,
                                                                   "txt_smt": 10})
        bs = BeautifulSoup(res.text, "lxml")
        grades = bs.find_all('td', 'table_bg_white')
        grades = list(map(lambda content: re.split(r"<*>", content.get_text())[-1].strip(), grades))

        info_keys = ['user_id', 'name', 'grade', 'college', 'school', 'major', 'second_major', 'third_major']
        info = [x for x in grades[:10] if x]
        ret_info = {}
        for idx, data in enumerate(info):
            ret_info[info_keys[idx]] = data

        ret_grades = []
        grades = grades[11:]
        grade = {}
        for idx, data in enumerate(grades):

            if idx % len(keys) == 0 and idx != 0:
                ret_grades.append(grade)
            else:
                grade[keys[idx % len(keys)]] = data
        return {'status': True, 'content': { 'info': ret_info, 'grades': ret_grades}}

# print(parseInfo(id, pwd))
# print(parseSimpleGrade(id, pwd))
# print(parseDetailGrade(id, pwd, 2017, 10))
