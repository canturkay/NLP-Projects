import json
import requests
from bs4 import BeautifulSoup
import re
from imdb import IMDb


def all_movies(year):
    film_titles = set()
    my_regex = "\(.*\)|\s-\s.*"
    nationalities = ['American', 'British']
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
            if 'Musical' in movie['genres']:
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


def get_nominee_films(data, year):
    keywords = ['nomin']
    noms = [tweet['text'] for tweet in data if all(w in tweet['text'] for w in keywords)]

    all_films = all_movies(year)
    drama_films = {}
    com_films = {}
    anim_films = {}
    for n in noms:
        if not any(w in n for w in ['song', 'foreign', 'tv', 'show', 'series', 'actress', 'actor',
                                    'supporting', 'original', 'performance',
                                    'score', 'director', 'television']):
            films = [f for f in all_films if f in n]
            for film in films:
                c = category(film)
                if c == 'Drama':
                    if film in drama_films:
                        drama_films[film] += 1
                    else:
                        drama_films[film] = 1
                elif c == 'Comedy':
                    if film in com_films:
                        com_films[film] += 1
                    else:
                        com_films[film] = 1
                elif c == 'Animation':
                    if film in anim_films:
                        anim_films[film] += 1
                    else:
                        anim_films[film] = 1
    return sorted(drama_films, key=drama_films.get, reverse=True)[:6], \
           sorted(com_films, key=com_films.get, reverse=True)[:6],\
           sorted(anim_films, key=anim_films.get, reverse=True)[:6]

# file = open('data/gg2013.json')
# data = json.load(file)

data = list()

with open('data/gg2020.json', 'r') as f_in:
    for line in f_in:
        data.append(json.loads(line))

nominees = get_nominee_films(data, '2020')
print("Best Motion Picture - Drama")
print(nominees[0])
print("Best Motion Picture - Comedy or Musical")
print(nominees[1])
print("Best Animated Film")
print(nominees[2])

