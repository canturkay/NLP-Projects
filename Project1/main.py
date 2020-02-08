import json

from .get_nominee_names import get_nominee_names
from .get_award_names import get_award_names


class GGresponse:
    data = {}
    award_names = []
    awards = {}

    def __init__(self, path):
        file = open(path)
        data = json.load(file)

        self.data = data

    def get_nominees(self):
        person_nominee_names = get_nominee_names(self.data, self.award_names)

    def get_award_names(self):
        self.award_names = get_award_names(self.data)



