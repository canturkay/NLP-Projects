import json
import requests
from bs4 import BeautifulSoup
import re
from imdb import IMDb
import nltk
import random
import re


def all_movies(year):
    film_titles = set()
    my_regex = "\(.*\)|\s-\s.*"
    html = requests.get('https://en.wikipedia.org/wiki/List_of_%s_films_of_%s' % ('American', str(int(year)-1)))
    b = BeautifulSoup(html.text, 'lxml')
    # print(b.prettify())
    for i in b.find_all(name='table', class_='wikitable sortable'):
        for j in i.find_all(name='td'):
            for k in j.find_all(name='i'):
                for link in k.find_all('a', href=True):
                    film_titles.add(re.sub(my_regex, "", link['title']).rstrip())
    html = requests.get('https://en.wikipedia.org/wiki/List_of_%s_films_of_%s' % ('British', str(int(year) - 1)))
    b = BeautifulSoup(html.text, 'lxml')
    # print(b.prettify())
    for table in b.find_all(name='table', class_='wikitable sortable plainrowheaders'):
        for tr in table.find_all(name='tr'):
            for j in tr.find_all(name='td'):
                for k in j.find_all(name='i'):
                    for link in k.find_all('a', href=True):
                        film_titles.add(re.sub(my_regex, "", link['title']).rstrip())
    return film_titles


dramas = set()
comedies = set()
anim = set()


def category(film_title):
    if film_title in dramas:
        return 'Drama'
    elif film_title in comedies:
        return 'Comedy'
    elif film_title in anim:
        return 'Animation'
    # print(dramas, comedies, film_title)
    ia = IMDb()
    movies = ia.search_movie(film_title)
    for m in movies:
        if m['title'] == film_title or m['title'][:len(film_title)] == film_title:
            movie = ia.get_movie(m.getID())
            if 'genre' in movie and 'Musical' in movie['genres']:
                comedies.add(film_title)
                return 'Comedy'
            for genre in movie['genres']:
                if genre == 'Comedy':
                    comedies.add(film_title)
                    return 'Comedy'
                elif genre == 'Drama':
                    dramas.add(film_title)
                    return 'Drama'
                elif genre == 'Animation':
                    anim.add(film_title)
                    return 'Animation'
            comedies.add(film_title)
            return 'Comedy'


def neg(text):
    stoplist = ['not', 'n\'t', 'should', 'wish', 'want', 'hope']
    for w in stoplist:
        if w in text:
            return True
    return False

def get_nominee_films(data, year):
    keywords = ['nomin', 'won', 'win', 'best']
    noms = [tweet['text'] for tweet in data if any(w in tweet['text'] for w in keywords)]

    all_films = all_movies(year)
    drama_films = {}
    com_films = {}
    anim_films = {}
    song_films = {}
    score_films = {}
    screenplay = {}
    for n in noms:
        if neg(n):
            continue
        if not any(w in n for w in ['song', 'foreign', 'tv', 'show', 'series', 'actress', 'actor',
                                    'supporting', 'original', 'performance', 'screenplay',
                                    'score', 'director', 'television']):
            films = [f for f in all_films if f in n]
            for nom in films:
                c = category(nom)
                if c == 'Drama':
                    if nom in drama_films:
                        drama_films[nom] += 1
                    else:
                        drama_films[nom] = 1
                elif c == 'Comedy':
                    if nom in com_films:
                        com_films[nom] += 1
                    else:
                        com_films[nom] = 1
                elif c == 'Animation':
                    if nom in anim_films:
                        anim_films[nom] += 1
                    else:
                        anim_films[nom] = 1
        elif "song" in n:
            films = [f for f in all_films if f in n]
            for nom in films:
                if nom in song_films:
                    song_films[nom] += 1
                else:
                    song_films[nom] = 1
        elif "score" in n:
            films = [f for f in all_films if f in n]
            for nom in films:
                if nom in score_films:
                    score_films[nom] += 1
                else:
                    score_films[nom] = 1
        elif "screenplay" in n:
            films = [f for f in all_films if f in n]
            for nom in films:
                if nom in screenplay:
                    screenplay[nom] += 1
                else:
                    screenplay[nom] = 1
    nom = {}
    nom['best motion picture - drama'] = sorted(drama_films, key=drama_films.get, reverse=True)[:5]
    nom['best motion picture - comedy or musical'] = sorted(com_films, key=com_films.get, reverse=True)[:5]
    nom['best animated film'] = sorted(anim_films, key=anim_films.get, reverse=True)[:5]
    nom['best original song - motion picture'] = sorted(song_films, key=song_films.get, reverse=True)[:5]
    nom['best original score - motion picture'] = sorted(score_films, key=score_films.get, reverse=True)[:5]
    nom['best screenplay - motion picture'] = sorted(screenplay, key=screenplay.get, reverse=True)[:5]
    win = {}
    for award in nom:
        win[award] = nom[award][0]
    return win, nom


