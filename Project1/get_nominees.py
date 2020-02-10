import nltk
import re
from string import punctuation
import json
import Levenshtein


AWARDS = ['best motion picture - drama', 'best motion picture - comedy or musical',
          'best animated feature film', 'best foreign language film',
          'best screenplay - motion picture', 'best original score - motion picture',
          'best original song - motion picture', 'best television series - drama',
          'best television series - comedy or musical', 'best mini-series or motion picture made for television']

STOPWORDS = ['rt', 'cecile', 'demille', 'golden', 'globes', 'goldenglobes', 'best', 'director', 'actor', 'actress',
             'movie', 'motion', 'picture', 'film', 'tv', 'series', 'performance', 'television', 'snub', 'wins', 'win',
             'congrats', 'congratulations', 'season', 'animated', 'animation', 'feature', 'comedy', 'drama', 'musical',
             'screenplay', 'award', 'awards', 'globe']
STOPWORDS = set(STOPWORDS)

punctuation.replace('#', '')
punctuation.replace('@', '')

def get_regexes():
    regexFor = {}
    award = 'best motion picture - drama'
    regexFor[award] = r'(?i)(best|top) (movie|picture|drama)(?!comedy)(?!musical)'

    award = 'best motion picture - comedy or musical'
    regexFor[award] = r'(?i)(best|top) (movie|picture|comedy|musical)(?!drama)'

    award = 'best animated feature film'
    regexFor[award] = r'(?i)best (animation|animated)'

    award = 'best foreign language film'
    regexFor[award] = r'(?i)best foreign'

    award = 'best screenplay - motion picture'
    regexFor[award] = r'(?i)best screenplay'

    award = 'best original score - motion picture'
    regexFor[award] = r'(?i)best score'

    award = 'best original song - motion picture'
    regexFor[award] = r'(?i)best song'

    award = 'best television series - drama'
    regexFor[award] = r'(?i)best (tv|television) (show|series) (?!comedy) (?!musical)'

    award = 'best television series - comedy or musical'
    regexFor[award] = r'(?i)best (tv|television) (show|series) (?!drama)(comedy|musical)'

    award = 'best mini-series or motion picture made for television'
    regexFor[award] = r'(?i)best (mini-series|mini series|(tv|television) (motion picture|movie))'

    return regexFor


def neg(text):
    stoplist = ['not', 'n\'t', 'should', 'wish', 'want', 'hope']
    for w in stoplist:
        if w in text:
            return True
    return False


def valid_word(w):
    if len(w) > 1:
        return w[0].isupper() and w.lower() not in STOPWORDS and w[1].islower()
    return True


def strip_punctuation(w):
    return "".join(l for l in w if l not in punctuation)


def get_movies(tweets, pattern):
    film_titles = {}
    for text in tweets:
        # text = tweet['text']
        if neg(text):
            continue
        if re.search(pattern, text):
            wordlist = text.split()
            title = []
            i = 0
            while i < len(wordlist):
                word = strip_punctuation(wordlist[i])
                # try:
                while valid_word(word) and i < len(wordlist):
                    word = strip_punctuation(wordlist[i])
                    title.append(word)
                    i += 1
                if title:
                    film_title = ' '.join(title)
                    if film_title not in film_titles:
                        film_titles[film_title] = 1
                    else:
                        film_titles[film_title] += 1
                i += 1
                # except IndexError:
                #    i += 1
    for title in film_titles:
        if title.lower() in ['a', 'the']:
            film_titles.pop(title)
    return sorted(film_titles, key=film_titles.get, reverse=True)[:5]


def get_nominee_films(data):
    nominees_dict = {}
    # count = Counter()
    # nomin_pattern = re.compile('(nomin|w[io]n)', re.IGNORECASE)
    regexes = get_regexes()
    for award in AWARDS:
        award_pattern = re.compile(regexes[award])
        nomins = get_movies(data, award_pattern)
        nominees_dict[award] = nomins
        print(award, nomins)
    return nominees_dict

# data = list()
#
# with open('data/gg2020.json', 'r') as f_in:
#     for line in f_in:
#         data.append(json.loads(line))
#
# nominees = get_nominee_films(data)


paths = ['data/gg2015.json']

for path in paths:
    file = open(path)
    data = json.load(file)
    data = [tweet['text'] for tweet in data]
    nominees = get_nominee_films(data)
    print(nominees)


