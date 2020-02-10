import json

from Project1.get_nominee_names import get_nominee_names
from .get_award_names import get_award_names
# from .nominees import
from .host import get_hosts
from .presenter import get_presenters
from .get_best_dressed import dress_sentiment
from .regex import search_award


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

    award_names = []
    hosts = []
    presenters = {}
    nominee_people = {}
    nominee_movies = {}

    winners = {}

    awards = {}

    dresses = {}

    first_names = []

    def __init__(self, path):
        file = open(path)
        data = json.load(file)

        file_first_names = open('data/names.json')
        self.first_names = json.load(file_first_names)

        self.data_text = [tweet["text"] for tweet in data]

        self.data = data
        self.get_hosts()
        self.get_award_names()
        self.get_presenters()
        self.get_nominees()
        self.best_dressed()
        

    def get_nominees(self):
        self.nominee_people = get_nominee_names(self.data_text)
        # self.nominee_movies = get_nominee_movies(self.data)

    def get_award_names(self):
        self.award_names = get_award_names(self.data)

    def get_hosts(self):
        self.hosts = get_hosts(self.data)

    def get_presenters(self):
        self.presenters = get_presenters(self.data, self.award_names)

    def get_best_dressed(self):
        self.dresses = dress_sentiment(self.data)

    def get_award_nominees(self, award):
        if award in self.nominee_people:
            return self.nominee_people[award]
        else:
            return self.nominee_movies[award]

    def get_awards(self):
        for award in self.award_names:
            self.awards[award] = {"presenters": self.presenters[award],
                                  "nominees": self.get_award_nominees(award),
                                  "winner": self.winners}

        self.awards["Hosts"] = self.hosts


print(search_award("best performance actress drama"))

gg = GGresponse("data/gg2013.json")
print(gg.awards)