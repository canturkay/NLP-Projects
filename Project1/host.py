import json
import nltk
from itertools import islice

paths = ['data/gg2015.json', 'data/gg2013.json']



def get_hosts(path): 
  #Given a path to a json object of an array of tweets, returns the hosts of the golden globes for the year.
  file = open(path)
  data = json.load(file)

  stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@']
  data = [tweet['text'] for tweet in data]
  potentialNames = {}
  for tweet in data:
    if 'hosts' in tweet:
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
            if potentialNames[name + ' ' + lastName] == 10:
              potentialNames = dict(
                  sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
              break
          else:
            potentialNames[name + ' ' + lastName] = 1

  first, second = islice(potentialNames.values(), 2)
  potentialNames = [*potentialNames]
  if first <= 2*second: 
    hosts = potentialNames[:2]
  else: 
    hosts = potentialNames[:1]
  print(hosts)
  return hosts


for path in paths:
  get_hosts(path)
