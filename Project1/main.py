import json
from levenshtein import fuzzy_match


file = open('data/gg2020.json')

data = json.load(file)

awards = ["Best Motion Picture", "Best Performance by an Actress", "Best Performance by an Actor",
          "Best Performance by an Actress in a Supporting Role", "Best Performance by an Actor in a Supporting Role",
          "Best Director", "Best Screenplay", "Best Original Score", "Best Original Song", "Best Television Series"]
awards = [a.lower() for a in awards]

categories = ["Drama", "Musical or Comedy", "Animated", "Foreign Language"]
categories = [c.lower() for c in categories]

for tweet in data:
    text = tweet["text"].lower()
    sentence = text.split()
    if "won" in sentence:
        for award in awards:
            if award in text:
                print(text)
