import json
from levenshtein import fuzzy_match
from host import get_hosts
#check timestamps

file = open('data/gg2020.json')

data = json.load(file)

awards = ["Best Motion Picture", "Best Performance by an Actress", "Best Performance by an Actor",
          "Best Performance by an Actress in a Supporting Role", "Best Performance by an Actor in a Supporting Role",
          "Best Director", "Best Screenplay", "Best Original Score", "Best Original Song", "Best Television Series"]
#awards = [a.lower() for a in awards]

categories = ["Drama", "Musical or Comedy", "Animated", "Foreign Language"]
#categories = [c.lower() for c in categories]


