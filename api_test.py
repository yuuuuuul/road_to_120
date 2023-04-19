import pprint

from requests import get, post, delete

pprint.pprint(get("http://127.0.0.1:5000/api/tasks/12/4").json())

'''pprint.pprint(post("http://127.0.0.1:5000/api/tasks/12", json={
    "answers": "его нет",
    "text_of_the_task": "Ыыыыыыы",
    "adding": "подсказки не будет"
}).json())
'''

pprint.pprint(get("http://127.0.0.1:5000/api/users").json())

pprint.pprint(get("http://127.0.0.1:5000/api/users/3").json())

pprint.pprint(post("http://127.0.0.1:5000/api/users", json={
    "nickname": "Ыыыыыыы",
    "email": "email",
    "password": "111"
}).json())

pprint.pprint(post("http://127.0.0.1:5000/api/users", json={
    "nickname": "test123",
    "email": "3124124",
    "password": "111"
}).json())

pprint.pprint(post("http://127.0.0.1:5000/api/users", json={
    "nickname": "ыыыыыыыыыывфв",
    "email": "password123@gmail.ru",
    "password": "111"
}).json())

pprint.pprint(get("http://127.0.0.1:5000/api/users/15").json())

pprint.pprint(delete("http://127.0.0.1:5000/api/users/15").json())

pprint.pprint(get("http://127.0.0.1:5000/api/users/15").json())
