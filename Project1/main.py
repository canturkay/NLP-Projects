import json

file = open('data/gg2013.json')

data = json.load(file)

for tweet in data:
    print(tweet["text"])
