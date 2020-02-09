import json
import nltk
# import spacy
from Project1.regex import search_person_award

# nlp = spacy.load("en_core_web_sm")


def get_nominee_names(data):
    # Given a path to a json object of an array of tweets, returns the hosts of the golden globes for the year.

    file_first_names = open('data/names.json')
    first_names = json.load(file_first_names)

    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    potential_names = {}
    count = 0

    tweets = list(filter(lambda x: "nomin" in x, data))

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
                        award = search_person_award(tweet)
                        if award:
                            potential_names[name + ' ' + last_name] = [award, 1]
        count += 1
        if count % 1000 == 0:
            print(int(count/len(tweets)*100), "% Complete")

    filtered_potential_nominees = {}
    print(potential_names)

    for name, award_and_count in potential_names.items():
        if award_and_count[1] > 0:
            award = award_and_count[0]
            if award in filtered_potential_nominees:
                filtered_potential_nominees[award].append(name)
            else:
                filtered_potential_nominees[award] = [name]

    return filtered_potential_nominees


paths = ['data/gg2015.json']

for path in paths:

    file = open(path)
    data = json.load(file)
    data = [tweet['text'] for tweet in data]
    nominees = get_nominee_names(data)
    print(nominees)
