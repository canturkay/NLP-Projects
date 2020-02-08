import json
import spacy
import wikipedia
import requests
from bs4 import BeautifulSoup
import re
from imdb import IMDb
import time
import numpy as np
import pandas as pd

year = '2015'
def all_movies():
    '''
    df = pd.read_csv('data.tsv', sep='\t', low_memory=False)
    df.query('titleType == "movie" and startYear == "2014"', inplace=True)
    all_films = set(df['primaryTitle'])
    return all_films
    '''

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


all_movies()
dramas = set()
comedies = set()
anim = set()
ia = IMDb()


def category(film_title):
    if film_title in dramas:
        return 'Drama'
    elif film_title in comedies:
        return 'Comedy'
    elif film_title in anim:
        return 'Animation'
    # print(dramas, comedies, film_title)
    movies = ia.search_movie(film_title)
    for m in movies:
        if m['title'] == film_title or m['title'][:len(film_title)] == film_title:
            # if 'year' not in m or m['year'] == str(int(year)-1):
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


file = open('data/gg2015.json')

data = json.load(file)

awards = ["Best Motion Picture", "Best Performance by an Actress", "Best Performance by an Actor",
          "Best Performance by an Actress in a Supporting Role", "Best Performance by an Actor in a Supporting Role",
          "Best Director", "Best Screenplay", "Best Original Score", "Best Original Song", "Best Television Series"]
#awards = [a.lower() for a in awards]

categories = ["Drama", "Musical or Comedy", "Animated", "Foreign Language"]
#categories = [c.lower() for c in categories]

keywords = ['nomin']  #, 'best']
noms = [tweet['text'] for tweet in data if all(w in tweet['text'] for w in keywords)]

all_films = all_movies()
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
print("Best Motion Picture - Drama")
print(sorted(drama_films, key=drama_films.get, reverse=True)[:6])
print("Best Motion Picture - Comedy or Musical")
print(sorted(com_films, key=com_films.get, reverse=True)[:6])
print("Best Animated Film")
print(sorted(anim_films, key=anim_films.get, reverse=True)[:6])

