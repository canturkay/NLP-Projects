import json
from nltk.tokenize import RegexpTokenizer
from Project1.regex import search_person_award, search_award, search_movie_award
import string


def get_presenters_new(data, first_names):
    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    potential_names = {}
    count = 0

    keywords = ["present"]

    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    tokenizer = RegexpTokenizer(r'\w+')

    for tweet in tweets:
        # tags = nltk.pos_tag(nltk.word_tokenize(tweet))
        tags = tokenizer.tokenize(tweet)
        for i in range(len(tags) - 1):
            word = tags[i]
            if word[0].isupper() and word not in stopwords and word in first_names:
                name = word
                if tags[i + 1][0].isupper() and tags[i + 1] not in stopwords:
                    last_name = tags[i + 1]
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
    # print(potential_names)
    threshold = 1/100000

    for name, award_and_count in potential_names.items():
        if award_and_count[1] > threshold*len(data):
            award = award_and_count[0]
            if award in filtered_potential_nominees:
                filtered_potential_nominees[award].append(name)
            else:
                filtered_potential_nominees[award] = [name]

    return filtered_potential_nominees


def get_person_nominees(data, first_names):
    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    potential_names = {}
    count = 0

    keywords = ["nomin", "win", "get"]

    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    tokenizer = RegexpTokenizer(r'\w+')

    for tweet in tweets:
        # tags = nltk.pos_tag(nltk.word_tokenize(tweet))
        tags = tokenizer.tokenize(tweet)
        for i in range(len(tags) - 1):
            word = tags[i]
            if word[0].isupper() and word not in stopwords and word in first_names:
                name = word
                if tags[i + 1][0].isupper() and tags[i + 1] not in stopwords:
                    last_name = tags[i + 1]
                    if name + ' ' + last_name in potential_names:
                        potential_names[name + ' ' + last_name][1] += 1

                    else:
                        award = search_person_award(tweet)
                        if award:
                            potential_names[name + ' ' + last_name] = [award, 1]
        count += 1
        if count % 3000 == 0:
            print(int(count / len(tweets) * 100), "% Complete")

    filtered_potential_nominees = {}
    # print(potential_names)
    threshold = 1 / 10000
    #print(potential_names)
    for name, award_and_count in potential_names.items():
        if award_and_count[1] > threshold * len(data):
            award = award_and_count[0]
            if award in filtered_potential_nominees:
                filtered_potential_nominees[award].append(name)
            else:
                filtered_potential_nominees[award] = [name]

    return filtered_potential_nominees


def get_person_winners(data, first_names):
    stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
    potential_names = {}
    count = 0

    keywords = ["win", "won", "get", "got"]

    tweets = []
    for line in data:
        if any(keyword in line.lower() for keyword in keywords):
            tweets.append(line)

    tokenizer = RegexpTokenizer(r'\w+')

    for tweet in tweets:
        # tags = nltk.pos_tag(nltk.word_tokenize(tweet))
        tags = tokenizer.tokenize(tweet)
        for i in range(len(tags) - 1):
            word = tags[i]
            if word[0].isupper() and word not in stopwords and word in first_names:
                name = word
                if tags[i + 1][0].isupper() and tags[i + 1] not in stopwords:
                    last_name = tags[i + 1]
                    if name + ' ' + last_name in potential_names:
                        potential_names[name + ' ' + last_name][1] += 1
                    else:
                        award = search_person_award(tweet)
                        if award:
                            potential_names[name + ' ' + last_name] = [award, 1]
        count += 1
        if count % 5000 == 0:
            print(int(count / len(tweets) * 100), "% Complete")

    filtered_potential_nominees = {}

    for name, award_and_count in potential_names.items():
        award = award_and_count[0]
        if award in filtered_potential_nominees:
            filtered_potential_nominees[award].append((name, award_and_count[1]))
        else:
            filtered_potential_nominees[award] = [(name, award_and_count[1])]

    winners = {}
    # print(filtered_potential_nominees)
    for award, potentials in filtered_potential_nominees.items():
        max_val = 0
        max_ind = 0
        i = 0
        for nominee in potentials:
            if nominee[1] > max_val:
                max_val = nominee[1]
                max_ind = i
            i += 1
        winners[award] = potentials[max_ind][0]

    return winners


# def get_movie_nominees(data):
#     # stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
#     potential_names = {}
#     count = 0
#
#     keywords = ["nomin", "for"]
#
#     tweets = []
#     for line in data:
#         if any(keyword in line.lower() for keyword in keywords):
#             tweets.append(line)
#
#     tokenizer = RegexpTokenizer(r'\w+')
#
#     for tweet in tweets:
#         # tags = nltk.pos_tag(nltk.word_tokenize(tweet))
#         tags = tokenizer.tokenize(tweet)
#         movie_name = get_movie_name(tags)
#         if movie_name:
#             award = search_movie_award(tweet)
#             if award:
#                 if movie_name in potential_names:
#                     potential_names[movie_name][1] += 1
#                 else:
#                     award = search_person_award(tweet)
#                     if award:
#                         potential_names[movie_name] = [award, 1]
#         count += 1
#         if count % 1000 == 0:
#             print(int(count / len(tweets) * 100), "% Complete")
#
#     filtered_potential_nominees = {}
#     print(potential_names)
#     threshold = 1 / 100000
#
#     for name, award_and_count in potential_names.items():
#         if award_and_count[1] > threshold * len(data):
#             award = award_and_count[0]
#             if award in filtered_potential_nominees:
#                 filtered_potential_nominees[award].append(name)
#             else:
#                 filtered_potential_nominees[award] = [name]
#
#     return filtered_potential_nominees
# def get_movie_name(tags):
#     i = 0
#
#     stopwords = ['RT', 'Golden', 'Globes', 'GoldenGlobes', '@goldenglobes', '@', 'Best']
#
#     while i < len(tags) - 2 and tags[i][0].islower():
#         i += 1
#
#     movie_name = ""
#
#     while tags[i][0].isupper() and i < len(tags) - 1:
#         if tags[i] in stopwords:
#             break
#         movie_name += " " + tags[i]
#         i += 1
#     if len(movie_name.split()) > 1:
#         print(movie_name)
#         return movie_name
#     else:
#         return None




# path = 'data/gg2013.json'
# file_first_names = open('data/names.json')
# first_names = json.load(file_first_names)
#
# file = open(path)
# data = json.load(file)
# data = [tweet['text'] for tweet in data]
#
# winners = get_person_winners(data, first_names)
# print(winners)

# nominees = get_person_nominees(data, first_names)
# print(nominees)

# presenters = get_presenters_new(data, first_names)
# print(presenters)

