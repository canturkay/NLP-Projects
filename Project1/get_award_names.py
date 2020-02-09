import nltk
import json


def get_award_name(tags):
    i = 0

    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@']

    while i < len(tags) - 2 and tags[i][0] != "Best":
        i += 1

    if tags[i][0] == "Best":
        award_name = "Best"
        i += 1
        while tags[i][1] == "NNP" and i < len(tags) - 1:
            if tags[i][0] in stopwords:
                break
            award_name += " " + tags[i][0]
            i += 1
        if award_name != "Best":
            # print(award_name)
            return award_name
        else:
            return None
    else:
        return None


def get_potential_award_names(tweets_unfiltered):
    tweets = list(filter(lambda x: "best" in x["text"].lower(), tweets_unfiltered))
    count = 0
    awards = {}

    for tweet in tweets:
        tags = nltk.pos_tag(nltk.word_tokenize(tweet["text"]))
        # targets = ["NNP", "NN"]
        # print(tags)
        award_name = get_award_name(tags)   # list(filter(lambda x: x[1] in targets, tags)))
        if award_name:
            if award_name in awards:
                awards[award_name] += 1
            else:
                awards[award_name] = 1
        count += 1
        if count % 1000 == 0:
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
    awards_threshold = .1

    for award, count in awards.items():
        if count > len(awards) * awards_threshold:
            awards_final.append(award)

    return awards_final


def get_award_names(data_in):
    potential_awards = get_potential_award_names(data_in)
    return parse_awards(potential_awards)




file = open('data/gg2015.json', encoding="cp866")
data = json.load(file)

