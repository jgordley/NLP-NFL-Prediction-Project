import requests
from datetime import date, datetime

base_url = "https://api.twitter.com/2/tweets/search/recent"

headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAKIeTQEAAAAAwr4P%2FqkIBDMXZSH2bdHVuFhJaHY%3Ddi9yQN0geGUXg4IBYdUxvV4y5923sXy0Wq5QnEXYPVkAuBk2et"}

hashtags = "#ndfootball #notredame #notredamefootball #fightingirish #ndfb #notredamefightingirish"
hashtags = ' OR '.join(hashtags.split())

max_results = 100

start_time = datetime(2021, 9, 11, 18, 30, 0)
end_time = datetime(2021, 9, 11, 20, 0, 0)

print(end_time.isoformat())

query = {
    "start_time": "2021-09-11T18:30:00Z",
    "end_time": "2021-09-11T20:00:00Z",
    "query": hashtags,
    "max_results": max_results
}

r = requests.get(base_url, params=query, headers=headers)
with open('result.txt', 'wb') as f:
    f.write(r.content)