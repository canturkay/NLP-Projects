import json

'''
from Project1.get_nominee_names import get_nominee_names
from  Project1.get_award_names import get_award_names
from  Project1.host import get_hosts
from  Project1.presenter import get_presenters
from  Project1.get_best_dressed import dress_sentiment
from  Project1.regex import search_award, awards_regex
from Project1.get_award_keyword import get_person_nominees, get_presenters_new, get_person_winners
from Project1.winners import get_winners
from Project1.speech import speech_sentiment
'''

from get_nominee_names import get_nominee_names
from  get_award_names import get_award_names
from  host import get_hosts
from  presenter import get_presenters
from  get_best_dressed import dress_sentiment
from  regex import search_award, awards_regex
from get_award_keyword import get_person_nominees, get_presenters_new, get_person_winners
from winners import get_winners
from speech import speech_sentiment
from noms import get_people_noms

print("Running!")

class GGresponse:
    real_award_names = ["best screenplay - motion picture", "best director - motion picture",
                        "best performance by an actress in a television series - comedy or musical",
                        "best foreign language film",
                        "best performance by an actor in a supporting role in a motion picture",
                        "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television",
                        "best motion picture - comedy or musical",
                        "best mini-series or motion picture made for television",
                        "best original score - motion picture",
                        "best performance by an actress in a television series - drama",
                        "best performance by an actress in a motion picture - drama",
                        "best performance by an actor in a motion picture - comedy or musical",
                        "best motion picture - drama",
                        "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television",
                        "best performance by an actress in a supporting role in a motion picture",
                        "best television series - drama",
                        "best performance by an actor in a mini-series or motion picture made for television",
                        "best performance by an actress in a mini-series or motion picture made for television",
                        "best animated feature film",
                        "best original song - motion picture",
                        "best performance by an actor in a motion picture - drama",
                        "best television series - comedy or musical",
                        "best performance by an actor in a television series - drama",
                        "best performance by an actor in a television series - comedy or musical"
                        ]
    data = {}
    tweets = []

    hosts = []
    presenters = {}
    nominee_people = {}
    nominee_movies = {}
    nominee = {}

    winners = {}
    awards = {}
    dresses = {}
    speech = {}

    first_names = []
    keywords = []
    award_names = []

    def __init__(self, path):
        print("Loading data!")
        print("Loading first names file!")

        file = open(path)
        data = json.load(file)

        keywords = ["get", "got", "win", "won", "host", "present", "nomin", "look", "dress", "want", "wish",
                    "hope", "should", "best", "give", "speech", "monologue"]

        data_text = [tweet["text"] for tweet in data]
        tweets = []
        for line in data_text:
            if any(keyword in line.lower() for keyword in keywords):
                tweets.append(line)

        tweets = tweets[:300000]

        file_first_names = open('data/names.json')
        first_names = json.load(file_first_names)

        self.first_names = first_names
        self.tweets = tweets
        self.data = data

    def __str__(self):
        s = ""
        for award in awards_regex.keys():
            s += "Award: " + ' '.join(x.capitalize() for x in award.split()) + "\n"
            s += "Presenters: " + ', '.join(x for x in (self.presenters[award] if self.presenters[award] else [])) + "\n"
            s += "Nominees: " + ', '.join(x if x else "Not found" for x in (self.get_award_nominees(award) if self.get_award_nominees(award) != None else [])) + "\n"
            s += "Winner: " + (str(self.winners[award]) if award in self.winners.keys() else "Not Found") + "\n\n"

        s += "Best Dressed: " + self.dresses["best"] + "\n"
        s += "Worst Dressed: " + self.dresses["worst"] + "\n"
        s += "Most Controversially Dressed: " + self.dresses["controversial"] + "\n\n"

        s += "Best Speech: " + self.speech["best"] + "\n"
        s += "Worst Speech: " + self.speech["worst"] + "\n\n"

        return s

    def get_all_values(self):
        print("Getting hosts!")
        self.get_hosts()
        print("Getting award names!")
        self.get_award_names()
        print("Getting winners!")
        self.get_winners()
        print("Getting presenters!")
        self.get_presenters()
        print("Getting nominees!")
        self.get_nominees()
        print("Getting best dressed!")
        self.get_best_dressed()
        print("Getting speeches!")
        self.get_speeches()
        print("Generating the awards object!")
        self.get_awards()
        print("Removing presenters from the nominee list!")
        self.remove_presenters_from_nominees()
        print(self)

    def get_nominees(self):
        # self.nominee_people = get_person_nominees(self.tweets, self.first_names)
        # self.nominee_movies = get_nominee_movies(self.data)

        self.nominee_people = get_people_noms(self.tweets, self.first_names, self.presenters)
        self.nominee = self.nominee_people
        for award in awards_regex.keys():
            if award not in self.nominee.keys():
                self.nominee[award] = []

        for award in awards_regex.keys():
            if award in self.winners.keys():
                winner = self.winners[award]
                # print(award, winner)
                if award in self.nominee.keys():
                    if winner in self.nominee[award]:
                        self.nominee[award].remove(winner)

    def get_winners(self):
        # self.winners = get_person_winners(self.tweets, self.first_names)
        self.winners = get_winners(self.tweets, self.first_names)


    def get_award_names(self):
        self.award_names = get_award_names(self.tweets)
        # print(self.award_names)

    def get_hosts(self):
        self.hosts = get_hosts(self.tweets, self.first_names)
        # print(self.hosts)

    def get_presenters(self):
        self.presenters = get_presenters(self.tweets, self.first_names, self.winners)

        for award, presenters in self.presenters.items():
            if not presenters:
                self.presenters[award] = []
        # self.presenters = get_presenters_new(self.tweets, self.first_names, self.winners)
        # for award, presenters in self.presenters.items():
        #     if presenters and len(presenters) > 2:
        #         self.presenters[award] = presenters[:2]
        # print(self.presenters)

    def get_best_dressed(self):
        self.dresses = dress_sentiment(self.tweets, self.first_names)

    def get_speeches(self):
        self.speech = speech_sentiment(self.tweets, self.first_names)

    def get_award_nominees(self, award):
        if award in self.nominee_people:
            return self.nominee_people[award]
        else:
            return self.nominee_movies[award] if award in self.nominee_movies.keys() else None

    def remove_presenters_from_nominees(self):
        for award, presenters in self.presenters.items():
            if presenters:
                for presenter in presenters:
                    if award in self.nominee_people:
                        if presenter in self.nominee_people[award]:
                            self.nominee_people[award].remove(presenter)

    def get_awards(self):
        for award in awards_regex.keys():
            self.awards[award] = {"presenters": self.presenters[award] if award in self.presenters.keys() else None,
                                  "nominees": self.get_award_nominees(award),
                                  "winner": self.winners[award] if award in self.winners.keys() else None}

        self.awards["hosts"] = self.hosts
        self.awards["awardNames"] = self.award_names
        self.awards["bestDressed"] = self.dresses
        self.awards["speeches"] = self.speech

