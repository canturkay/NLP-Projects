import json
import nltk
from itertools import islice
from host import get_hosts

paths = ['data/gg2015.json', 'data/gg2013.json']

Awards = ["Best Motion Picture", "Best Performance by an Actress", "Best Performance by an Actor",
            "Best Performance by an Actress in a Supporting Role", "Best Performance by an Actor in a Supporting Role",
            "Best Director", "Best Screenplay", "Best Original Score", "Best Original Song", "Best Television Series"]

stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@']



file_first_names = open('data/names.json')
first_names = json.load(file_first_names)

def get_presenter_for_award(tweets, award):
  
  potentialNames = {}
  for tweet in tweets:
    if 'present' in tweet and award in tweet:
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
            if name in first_names:
              potentialNames[name + ' ' + lastName] += 5
            else: 
              potentialNames[name + ' ' + lastName] += 1
            if potentialNames[name + ' ' + lastName] == 30:
              potentialNames = dict(
                  sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
              break
          else:
            potentialNames[name + ' ' + lastName] = 1
  if potentialNames:
    first, second = islice(potentialNames.values(), 2)
    potentialNames = [*potentialNames]
    if first <= 2 * second:
      presenters = potentialNames[:2]
    else:
      presenters = potentialNames[:1]
    # print(presenters)
    return presenters
  else:
    return
  

def get_presenters(path, awards = Awards): 
  #Given a path to a json object of an array of tweets and award categories, returns the presenter of all awards of the golden globes for the year as dictionaries.
  file = open(path)
  data = json.load(file)
  data = [tweet['text'] for tweet in data]
  presenters = {}
  for award in awards:
    tags = nltk.pos_tag(nltk.word_tokenize(award))
    for tag in tags:
      stopwords.append(tag[0])
  for award in awards: 
    presenters[award] = get_presenter_for_award(data, award)
  print(presenters)
  return presenters

for path in paths: 
  get_presenters(path)

