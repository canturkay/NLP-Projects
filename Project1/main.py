import json

from .get_nominee_names import get_nominee_names
from .get_award_names import get_award_names
# from .nominees import
from .host import get_hosts
from .presenter import get_presenters


class GGresponse:
    data = {}

    award_names = []
    hosts = []
    presenters = {}
    nominee_people = {}
    nominee_movies = {}

    awards = {}

    def __init__(self, path):
        file = open(path)
        data = json.load(file)

        self.data = data
        self.get_hosts()
        self.get_award_names()
        self.get_presenters()
        self.get_nominees()

    def get_nominees(self):
        self.nominee_people = get_nominee_names(self.data, self.award_names)
        # self.nominee_movies = get_nominee_movies(self.data)

    def get_award_names(self):
        self.award_names = get_award_names(self.data)

    def get_hosts(self):
        self.hosts = get_hosts(self.data)

    def get_presenters(self):
        self.presenters = get_presenters(self.data, self.award_names)