def get_nominee_tv(data):
    file_first_names = open('data/names.json')
    first_names = json.load(file_first_names)

    stopwords = set(['RT', 'golden', 'Golden', 'globes', 'Globes', 'goldenglobes', '@goldenglobes', '@',
                     'best', 'wins', '#', 'congrats',
                 'congratulations', 'actor', 'actress', 'Actor', 'Actress', 'globe', 'Globe' 'winning'])

    potential_names = {'best mini-series or motion picture made for television': {},
                       'best television series - drama': {},
                       'best television series - comedy or musical': {}}
    count = 0

    def valid_word(w):
        if len(w) > 1:
            return w[0].isupper() and w.lower() not in stopwords and w[1].islower()
        return True

    keywords = ['nomin', 'won', 'win', 'best']
    tweets = [tweet['text'] for tweet in data if any(w in tweet['text'] for w in keywords)]

    for tweet in tweets:
        if neg(tweet):
            continue
        if any(w in tweet for w in ['song', 'foreign', 'actress', 'actor', 'Actor', 'Actress'
                                    'supporting', 'original', 'performance', 'screenplay',
                                    'score', 'director']):
            continue
        pattern = re.compile(r'(?i)mini-series|mini series|((tv|television) (motion picture|movie))')
        if re.search(pattern, tweet):
            award = 'best mini-series or motion picture made for television'
        elif re.search(r'(?i)(tv|television) (show|series)', tweet):
            if 'drama' in tweet or ('comedy' not in tweet and 'musical' not in tweet):
                award = 'best television series - drama'
            elif 'comedy' in tweet or 'musical' in tweet and 'drama' not in tweet:
                award = 'best television series - comedy or musical'
            else:
                award = 'best television series - drama' if random.random() >= 0.5 \
                    else 'best television series - comedy or musical'
        else:
            continue
        # print(award, tweet)
        tags = nltk.pos_tag(nltk.word_tokenize(tweet))
        for i in range(len(tags) - 1):
            if tags[i][1] == 'NNP' and tags[i][0] not in stopwords and tags[i][0] not in first_names:
                w = tags[i][0]
                title = []
                i = 0
                while w[0].isupper() and w not in stopwords and i < len(tags):
                    w = tags[i][0]
                    title.append(w)
                    i += 1
                if title:
                    for word in title:
                        if word.lower() in stopwords:
                            continue
                    name = ' '.join(title)
                    if name in potential_names[award]:
                        potential_names[award][name] += 1
                    else:
                        potential_names[award][name] = 1
        count += 1
        if count % 1000 == 0:
            print(int(count / len(tweets) * 100), "% Complete")

    for award in potential_names:
        potential_names[award] = sorted(potential_names[award], key=potential_names[award].get, reverse=True)[:5]

    return potential_names


file = open('data/gg2013.json')
data = json.load(file)


data = list()

with open('data/gg2020.json', 'r') as f_in:
    for line in f_in:
        data.append(json.loads(line))


# print(get_nominee_tv(data))

winners, nominees = get_nominee_films(data, '2020')
print(winners)
print(nominees)




