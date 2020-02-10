import re
awards_regex = {"best screenplay - motion picture":
                    r'.*best screenplay.*motion picture',
                "best director - motion picture":
                    r'best director.*motion picture',
                "best performance by an actress in a television series - comedy or musical":
                    r'best performance.*actress.*(tv|television) series.*comedy.*musical',
                "best foreign language film":
                    r'best foreign language',
                "best performance by an actor in a supporting role in a motion picture":
                    r'best performance.*actor.*supporting.*motion picture',
                "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television":
                    r'best performance.*actress.*supporting.*series.*motion picture',
                "best motion picture - comedy or musical":
                    r'best motion picture .*comedy.*musical',
                "best mini-series or motion picture made for television":
                    r'best mini.*series.*(tv|television)',
                "best original score - motion picture":
                    r'best original score.*motion picture',
                "best performance by an actress in a television series - drama":
                    r'best performance.*actress.*(tv|television).*drama',
                "best performance by an actress in a motion picture - drama":
                    r'bet performance.*actress,*motion picture.*drama',
                "best performance by an actor in a motion picture - comedy or musical":
                    r'best performance.*actor.*motion picture.*comedy.*musical',
                "best motion picture - drama":
                    r'best motion picture.*drama',
                "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television":
                    r'best performance.*actor.*supporting.*series.*motion picture.*made for (tv|television)',
                "best performance by an actress in a supporting role in a motion picture":
                    r'best performance.*actress.*supporting.*motion picture',
                "best television series - drama":
                    r'best [tv|television] series.*drama',
                "best performance by an actor in a mini-series or motion picture made for television":
                    r'best performance.*actor.*series.*motion picture.*made for(tv|television)',
                "best performance by an actress in a mini-series or motion picture made for television":
                    r'best performance.*actress.*series.*motion picture.*made for (tv|television)',
                "best animated feature film":
                    r'best animated feature film',
                "best original song - motion picture":
                    r'best original song.*motion picture',
                "best performance by an actor in a motion picture - drama":
                    r'best performance.*actor.*motion picture.*drama',
                "best television series - comedy or musical":
                    r'best [tv|television] series.*comedy.*musical',
                "best performance by an actor in a television series - drama":
                    r'best performance.*actor.*(tv|television) series.*drama',
                "best performance by an actor in a television series - comedy or musical":
                    r'best performance.*actor.*(tv|television) series.*comedy.*musical'
                }

person_awards_regex = {"best screenplay - motion picture":
                    r'.*best screenplay.*motion picture',
                "best director - motion picture":
                    r'best director.*motion picture',
                "best performance by an actress in a television series - comedy or musical":
                    r'best performance.*actress.*[tv|television] series.*comedy.*musical',
                "best performance by an actor in a supporting role in a motion picture":
                    r'best performance.*actor.*supporting.*motion picture',
                "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television":
                    r'best performance.*actress.*supporting.*series.*motion picture',
                "best original score - motion picture":
                    r'best original score.*motion picture',
                "best performance by an actress in a television series - drama":
                    r'best performance.*actress.*[tv|television].*drama',
                "best performance by an actress in a motion picture - drama":
                    r'bet performance.*actress,*motion picture.*drama',
                "best performance by an actor in a motion picture - comedy or musical":
                    r'best performance.*actor.*motion picture.*comedy.*musical',
                "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television":
                    r'best performance.*actor.*supporting.*series.*motion picture.*made for [tv|television]',
                "best performance by an actress in a supporting role in a motion picture":
                    r'best performance.*actress.*supporting.*motion picture',
                "best performance by an actor in a mini-series or motion picture made for television":
                    r'best performance.*actor.*series.*motion picture.*made for[tv|television]',
                "best performance by an actress in a mini-series or motion picture made for television":
                    r'best performance.*actress.*series.*motion picture.*made for [tv|television]',
                "best original song - motion picture":
                    r'best original song.*motion picture',
                "best performance by an actor in a motion picture - drama":
                    r'best performance.*actor.*motion picture.*drama',
                "best performance by an actor in a television series - drama":
                    r'best performance.*actor.*[tv|television] series.*drama',
                "best performance by an actor in a television series - comedy or musical":
                    r'best performance.*actor.*[tv|television] series.*comedy.*musical'
                }

movie_awards_regex = {"best screenplay - motion picture":
                    r'.*best screenplay.*motion picture',
                "best foreign language film":
                    r'best foreign language',
                "best motion picture - comedy or musical":
                    r'best motion picture .*comedy.*musical',
                "best mini-series or motion picture made for television":
                    r'best mini.*series.*(tv|television)',
                "best original score - motion picture":
                    r'best original score.*motion picture',
                "best motion picture - drama":
                    r'best motion picture.*drama',
                "best television series - drama":
                    r'best [tv|television] series.*drama',
                "best animated feature film":
                    r'best animated feature film',
                "best original song - motion picture":
                    r'best original song.*motion picture',
                "best television series - comedy or musical":
                    r'best [tv|television] series.*comedy.*musical',
                }

for key in awards_regex.keys():
    awards_regex[key] = re.compile(awards_regex[key])


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


