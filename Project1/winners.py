import json
import nltk
from itertools import islice

stopwords = ['RT', 'Golden', 'Globes',
             'GoldenGlobes', '@goldenglobes', '@', 'goldenglobes', 'Best', 'Award']

file_first_names = open('data/names.json')
first_names = json.load(file_first_names)

awardkeywords = ["best screenplay", 
                    "best director",
                    "best actress tv comedy",
                    "best foreign language film",
                    "best supporting actor",
                    "best supporting actress limited series",
                    "best comedy or musical movie",
                    "best limited series",
                    "best original score",
                    "Best actress in a musical or comedy",
                    "best actress in drama",
                    "best actor in a musical or comedy",
                    "best drama movie",
                    "best supporting actor limited series",
                    "best supporting actress",
                    "best drama series",
                    "best actor limited series",
                    "best actress limited series",
                    "best animated film",
                    "best original song",
                    "best actor drama",
                    "best comedy series",
                    "Best actor tv drama",
                    "Best TV comedy actor"
                ]
def get_winner_for_award(tweets, award, first_names = first_names):
    # Given a dictionary of tweets and a specific award, returns the presenter of the
    potentialNames = {}
    for tweet in tweets:
        if 'movies' not in award.lower() or 'series' not in award.lower() or 'limited series' in award.lower():
            if ('won' in tweet.lower() or 'win' in tweet.lower()) and award.lower() in tweet.lower():
                tags = nltk.pos_tag(nltk.word_tokenize(tweet))
                for i in range(len(tags) - 1):
                    name = ''
                    lastName = ''
                    if tags[i][1] == 'NNP' and tags[i][0] not in stopwords:
                        name = tags[i][0]
                        if tags[i + 1][1] == 'NNP' and tags[i + 1][0] not in stopwords:
                            lastName = tags[i + 1][0]
                            if name + ' ' + lastName in potentialNames:
                                potentialNames[name + ' ' + lastName] += 1
                                if potentialNames[name + ' ' + lastName] == 100:
                                    potentialNames = dict(
                                        sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
                                    if potentialNames:
                                        potentialNames = [*potentialNames]
                                        winner = potentialNames[0]
                                        return winner
                            else:
                                if name in first_names:
                                    potentialNames[name + ' ' + lastName] = 1
        else: 
            if ('won' in tweet.lower() or 'win' in tweet.lower() or 'got' in tweet.lower()) and award.lower() in tweet.lower():
                tags = nltk.pos_tag(nltk.word_tokenize(tweet))
                for i in range(len(tags) - 1):
                    name = ''
                    lastName = ''
                    if tags[i][1] == 'NNP' and tags[i][0] not in stopwords:
                        name = tags[i][0]
                        if name in potentialNames:
                            potentialNames[name] += 1
                            if potentialNames[name] == 100:
                                potentialNames = dict(
                                    sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
                                if potentialNames:
                                    potentialNames = [*potentialNames]
                                    winner = potentialNames[0]
                                    return winner
                        else:
                            potentialNames[name] = 1
    if potentialNames:
        potentialNames = dict(sorted(potentialNames.items(),
                                     key=lambda item: item[1], reverse=True))
        potentialNames = [*potentialNames]
        return potentialNames[0]
    else:
        return


def get_winners(data, first_names = first_names, awards=awardkeywords):
    # Given a path to a json object of an array of tweets and award categories, returns the presenter of all awards of the golden globes for the year as dictionaries.
    # data = [tweet['text'] for tweet in data]
    winners = {}
    for award in awards:
        tags = nltk.pos_tag(nltk.word_tokenize(award))
        for tag in tags:
            stopwords.append(tag[0])
    for award in awards:
        winners[award] = get_winner_for_award(data, award, first_names)
    return winners


paths = ['data/gg2015.json', 'data/gg2013.json']


for path in paths:
    file = open(path)
    data = json.load(file)
    tweets = [tweet["text"] for tweet in data]
    print(get_winners(tweets))

data = list()
with open('data/gg2020.json', 'r') as f_in:
  for line in f_in:
    data.append(json.loads(line))
  tweets = [tweet["text"] for tweet in data]
print(get_winners(tweets))
