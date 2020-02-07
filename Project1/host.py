import json
import nltk



file = open('data/gg2015.json')

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
potentialNames = [*potentialNames]
hosts = potentialNames[:2]
print(hosts)
