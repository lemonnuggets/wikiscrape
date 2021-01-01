import requests

BASE_URL = "https://en.wikipedia.org/wiki/"
user_req = input("Enter the title of the page you're looking for => ")
res = requests.get(BASE_URL + user_req)
print(res.content)