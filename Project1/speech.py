import json
import nltk
from itertools import islice
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer

file_first_names = open('data/names.json')
first_names = json.load(file_first_names)

def analyze_speeches(data, first_names = first_names):
      # Given a dictionary of tweets, returns the best dressed person at the Golden Globes for the tweets' year.
      # check nominee name instead of all
      stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes',
                   '@goldenglobes', '@', 'GoldenGlobe']
      # data = [tweet['text'] for tweet in data]
      potentialNames = {}
      count = 0

      tokenizer = RegexpTokenizer(r'\w+')

      keywords = ["speech", "monologue"]

      tweets = []
      for line in data:
          if any(keyword in line.lower() for keyword in keywords):
              tweets.append(line)

      for tweet in tweets:
          # tags = nltk.pos_tag(nltk.word_tokenize(tweet))
          tags = tokenizer.tokenize(tweet)
          for i in range(len(tags) - 1):
                name = ''
                lastName = ''
                if tags[i][0].isupper() and tags[i] not in stopwords and tags[i] in first_names:
                      name = tags[i]
                      if tags[i + 1][0].isupper() and tags[i + 1] not in stopwords:
                            lastName = tags[i + 1]
                            blob = TextBlob(tweet)
                            sent = blob.sentences[0].sentiment.polarity
                            if name + ' ' + lastName in potentialNames:
                                  potentialNames[name + ' ' +
                                                 lastName] += sent
                                  # print(name + ' ' + lastName, potentialNames[name + ' ' + lastName])
                                  if(potentialNames[name + ' ' +
                                                    lastName] >= 150):
                                        potentialNames = dict(
                                            sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
                                        potentialNames = [
                                            *potentialNames]
                                        return potentialNames
                            else:
                                  potentialNames[name + ' ' + lastName] = 1
          count += 1
          if count % 500 == 0:
            print(int(count / len(tweets) * 100), "% Complete")

      potentialNames = dict(
          sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
      potentialNames = [*potentialNames]
      return potentialNames

def speech_sentiment(data, first_names = first_names):
  #Given a list of tweets, finds the best, worst and most controversially dressed people at the Golden Globes for the year
  candidates = analyze_speeches(data, first_names)
  sentiment = {}
  sentiment['best'] = candidates[0]
  sentiment['worst'] = candidates[len(candidates) - 2]
  return sentiment


# paths = ['data/gg2015.json']#, 'data/gg2013.json']
#
#
#
#
# for path in paths:
#   file = open(path)
#   data = json.load(file)
#   tweets = [tweet["text"] for tweet in data]
#   candidates = speech_sentiment(tweets)
#   print(candidates)

# data = list()
# with open('data/gg2020.json', 'r') as f_in:
#   for line in f_in:
#     data.append(json.loads(line))
#   tweets = [tweet["text"] for tweet in data]
# candidates = speech_sentiment(tweets)
# print(candidates)
