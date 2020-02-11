import json
import nltk
from itertools import islice
from regex import awards_regex, movie_awards_regex, person_awards_regex, match_award
from nltk.tokenize import RegexpTokenizer


def get_movie_winner_for_award(tweets, award):
    tokenizer = RegexpTokenizer(r'\w+')

    potentialNames = {}
    for tweet in tweets:
        if match_award(tweet, award):
            #tags = nltk.pos_tag(nltk.word_tokenize(tweet))
            tags = tokenizer.tokenize(tweet)
            for i in range(len(tags) - 1):
                name = ''
                lastName = ''
                if tags[i][0].isupper() and tags[i] not in stopwords:
                    name = tags[i]
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
        winners[award] = get_movie_winner_for_award(tweets, award)
        count += 1
        print(int(count / len(awards_regex.keys()) * 100), "% Complete")
    return winners

stopwords = ['RT', 'Golden', 'Globes',
             'GoldenGlobes', '@goldenglobes', '@', 'goldenglobes', 'Best', 'Award', 'Picture', 'Musical', 'Comedy',
             'Drama', 'Motion', 'Globe', 'Actress', 'Actor', 'Performance', '#', 'Foreign', 'Language', 'Animated',
             'Film', 'Supporting', 'TV', 'Series', 'Television', 'Song', 'Score', 'Screenplay', 'Limited', 'Original',
             'Feature', 'Disney', 'Pixar', 'Miniseries', 'EW', 'Variety', 'BBC', 'NBC', 'Movie', 'Wins', 'Won',
             'Winning', 'Cecil', 'Director', 'Categories', 'Oscar', 'Nominees']


file_first_names = open('data/names.json')
first_names = json.load(file_first_names)

def get_movie_nom_for_award(tweets, award):
    tokenizer = RegexpTokenizer(r'\w+')

    potentialNames = {}
    for tweet in tweets:
        if match_award(tweet, award):
            #tags = nltk.pos_tag(nltk.word_tokenize(tweet))
            tags = tokenizer.tokenize(tweet)
            i = 0
            while i < len(tags):
                name = ''
                while i < len(tags) and tags[i][0].isupper() and tags[i] not in stopwords:
                    # print
                    name += tags[i] + ' '
                    i += 1
                name = name[:-1]
                if name == '':
                    i += 1
                    continue
                # print(name)
                if name in potentialNames:
                    potentialNames[name] += 1
                else:
                    potentialNames[name] = 1
                i += 1
    # print(potentialNames)
    return sorted(potentialNames, key=potentialNames.get, reverse=True)[:5]

def get_nominees(data):
    keywords = ["nomin"]
    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)
    count = 0
    nomins = {}
    for award in movie_awards_regex.keys():
        nomins[award] = get_movie_nom_for_award(tweets, award)
        count += 1
        print(int(count / len(awards_regex.keys()) * 100), "% Complete")
    return nomins

paths = ['data/gg2013.json', 'data/gg2015.json']#, 'data/gg2013.json']


for path in paths:
     file = open(path)
     data = json.load(file)
     tweets = [tweet["text"] for tweet in data]
     # print(get_winners(tweets, first_names))
     print(get_nominees(tweets))    

data = list()
with open('data/gg2020.json', 'r') as f_in:
    for line in f_in:
        data.append(json.loads(line))
    tweets = [tweet["text"] for tweet in data]
# print(get_winners(tweets, first_names))
print(get_nominees(tweets))

# data = list()
# with open('data/gg2020.json', 'r') as f_in:
#   for line in f_in:
#     data.append(json.loads(line))
#   tweets = [tweet["text"] for tweet in data]
# print(get_winners(tweets,  first_names))
