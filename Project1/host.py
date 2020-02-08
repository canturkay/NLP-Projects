import json
import nltk
from itertools import islice

paths = ['data/gg2015.json', 'data/gg2013.json']

  
file_first_names = open('data/names.json')
first_names = json.load(file_first_names)

def get_hosts(data): 
  #Given a dictionary of tweets, returns the hosts of the golden globes for the year the tweets were tweeted.
  stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@']
  data = [tweet['text'] for tweet in data]
  potentialNames = {}
  for tweet in data:
    if 'Hosts' in tweet or 'host' in tweet or 'hosts' in tweet:
      tags = nltk.pos_tag(nltk.word_tokenize(tweet))
      for i in range(len(tags) - 1):
        name = ''
        lastName = ''
        if tags[i][1] == 'NNP' and tags[i][0] not in stopwords:
          name = tags[i][0]
        if tags[i + 1][1] == 'NNP' and tags[i + 1][0] not in stopwords:
          lastName = tags[i + 1][0]
        if len(name) != 0 and len(lastName) != 0:
          if name + ' ' + lastName in potentialNames:
            potentialNames[name + ' ' + lastName] += 1
            if potentialNames[name + ' ' + lastName] == 300:
              print('i came i saw i conquered')
              potentialNames = dict(
                  sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
              first, second = islice(potentialNames.values(), 2)
              potentialNames = [*potentialNames]
              if first <= 2*second:
                hosts = potentialNames[:2]
              else:
                hosts = potentialNames[:1]
              return hosts
          else:
            if name in first_names:
              potentialNames[name + ' ' + lastName] = 1
  potentialNames = dict(
    sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
  first, second = islice(potentialNames.values(), 2)
  potentialNames = [*potentialNames]
  if first <= 2*second:
    hosts = potentialNames[:2]
  else:
    hosts = potentialNames[:1]
  return hosts


datas = []
for path in paths:
  file = open(path)
  data = json.load(file)
  print(get_hosts(data))
