import nltk
import json
from nltk.tokenize import RegexpTokenizer


def get_award_name(tags):
    i = 0

    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'GoldenGlobe']

    while i < len(tags) - 2 and tags[i] != "Best":
        i += 1

    if tags[i] == "Best":
        award_name = "Best"
        i += 1
        while tags[i][0].isupper() and i < len(tags) - 1:
            if tags[i] in stopwords:
                break
            award_name += " " + tags[i]
            i += 1
        if award_name != "Best":
            # print(award_name)
            return award_name
        else:
            return None
    else:
        return None


def get_potential_award_names(data):
    count = 0
    awards = {}

    # stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    keywords = ["best"]

    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    tokenizer = RegexpTokenizer(r'\w+')

    for tweet in tweets:
        tags = tokenizer.tokenize(tweet)
        # targets = ["NNP", "NN"]
        # print(tags)
        award_name = get_award_name(tags)   # list(filter(lambda x: x[1] in targets, tags)))
        if award_name:
            if award_name in awards:
                awards[award_name] += 1
            else:
                awards[award_name] = 1
        count += 1
        if count % 5000 == 0:
            print(int(count/len(tweets)*100), "% Complete")

    # awards_file = open("processed_data/awards.json", "w+")
    # awards_file.write(json.dumps(awards))
    # awards_file.close()
    return awards


def parse_awards(awards):
    # awards_file = open("processed_data/awards.json", encoding="cp866")
    # awards = json.load(awards_file)

    awards_final = []
    # print(awards)
    awards_threshold = .2

    for award, count in awards.items():
        if count > len(awards) * awards_threshold:
            awards_final.append(award)

    return awards_final


def get_award_names(data_in):
    potential_awards = get_potential_award_names(data_in)
    return parse_awards(potential_awards)

# file = open('data/gg2015.json', encoding="cp866")
# data = json.load(file)
# print(get_award_names([x["text"] for x in data]))

