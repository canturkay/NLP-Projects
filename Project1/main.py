import json

from get_nominee_names import get_nominee_names
from  get_award_names import get_award_names
from  host import get_hosts
from  presenter import get_presenters
from  get_best_dressed import dress_sentiment
from  regex import search_award, awards_regex
from  get_award_keyword import get_person_nominees, get_presenters_new, get_person_winners
from  winners import get_winners

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
    data_text = []
    tweets = []

    keywords = []

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
        print("Loading data!")
        file = open(path)
        data = json.load(file)

        print("Loading first names file!")
        file_first_names = open('data/names.json')
        self.first_names = json.load(file_first_names)

        self.data_text = [tweet["text"] for tweet in data]

        self.keywords = ["get", "got", "win", "won", "host", "present", "nomin", "look", "dress", "want", "wish",
                         "hope", "should", "best"]

        for line in self.data_text:
            if any(keyword in line.lower() for keyword in self.keywords):
                self.tweets.append(line)

        self.tweets = self.tweets[:300000]

        self.data = data
        print("Getting hosts!")
        self.get_hosts()
        print("Getting award names!")
        self.get_award_names()
        print("Getting presenters!")
        self.get_presenters()
        print("Getting nominees!")
        self.get_nominees()
        print("Getting winners!")
        self.get_winners()
        print("Getting best dressed!")
        self.get_best_dressed()
        print("Generating the awards object!")
        self.get_awards()
        print("Removing presenters from the nominee list!")
        self.remove_presenters_from_nominees()
        print(self)

    def __str__(self):
        s = ""
        for award in awards_regex.keys():
            s += "Award: " + ' '.join(x.capitalize() for x in award.split()) + "\n"
            s += "Presenters: " + ', '.join(x for x in (self.presenters[award] if award in
                                                                                 self.presenters.keys() else [])) + "\n"
            s += "Nominees: " + ', '.join(x for x in (str(self.get_award_nominees(award)) if
                                                         self.get_award_nominees(award) else ["Not Found"])) + "\n"
            s += "Winner: " + (str(self.winners[award]) if award in self.winners.keys() else "Not Found") + "\n\n"

        s += "Best Dressed: " + self.dresses["best"] + "\n"
        s += "Worst Dressed: " + self.dresses["worst"] + "\n"
        s += "Most Controversially Dressed: " + self.dresses["controversial"] + "\n\n"

        s += "Fetched Award Names: " + ', '.join(x for x in self.award_names) + "\n"
        return s

    def get_nominees(self):
        self.nominee_people = get_person_nominees(self.tweets, self.first_names)
        # print(self.nominee_people)
        # self.nominee_movies = get_nominee_movies(self.data)

    def get_winners(self):
        # self.winners = get_person_winners(self.tweets, self.first_names)
        self.winners = get_winners(self.tweets, self.first_names)
        for award in awards_regex.keys():
            if award not in self.winners.keys():
                nominees = self.nominee_people[award] if award in self.nominee_people.keys() else None
                if nominees and len(nominees) == 1:
                    # print(award, nominees[0])
                    self.winners[award] = nominees[0]
            else:
                winner = self.winners[award]
                # print(award, winner)
                if award not in self.nominee_people.keys():
                    self.nominee_people[award] = [winner]
                elif winner not in self.nominee_people[award]:
                    self.nominee_people[award].append(winner)
        # print(self.winners)
    # def get_aaron_winners(self): 
    #     self.aaron_winners = get_award_names
    def get_award_names(self):
        self.award_names = get_award_names(self.tweets)
        # print(self.award_names)

    def get_hosts(self):
        self.hosts = get_hosts(self.tweets, self.first_names)
        # print(self.hosts)

    def get_presenters(self):
        #self.presenters = get_presenters(self.tweets, self.first_names)
        self.presenters = get_presenters_new(self.tweets, self.first_names)
        for award, presenters in self.presenters.items():
            if len(presenters) > 2:
                self.presenters[award] = presenters[:2]
        print(self.presenters)

    def get_best_dressed(self):
        self.dresses = dress_sentiment(self.tweets, self.first_names)

    def get_award_nominees(self, award):
        if award in self.nominee_people:
            return self.nominee_people[award]
        else:
            return self.nominee_movies[award] if award in self.nominee_movies.keys() else None

    def remove_presenters_from_nominees(self):
        for award, presenters in self.presenters.items():
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


gg = GGresponse("data/gg2013.json")
# print(gg.awards)
