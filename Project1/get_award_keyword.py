import json
import nltk
from Project1.regex import search_person_award, search_award, search_movie_award


def get_presenters(data, first_names):

    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    potential_names = {}
    count = 0

    keywords = ["present"]

    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    for tweet in tweets:
        tags = nltk.pos_tag(nltk.word_tokenize(tweet))
        for i in range(len(tags) - 1):
            if tags[i][1] == 'NNP' and tags[i][0] not in stopwords and tags[i][0] in first_names:
                name = tags[i][0]
                if tags[i + 1][1] == 'NNP' and tags[i + 1][0] not in stopwords:
                    last_name = tags[i + 1][0]
                    if name + ' ' + last_name in potential_names:
                        potential_names[name + ' ' + last_name][1] += 1
                    else:
                        award = search_award(tweet)
                        if award:
                            potential_names[name + ' ' + last_name] = [award, 1]
        count += 1
        if count % 1000 == 0:
            print(int(count / len(tweets) * 100), "% Complete")

    filtered_potential_nominees = {}
    print(potential_names)
    threshold = 1/10000

    for name, award_and_count in potential_names.items():
        if award_and_count[1] > threshold*len(data):
            award = award_and_count[0]
            if award in filtered_potential_nominees:
                filtered_potential_nominees[award].append(name)
            else:
                filtered_potential_nominees[award] = [name]

    return filtered_potential_nominees


paths = ['data/gg2015.json']
file_first_names = open('data/names.json')
first_names = json.load(file_first_names)

for path in paths:

    file = open(path)
    data = json.load(file)
    data = [tweet['text'] for tweet in data]
    nominees = get_presenters(data, first_names)
    print(nominees)

