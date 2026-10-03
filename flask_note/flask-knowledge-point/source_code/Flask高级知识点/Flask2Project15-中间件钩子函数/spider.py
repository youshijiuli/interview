import requests

for _ in range(20):
    
    rep = requests.get(url='http://127.0.0.1:5000/')

    print(rep)
