import pprint

from requests import get, post, delete

pprint.pprint(get("http://127.0.0.1:5000/api/tasks/12/4").json())

pprint.pprint(post("http://127.0.0.1:5000/api/tasks/12", json={
    "answers": "его нет",
    "text_of_the_task": "Ыыыыыыы",
    "adding": "подсказки не будет"
}).json())
