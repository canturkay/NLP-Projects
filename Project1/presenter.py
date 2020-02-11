import json
import nltk
from itertools import islice
from Project1.regex import awards_regex, match_award, person_awards_regex
from nltk.tokenize import RegexpTokenizer


def get_presenter_for_award(data, award, first_names, winner_list):
    # Given a dictionary of tweets and a specific award, returns the presenter of the
    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@']

    keywords = ["present"]

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
                if tags[i][0].isupper() and tags[i] not in stopwords and tags[i] in first_names:
                    name = tags[i]
                    if tags[i + 1][0].isupper() and tags[i + 1] not in stopwords:
                        lastName = tags[i + 1]
                        if name + ' ' + lastName not in winner_list:
                            if name + ' ' + lastName in potentialNames:
                                potentialNames[name + ' ' + lastName] += 1
                                if potentialNames[name + ' ' + lastName] == 200:
                                    potentialNames = dict(
                                        sorted(potentialNames.items(), key=lambda item: item[1], reverse=True))
                                    if potentialNames:
                                        first, second = islice(potentialNames.values(), 2)
                                        potentialNames = [*potentialNames]
                                        if first <= 2 * second:
                                            presenters = potentialNames[:2]
                                        else:
                                            presenters = potentialNames[:1]
                                        return presenters
                            else:
                                potentialNames[name + ' ' + lastName] = 1
    if potentialNames:
        potentialNames = dict(sorted(potentialNames.items(),
                                     key=lambda item: item[1], reverse=True))
        potentialNames = [*potentialNames]
        return potentialNames[0]
    else:
        return


def get_presenters(data, first_names, winners):
    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@']
    # Given a path to a json object of an array of tweets and award categories, returns the presenter of all awards of the golden globes for the year as dictionaries.
    # data = [tweet['text'] for tweet in data]
    presenters = {}
    for award in awards_regex.keys():
        tags = nltk.pos_tag(nltk.word_tokenize(award))
        for tag in tags:
            stopwords.append(tag[0])
    count = 0
    for award in awards_regex.keys():
        winner_list = winners[award] if award in person_awards_regex.keys() else []
        presenters[award] = get_presenter_for_award(data, award, first_names, winner_list)
        count += 1
        print(int(count / len(awards_regex.keys()) * 100), "% Complete")
    return presenters


# paths = ['data/gg2015.json']
#
#
# file_first_names = open('data/names.json')
# first_names = json.load(file_first_names)
#
#
# for path in paths:
#     file = open(path)
#     data = json.load(file)
#     data_text = [tweet["text"] for tweet in data]
#     print(get_presenters(data_text, first_names, {}))

# data = list()
# with open('data/gg2020.json', 'r') as f_in:
#   for line in f_in:
#     data.append(json.loads(line))
# print(get_presenters(data))
