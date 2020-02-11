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
    data2013 = {}
    tweets2013 = []

    hosts2013 = []
    presenters2013 = {}
    nominee_people2013 = {}
    nominee_movies2013 = {}

    winners2013 = {}
    awards2013 = {}
    dresses2013 = {}
    speech2013 = {}

    data2015 = {}
    tweets2015 = []

    hosts2015 = []
    presenters2015 = {}
    nominee_people2015 = {}
    nominee_movies2015 = {}

    winners2015 = {}
    awards2015 = {}
    dresses2015 = {}
    speech2015 = {}


    first_names = []
    keywords = []
    award_names = []

    def __init__(self, data2013, data2015, tweets2013, tweets2015, first_names):
        print("Loading data!")
        print("Loading first names file!")

        self.first_names = first_names

        self.tweets2013 = tweets2013
        self.tweets2015 = tweets2015

        self.data2013 = data2013
        self.data2015 = data2015

        print("Getting hosts!")
        self.get_hosts()
        print("Getting award names!")
        self.get_award_names()
        print("Getting nominees!")
        self.get_nominees()
        print("Getting winners!")
        self.get_winners()
        print("Getting presenters!")
        self.get_presenters()
        print("Getting best dressed!")
        self.get_best_dressed()
        print("Getting speeches!")
        self.get_speeches()
        print("Generating the awards object!")
        self.get_awards()
        print("Removing presenters from the nominee list!")
        self.remove_presenters_from_nominees()
        print(self)

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

        s += "Fetched Award Names: " + ', '.join(x for x in self.award_names) + "\n"
        return s

    def get_nominees(self):
        self.nominee_people2013 = get_person_nominees(self.tweets2013, self.first_names)
        self.nominee_people2015 = get_person_nominees(self.tweets2015, self.first_names)
        # print(self.nominee_people)
        # self.nominee_movies = get_nominee_movies(self.data)

    def get_winners(self):
        # self.winners = get_person_winners(self.tweets, self.first_names)
        self.winners2013 = get_winners(self.tweets2013, self.first_names)
        for award in awards_regex.keys():
            if award not in self.winners2013.keys():
                nominees = self.nominee_people2013[award] if award in self.nominee_people2013.keys() else None
                if nominees and len(nominees) == 1:
                    # print(award, nominees[0])
                    self.winners2013[award] = nominees[0]
            else:
                winner = self.winners2013[award]
                # print(award, winner)
                if award not in self.nominee_people2013.keys():
                    self.nominee_people2013[award] = [winner]
                elif winner not in self.nominee_people2013[award]:
                    self.nominee_people2013[award].append(winner)


        self.winners2015 = get_winners(self.tweets2015, self.first_names)
        for award in awards_regex.keys():
            if award not in self.winners2015.keys():
                nominees = self.nominee_people2015[award] if award in self.nominee_people2015.keys() else None
                if nominees and len(nominees) == 1:
                    # print(award, nominees[0])
                    self.winners2015[award] = nominees[0]
            else:
                winner = self.winners2015[award]
                # print(award, winner)
                if award not in self.nominee_people2015.keys():
                    self.nominee_people2015[award] = [winner]
                elif winner not in self.nominee_people2015[award]:
                    self.nominee_people2015[award].append(winner)
        # print(self.winners)

    def get_award_names(self):
        self.award_names2013 = get_award_names(self.tweets2013)
        self.award_names2015 = get_award_names(self.tweets2015)
        # print(self.award_names)

    def get_hosts(self):
        self.hosts2013 = get_hosts(self.tweets2013, self.first_names)
        self.hosts2013 = get_hosts(self.tweets2015, self.first_names)
        # print(self.hosts)

    def get_presenters(self):
        self.presenters2013 = get_presenters(self.tweets2013, self.first_names, self.winners2013)
        self.presenters2015 = get_presenters(self.tweets2015, self.first_names, self.winners2015)
        # self.presenters = get_presenters_new(self.tweets, self.first_names, self.winners)
        # for award, presenters in self.presenters.items():
        #     if presenters and len(presenters) > 2:
        #         self.presenters[award] = presenters[:2]
        # print(self.presenters)

    def get_best_dressed(self):
        self.dresses2013 = dress_sentiment(self.tweets2013, self.first_names)
        self.dresses2015 = dress_sentiment(self.tweets2015, self.first_names)

    def get_speeches(self):
        self.speech2013 = speech_sentiment(self.tweets2013, self.first_names)
        self.speech2015 = speech_sentiment(self.tweets2015, self.first_names)

    def get_award_nominees(self, award, year):
        if year == 2013:
            if award in self.nominee_people2013:
                return self.nominee_people2013[award]
            else:
                return self.nominee_movies2013[award] if award in self.nominee_movies2013.keys() else None
        elif year == 2015:
            if award in self.nominee_people2015:
                return self.nominee_people2015[award]
            else:
                return self.nominee_movies2015[award] if award in self.nominee_movies2015.keys() else None

    def remove_presenters_from_nominees(self):
        for award, presenters in self.presenters2013.items():
            if presenters:
                for presenter in presenters:
                    if award in self.nominee_people2013:
                        if presenter in self.nominee_people2013[award]:
                            self.nominee_people2013[award].remove(presenter)

        for award, presenters in self.presenters2015.items():
            if presenters:
                for presenter in presenters:
                    if award in self.nominee_people2015:
                        if presenter in self.nominee_people2015[award]:
                            self.nominee_people2015[award].remove(presenter)

    def get_awards(self):
        for award in awards_regex.keys():
            self.awards2013[award] = {"presenters": self.presenters2013[award] if award in self.presenters2013.keys() else None,
                                  "nominees": self.get_award_nominees(award, 2013),
                                  "winner": self.winners2013[award] if award in self.winners2013.keys() else None}

        self.awards2013["hosts"] = self.hosts2013
        self.awards2013["awardNames"] = self.award_names2013
        self.awards2013["bestDressed"] = self.dresses2013
        self.awards2013["speeches"] = self.speech2013

        for award in awards_regex.keys():
            self.awards2015[award] = {"presenters": self.presenters2015[award] if award in self.presenters2015.keys() else None,
                                  "nominees": self.get_award_nominees(award, 2015),
                                  "winner": self.winners2015[award] if award in self.winners2015.keys() else None}

        self.awards2015["hosts"] = self.hosts2015
        self.awards2015["awardNames"] = self.award_names2015
        self.awards2015["bestDressed"] = self.dresses2015
        self.awards2015["speeches"] = self.speech2015

