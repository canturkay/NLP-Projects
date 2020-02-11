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


def get_award_names(data):
    count = 0
    awards = {}

    # stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    keywords = ["best"]

    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    tokenizer = RegexpTokenizer(r'\w+')
    award_keywords = ["act", "award", "television", "series", "performance", "picture", "supporting"]
    for tweet in tweets:
        tags = tokenizer.tokenize(tweet)
        # targets = ["NNP", "NN"]
        # print(tags)
        award_name = get_award_name(tags)   # list(filter(lambda x: x[1] in targets, tags)))
        if award_name:
            if award_name in awards:
                if len(award_name.split()) >= 4:
                    if any(keyword in tweet.lower() for keyword in award_keywords):
                        awards[award_name] += 3
                    else:
                        awards[award_name] += 1
            else:
                awards[award_name] = 1
        count += 1
        if count % 5000 == 0:
            print(int(count/len(tweets)*100), "% Complete")

    # awards_file = open("processed_data/awards.json", "w+")
    # awards_file.write(json.dumps(awards))
    # awards_file.close()
    awards = dict(sorted(awards.items(),
                key=lambda item: item[1], reverse=True))
    awards = [*awards]
    return awards[:26]
#
# file = open('data/gg2015.json', encoding="cp866")
# data = json.load(file)
# print(get_award_names([x["text"] for x in data]))

