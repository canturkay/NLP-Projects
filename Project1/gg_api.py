'''Version 0.35'''
import json

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

from Project1.main import GGresponse

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    if year == 2013:
        return our_gg.hosts2013
    elif year == 2015:
        return our_gg.hosts2015


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    if year == 2013:
        return our_gg.award_names2013
    elif year == 2015:
        return our_gg.award_names2015

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    if year == 2013:
        return our_gg.nominees2013
    elif year == 2015:
        return our_gg.nominees2015

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    if year == 2013:
        return our_gg.winners2013
    elif year == 2015:
        return our_gg.winners2015


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    if year == 2013:
        return our_gg.presenters2013
    elif year == 2015:
        return our_gg.presenters2015


global data2013, data2015, tweets2013, tweets2015, first_names, our_gg
our_gg = None
data2013 = None
data2015 = None

tweets2013 = None
tweets2015 = None

first_names = None

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here

    global data2013, data2015, tweets2013, tweets2015, first_names
    file2013 = open("data/gg2013.json")
    data2013 = json.load(file2013)

    file2015 = open("data/gg2013.json")
    data2015 = json.load(file2015)

    keywords = ["get", "got", "win", "won", "host", "present", "nomin", "look", "dress", "want", "wish",
                     "hope", "should", "best"]

    data_text = [tweet["text"] for tweet in data2013]
    tweets2013 = []
    for line in data_text:
        if any(keyword in line.lower() for keyword in keywords):
            tweets2013.append(line)

    tweets2013 = tweets2013[:300000]


    data_text = [tweet["text"] for tweet in data2015]
    tweets2015 = []
    for line in data_text:
        if any(keyword in line.lower() for keyword in keywords):
            tweets2015.append(line)

    tweets2015 = tweets2015[:300000]

    file_first_names = open('data/names.json')
    first_names = json.load(file_first_names)

    print("Pre-ceremony processing complete.")
    return


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    global data2013, data2015, tweets2013, tweets2015, first_names, our_gg
    if data2013 == None or data2015 == None:
        pre_ceremony()
    our_gg = GGresponse(data2013, data2015, tweets2013, tweets2015, first_names)
    return

if __name__ == '__main__':
    main()
    print(get_presenters(2013))
    print(get_presenters(2015))
    print(get_awards(2013))
    print(get_awards(2015))
