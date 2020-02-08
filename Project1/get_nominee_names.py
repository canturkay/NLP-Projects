import json
import nltk
# import spacy

# nlp = spacy.load("en_core_web_sm")


def get_nominee_names(path, awards_list):
    # Given a path to a json object of an array of tweets, returns the hosts of the golden globes for the year.
    file = open(path)
    data = json.load(file)

    file_first_names = open('data/first_names.json')
    first_names = json.load(file_first_names)

    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@']
    data = [tweet['text'] for tweet in data]
    potential_names = {}
    count = 0

    for tweet in data:
        if 'nomin' in tweet:
          tags = nltk.pos_tag(nltk.word_tokenize(tweet))
          for i in range(len(tags) - 1):
            if tags[i][1] == 'NNP' and tags[i][0] not in stopwords:
                name = tags[i][0]
                if tags[i + 1][1] == 'NNP' and tags[i + 1][0] not in stopwords:
                    last_name = tags[i + 1][0]
                    if name in first_names:
                        inc = 5
                    else:
                        inc = 1
                    for award in awards_list:
                        if award in tweet:
                            if name not in award and last_name not in award:
                                if name + ' ' + last_name in potential_names:
                                    potential_names[name + ' ' + last_name][1] += inc
                                else:
                                    potential_names[name + ' ' + last_name] = [award, inc]

        count += 1
        if count % 5000 == 0:
            print(int(count/len(data)*100), "% Complete")

    filtered_potential_names = []
    print(potential_names)
    threshold = 5/1000000

    for name, award_and_count in potential_names.items():
        if award_and_count[1] > threshold * len(data):
            filtered_potential_names.append(name + ' - ' + award_and_count[0])

    nominees = filtered_potential_names
    print(nominees)
    return nominees


paths = ['data/gg2015.json']

for path in paths:
    get_nominee_names(path, ["Best Motion Picture", "Best Performance by an Actress", "Best Performance by an Actor",
          "Best Performance by an Actress in a Supporting Role", "Best Performance by an Actor in a Supporting Role",
          "Best Director", "Best Screenplay", "Best Original Score", "Best Original Song", "Best Television Series"])
