import json
import nltk
from itertools import islice
from regex import awards_regex, match_award, person_awards_regex
from nltk.tokenize import RegexpTokenizer
from presenter import get_presenters


file_first_names = open('data/names.json')
first_names = json.load(file_first_names)


def get_person_noms_for_award(data, award, first_names, presenters):
    # Given a dictionary of tweets and a specific award, returns the presenter of the
    stopwords = ['RT', 'Golden', 'Globes',
                 'GoldenGlobes', '@goldenglobes', '@']

    keywords = ["nom", "hope", "should", "win", "get", "want", "chance", "wish", "for", "deserve"]
    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    tokenizer = RegexpTokenizer(r'\w+')

    potentialNames = {}
    for tweet in tweets:
        if match_award(tweet, award):
            # tags = nltk.pos_tag(nltk.word_tokenize(tweet))
            tags = tokenizer.tokenize(tweet)
            for i in range(len(tags) - 1):
                if tags[i][0].isupper() and tags[i] not in stopwords and tags[i] in first_names and tags[i] not in presenters:
                    name = tags[i]
                    if tags[i + 1][0].isupper() and tags[i + 1] not in stopwords:
                        lastName = tags[i + 1]
                        if name + ' ' + lastName in potentialNames:
                            potentialNames[name + ' ' + lastName] += 1
                            if potentialNames[name + ' ' + lastName] == 600:
                                potentialNames = dict(
                                    sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
                                if potentialNames:
                                    # print(potentialNames)
                                    potentialNames = [*potentialNames]
                                    nominees = potentialNames[:5]
                                    return nominees
                        else:
                            potentialNames[name + ' ' + lastName] = 1
    if potentialNames:
        potentialNames = dict(sorted(potentialNames.items(),
                                     key=lambda item: item[1], reverse=True))
        # print(potentialNames)
        potentialNames = [*potentialNames]
        return potentialNames[:5]
    else:
        return [""]


def get_people_noms(data, first_names, presenters):
    stopwords = ['RT', 'Golden', 'Globes',
                 'GoldenGlobes', '@goldenglobes', '@']
    # Given a path to a json object of an array of tweets and award categories, returns the presenter of all awards of the golden globes for the year as dictionaries.
    # data = [tweet['text'] for tweet in data]
    nominees = {}
    for award in person_awards_regex.keys():
        tags = nltk.pos_tag(nltk.word_tokenize(award))
        for tag in tags:
            stopwords.append(tag[0])
    count = 0
    for award in person_awards_regex.keys():
      if award != 'cecil b. demille award':
          presenters_in = presenters[award] if award in presenters.keys() else []
          nominees[award] = get_person_noms_for_award(data, award, first_names, presenters_in)
      else:
          nominees[award] = []
      count += 1
      print(int(count / len(person_awards_regex.keys()) * 100), "% Complete")
    return nominees
#
# paths = ['data/gg2013.json']
#
# for path in paths:
#     file = open(path)
#     data = json.load(file)
#     data_text = [tweet["text"] for tweet in data]
#     print(get_people_noms(data_text, first_names))

# data = list()
# with open('data/gg2020.json', 'r') as f_in:
#   for line in f_in:
#     data.append(json.loads(line))
# print(get_presenters(data))
