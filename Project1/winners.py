import json
import nltk
from itertools import islice
from regex import awards_regex, movie_awards_regex, person_awards_regex, match_award
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict

def get_movie_winner_for_award(tweets, award,first_names):# Given a dictionary of tweets and a specific award, returns the presenter of the

    tokenizer = RegexpTokenizer(r'\w+')

    potentialNames = {}
    count = 0
    for tweet in tweets:
        if match_award(tweet, award):
            #tags = nltk.pos_tag(nltk.word_tokenize(tweet))
            tags = tokenizer.tokenize(tweet)
            name = ''
            i = 0
            while i < len(tags):
                while i < len(tags) and tags[i][0].isupper() and tags[i] not in stopwords:
                    # print
                    name += tags[i] + ' '
                    i += 1
                name = name[:-1]
                i += 1
                break
            if name == '':
                continue
            if name in potentialNames:
                potentialNames[name] += 1
                if potentialNames[name] == 100:

                    potentialNames = dict(
                        sorted(potentialNames.items(), key=lambda item: item[1], reverse=True)[:10])
                    # if potentialNames:
                    # print(potentialNames)
                    mostFreq = max(potentialNames.values())
                    inv_map = OrderedDict((v, k) for k, v in potentialNames.items())
                    winner = []
                    for freq in inv_map:
                        if freq + 15 > mostFreq:
                            winner.append(inv_map[freq])
                        else:
                            return ' '.join(winner)

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

def get_person_winner_for_award(tweets, award, first_names):
    # Given a dictionary of tweets and a specific award, returns the presenter of the

    tokenizer = RegexpTokenizer(r'\w+')

    potentialNames = {}

    for tweet in tweets:
        if match_award(tweet, award):
            tags = tokenizer.tokenize(tweet)
            for i in range(len(tags) - 1):
                if tags[i][0].isupper() and tags[i] not in stopwords and tags[i] in first_names:
                    name = tags[i]
                    if tags[i + 1][0].isupper() and tags[i + 1] not in stopwords:
                        lastName = tags[i + 1]
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
                            potentialNames[name + ' ' + lastName] = 1

    if potentialNames:
        potentialNames = dict(sorted(potentialNames.items(),
                                     key=lambda item: item[1], reverse=True))
        potentialNames = [*potentialNames]
        return potentialNames[0]
    else:
        return


def get_winners(data, first_names):
    # Given a path to a json object of an array of tweets and award categories, returns the presenter of all awards of the golden globes for the year as dictionaries.
    # data = [tweet['text'] for tweet in data]
    winners = {}
    keywords = ["won", "win"]

    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    count = 0

    for award in awards_regex.keys():
        tags = nltk.pos_tag(nltk.word_tokenize(award))
        for tag in tags:
            stopwords.append(tag[0])
    for award in person_awards_regex.keys():
        winners[award] = get_person_winner_for_award(tweets, award, first_names)
        count += 1
        print(int(count / len(awards_regex.keys()) * 100), "% Complete")
   
    for award in movie_awards_regex.keys():
        winners[award] = get_movie_winner_for_award(tweets, award, first_names)
        count += 1
        print(int(count / len(awards_regex.keys()) * 100), "% Complete")
    return winners


stopwords = ['RT', 'Golden', 'Globes',
             'GoldenGlobes', '@goldenglobes', '@', 'goldenglobes', 'Best', 'Award', 'Picture', 'Musical', 'Comedy',
             'Drama', 'Motion', 'Globe', 'Actress', 'Actor', 'Performance', '#', 'Foreign', 'Language', 'Animated',
             'Film', 'Supporting', 'TV', 'Series', 'Television', 'Song', 'Score', 'Screenplay', 'Limited', 'Original',
             'Feature', 'Disney', 'Pixar', 'Miniseries', 'EW', 'Variety', 'BBC', 'NBC', 'Movie', 'Wins', 'Won',
             'Winning']

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

# paths = ['data/gg2013.json']#, 'data/gg2013.json']
#
#
# for path in paths:
#     file = open(path)
#     data = json.load(file)
#     tweets = [tweet["text"] for tweet in data]
#     print(get_winners(tweets, first_names))
#
# data = list()
# with open('data/gg2020.json', 'r') as f_in:
#     for line in f_in:
#         data.append(json.loads(line))
#     tweets = [tweet["text"] for tweet in data]
# print(get_winners(tweets, first_names))
