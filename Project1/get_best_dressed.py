import json
import nltk
from itertools import islice
from textblob import TextBlob

def get_best_dressed(data, first_names):
      # Given a dictionary of tweets, returns the best dressed person at the Golden Globes for the tweets' year.
      # check nominee name instead of all
      stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'GoldenGlobe']
      # data = [tweet['text'] for tweet in data]
      potentialNames = {}
      count = 0

      for tweet in data:
            if 'dress' in tweet.lower() or 'look' in tweet.lower():
                  tags = nltk.pos_tag(nltk.word_tokenize(tweet))
                  for i in range(len(tags) - 1):
                        name = ''
                        lastName = ''
                        if tags[i][1] == 'NNP' and tags[i][0] not in stopwords and tags[i][0] in first_names:
                              name = tags[i][0]
                              if tags[i + 1][1] == 'NNP' and tags[i + 1][0] not in stopwords:
                                    lastName = tags[i + 1][0]
                                    blob = TextBlob(tweet)
                                    sent = blob.sentences[0].sentiment.polarity
                                    if name + ' ' + lastName in potentialNames:
                                          potentialNames[name + ' ' +
                                                           lastName] += sent
                                          # print(name + ' ' + lastName, potentialNames[name + ' ' + lastName])
                                          if(potentialNames[name + ' ' +
                                                            lastName] >= 50):
                                                potentialNames = dict(
                                                    sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
                                                potentialNames = [*potentialNames]
                                                return potentialNames
                                    else:
                                                potentialNames[name + ' ' +
                                                           lastName] = 10

            count += 1
            if count % 1000 == 0:
                print(int(count*10 / len(data) * 100), "% Complete")

      potentialNames = dict(
          sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
      potentialNames = [*potentialNames]
      return potentialNames


def bestDressed(potentialNames): 
  return potentialNames[0]
def worstDressed(potentialNames): 
  return potentialNames[len(potentialNames) - 1]
def controversialDressed(potentialNames):
  middle = int(len(potentialNames)/2)
  return potentialNames[middle]


def dress_sentiment(data, first_names):
  #Given a list of tweets, finds the best, worst and most controversially dressed people at the Golden Globes for the year
  candidates = get_best_dressed(data, first_names)
  sentiment = {}
  sentiment['best'] = bestDressed(candidates)
  sentiment['worst'] = worstDressed(candidates)
  sentiment['controversial'] = controversialDressed(candidates)
  return sentiment



# paths = ['data/gg2015.json']
#
#
# file_first_names = open('data/names.json')
# first_names = json.load(file_first_names)
#
#
# datas = []
# for path in paths:
#   file = open(path)
#   data = json.load(file)
#   candidates = get_best_dressed(data)
#   print('Best dressed:', bestDressed(candidates))
#   print('Worst dressed:', worstDressed(candidates))
#   print('Most controversially dressed:', controversialDressed(candidates))
