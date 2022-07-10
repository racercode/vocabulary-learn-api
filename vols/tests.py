import requests as rq
import json
r = rq.post("http://127.0.0.1:8000/api/v1/add_category/", data={
    'name': 'first_ffcategory',
    'description': '第4dddd44個測試',
    'vol_list': [
        'fwdfffwfefewee',
    ]
})
print(r.text)


# Create your tests here.