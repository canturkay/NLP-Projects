import re
awards_regex = {"best screenplay - motion picture":
                    r'best screenplay',
                "best director - motion picture":
                    r'best director',
                "best performance by an actress in a television series - comedy or musical":
                    r'best.*actress.*(tv|television|series).*comedy',
                "best foreign language film":
                    r'best foreign language',
                "best performance by an actor in a supporting role in a motion picture":
                    r'best.*supporting.*actor.*(picture|movie|)',
                "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television":
                    r'best.*supporting.*actress.*series',
                "best motion picture - comedy or musical":
                    r'best.*(picture|movie) .*comedy',
                "best mini-series or motion picture made for television":
                    r'best.*(limited|mini).*series',
                "best original score - motion picture":
                    r'best original score',
                "best performance by an actress in a television series - drama":
                    r'best.*actress.*(tv|television).*drama',
                "best performance by an actress in a motion picture - drama":
                    r'best.*actress.*drama.*(film|movie|picture)',
                "best performance by an actor in a motion picture - comedy or musical":
                    r'best.*actor.*comedy.*(film|movie|picture)',
                "best performance by an actress in a motion picture - comedy or musical":
                    r'best.*actress.*comedy.*(film|movie|picture)',
                "best motion picture - drama":
                    r'best.*drama',
                "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television":
                    r'best.*supporting.*actor.*(series|picture).*(tv|television)',
                "best performance by an actress in a supporting role in a motion picture":
                    r'best.*supporting.*actress.*(film|movie|picture)',
                "best television series - drama":
                    r'best.*drama.*series',
                "best performance by an actor in a mini-series or motion picture made for television":
                    r'best.*actor*(mini|limited|picture).*(tv|television)',
                "best performance by an actress in a mini-series or motion picture made for television":
                    r'best.*actress.*(tv|television)',
                "best animated feature film":
                    r'best animated',
                "best original song - motion picture":
                    r'best original song',
                "best performance by an actor in a motion picture - drama":
                    r'best.*actor.*drama.*(film|movie|picture)',
                "best television series - comedy or musical":
                    r'best (tv|television).*comedy',
                "best performance by an actor in a television series - drama":
                    r'best.*actor.*(tv|television).*drama',
                "best performance by an actor in a television series - comedy or musical":
                    r'best.*actor.*(tv|television).*comedy',
                "cecil b. demille award":
                r'(cecil|lifetime).*award'
                }

person_awards_regex = {"best screenplay - motion picture":
                       r'best screenplay',
                       "best director - motion picture":
                       r'best director',
                       "best performance by an actress in a television series - comedy or musical":
                       r'best (?!supporting).*actress.*(tv|television|series).*comedy',
                       "best performance by an actor in a supporting role in a motion picture":
                       r'best.*supporting.*actor.*(picture|movie|film)',
                       "best performance by an actress in a motion picture - comedy or musical":
                       r'best (?!supporting).*actress.*comedy.*(film|movie|picture)',
                       "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television":
                       r'best.*supporting.*actress.*series', 
                       "best performance by an actress in a television series - drama":
                       r'best (?!supporting).*actress.*(tv|television).*drama',
                       "best performance by an actress in a motion picture - drama":
                       r'best (?!supporting).*actress.*drama.*(film|movie|picture)',
                       "best performance by an actor in a motion picture - comedy or musical":
                       r'best (?!supporting).*actor.*comedy.*(film|movie|picture)',
                       "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television":
                       r'best.*supporting.*actor.*(series|picture).*(tv|television)',
                       "best performance by an actress in a supporting role in a motion picture":
                       r'best.*supporting.*actress.*(film|movie|picture)',
                       "best performance by an actor in a mini-series or motion picture made for television":
                       r'best (?!supporting).*actor.*(tv|television)',
                       "best performance by an actress in a mini-series or motion picture made for television":
                       r'best (?!supporting).*actress.*(tv|television)',
                       "best performance by an actor in a motion picture - drama":
                       r'best (?!supporting).*actor.*drama.*(film|movie|picture)',
                       "best performance by an actor in a television series - drama":
                       r'best (?!supporting).*actor.*(tv|television).*drama',
                       "best performance by an actor in a television series - comedy or musical":
                       r'best (?!supporting).*actor.*(tv|television).*comedy',
                       "cecil b. demille award":
                       r'(cecil|lifetime).*award',
                       }

movie_awards_regex = {"best foreign language film":
                      r'best foreign language', 
                      "best original score - motion picture":
                      r'best original score',
                      "best motion picture - comedy or musical":
                      r'best.*(picture|movie) .*comedy',
                      "best mini-series or motion picture made for television":
                      r'best.*(limited|mini).*series',
                      "best motion picture - drama":
                      r'best.*drama', 
                      "best television series - drama":
                      r'best.*drama.*series', 
                      "best television series - comedy or musical":
                      r'best (tv|television).*comedy',
                      "best original song - motion picture":
                      r'best original song',
                      "best animated feature film":
                      r'best animated',
                      }

for key in awards_regex.keys():
    awards_regex[key] = re.compile(awards_regex[key])

def match_award(sentence, award):
    if awards_regex[award].search(sentence.lower()):
        return True
    return False


def search_award(sentence):
    sentence_lower = sentence.lower()

    for award in awards_regex.keys():
        if awards_regex[award].search(sentence_lower):
            return award

    return None


def search_person_award(sentence):
    sentence_lower = sentence.lower()
    for award in person_awards_regex.keys():
        if awards_regex[award].search(sentence_lower):
            return award
    return None


def search_movie_award(sentence):
    sentence_lower = sentence.lower()
    for award in movie_awards_regex.keys():
        if awards_regex[award].search(sentence_lower):
            return award
    return None


