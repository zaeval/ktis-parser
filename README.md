# ktis-parser

This is parser of default information of "ktis.kookmin.ac.kr" with student-number & password

## How 2 use

```
pip3 install ktis-parser
```

or

```
pip install ktis-parser
```

after then

```python
from ktis_parser.ktis_parser import *

print(parseInfoFromKTIS("2017XXXX","password"))

```

it return when, successful.
```json
{
  "status": "True",
  "content": {
      "id": "2017XXXX",
      "name": "{YOUR_NAME}",
      "ssn": "{YOUR_SOCIAL_SECURITY_NUMBER}",
      "college": "{YOUR_COLLEGE}",
      "school": "{YOUR_SCHOOL}",
      "time": "{YOUR_TIME}",
      "major": "{YOUR_MAJOR}",
      "date": "{YOUR_IN_DATE}",
      "status": "{YOUR_STATUS}",
      "grade": "{YOUR_GRADE}",
      "passwd": "{YOUR_PASSWORD}"
   }
}
```
then fail caseㄴ
```json
{
  "status": "False",
  "content": "존재하지 않는 사용자입니다."
}
```

```json
{
  "status": "False",
  "content": "비밀번호가 맞지않습니다\\r\\n비밀번호 입력오류 횟수 : (2 / 5)"
}
```