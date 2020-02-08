import json
import nltk
# import spacy

# nlp = spacy.load("en_core_web_sm")

def get_nominee_names(data_in, awards_list):
    # Given a path to a json object of an array of tweets, returns the hosts of the golden globes for the year.

    file_first_names = open('data/names.json')
    first_names = json.load(file_first_names)

    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    data = [tweet['text'] for tweet in data_in]
    potential_names = {}
    count = 0

    for tweet in data:
        if 'nomin' in tweet.lower():
          tags = nltk.pos_tag(nltk.word_tokenize(tweet))
          for i in range(len(tags) - 1):
            if tags[i][1] == 'NNP' and tags[i][0] not in stopwords and tags[i][0] in first_names :
                name = tags[i][0]
                if tags[i + 1][1] == 'NNP' and tags[i + 1][0] not in stopwords:
                    last_name = tags[i + 1][0]
                    if name + ' ' + last_name in potential_names:
                        potential_names[name + ' ' + last_name][1] += 1
                    else:
                        for award in awards_list:
                            if award.lower() in tweet.lower():
                                potential_names[name + ' ' + last_name] = [award, 1]

        count += 1
        if count % 5000 == 0:
            print(int(count/len(data)*100), "% Complete")

    filtered_potential_nominees = {}
    print(potential_names)
    threshold = 1/100000

    for name, award_and_count in potential_names.items():
        if award_and_count[1] > 3:
            award = award_and_count[0]
            if award in filtered_potential_nominees:
                filtered_potential_nominees[award].append(name)
            else:
                filtered_potential_nominees[award] = [name]

    return filtered_potential_nominees


paths = ['data/gg2013.json']

for path in paths:

    file = open(path)
    data = json.load(file)

    nominees = get_nominee_names(data, ["Best Performance", "Best Actor", "Best Actress",
                             "Best Supporting Actor", "Best Supporting Actress",
                            "Best Director", "Best Original Score", "Best Screenplay"
                             "Best Original Score", "Best Original Song"])
    print(nominees)
