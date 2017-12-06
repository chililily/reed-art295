"""Visualizing Twitter Topics Across America"""

from data import load_tweets
from datetime import datetime
from geo import us_states, us_state_pop, geo_distance, make_position, longitude, latitude
from maps import draw_state, wait
import random


################################
# Phase 1: Working With Tweets #
################################

# The tweet abstract data type, implemented as a dictionary.

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    >>> tweet_string(t)
    '"just ate lunch" @ (38, 74)'
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    return tweet['text']

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    return tweet['time']

def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    return make_position(tweet['latitude'], tweet['longitude'])

### === +++ ABSTRACTION BARRIER +++ === ###

def tweet_string(tweet):
    """Return a string representing a functional tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)


#################################
# Phase 2: The Geometry of Maps #
#################################

def check_intersect(point, segstart, segend):
    """Takes three positions, a point and two endpoints of a line 
    segment. Checks whether the ray pointing due east from 
    point goes through the line segment from segstart to segend"""
    #y = latitude, x = longitude
    x_init, y_init = longitude(segstart), latitude(segstart)
    x_final, y_final = longitude(segend), latitude(segend)
    x_point, y_point = longitude(point), latitude(point)
    if y_init < latitude(point) < y_final or y_final < latitude(point) < y_init: #checks if point's latitude is in latitudinal range of line segment
        if x_init == x_final:
            if x_point < x_init: #equal case unnecessary since point is never on edge of polygon
                return True
            else:
                return False
        else:
            b = (y_final - y_init)/(x_final - x_init) #dy/dx = (y_final - y_init)/(x_final - x_init)
            c = y_init - b*x_init #y = bx + c => c = y - bx; plugs in initial point
            y = latitude(point)
            x_seg = (y-c)/b
            if x_seg > x_point:
                return True
            else:
                return False
    else:
        return False

def is_in_state(point, state):
    """Finds if a point (position) is inside a state (list of polygons).
    Uses the ray casting algorithm at http://en.wikipedia.org/wiki/Point_in_polygon
    Whether a side intersects the ray is checked with check_intersect """
    state = us_states[state]
    for shape in state: #loops through polygons
        p, n = 0, 0
        while p < len(shape) - 1: #loops through points in polygon. Last index in list is equal to one less than the length of the list
            if check_intersect(point, shape[p], shape[p+1]):
                #segstart = first point, segend = second point, then segstart = second point, segend = third point
                n += 1
            p += 1
        if n%2 != 0:
            return True
    return False


#####################################
# Phase 3: The Tweets of the Nation #
#####################################

def count_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their state of origin.

    The keys of the returned dictionary are state names, and the values are
    normalized per capita tweet frequencies. You may use the dictionary
    us_state_pop, which associates state abbreviation keys with 2013 estimated
    population for the given state.

    tweets -- a sequence of tweet abstract data types
    """
    tweets_by_state = {'AL': 0, 'AK': 0, 'AZ': 0, 'AR': 0, 'CA': 0, 'CO': 0, 'CT': 0, 'DE':0, 'FL': 0, 'GA': 0, 'HI': 0, 'ID': 0, 'IL': 0, 'IN': 0, 'IA': 0, 'KS': 0, 'KY': 0, 'LA': 0, 'ME': 0, 'MD': 0, 'MA': 0, 'MI': 0, 'MN': 0, 'MS': 0, 'MO': 0, 'MT': 0, 'NE': 0, 'NV': 0, 'NH': 0, 'NJ': 0, 'NM': 0, 'NY': 0, 'NC': 0, 'ND': 0, 'OH': 0, 'OK': 0, 'OR': 0, 'PA': 0, 'RI': 0, 'SC': 0, 'SD': 0, 'TN': 0, 'TX': 0, 'UT': 0, 'VT': 0, 'VA': 0, 'WA': 0, 'WV': 0, 'WI': 0, 'WY': 0, 'DC': 0}
    for tweet in tweets: #loops through all tweets
        for state in us_states: #for each tweet, loops through all states
            if is_in_state(tweet_location(tweet), state): #finds if tweet is in state being checked
                tweets_by_state[state] += 1 #adds 1 to dict value if true
                break #stops checking if state has been found
    for state in tweets_by_state:
        tweets_by_state[state] = tweets_by_state[state]/us_state_pop[state]
    maximum = max(tweets_by_state.values())
    for state in tweets_by_state:
        tweets_by_state[state] = tweets_by_state[state]/maximum
    return tweets_by_state

####################
# Phase 4: Queries #
####################

def canada_query(text):
    """Return True if text contains "canada" as a substring.
    Results should not be case-sensitive.  When text includes "CAnada", 
    for example, should return True.
    """
    if 'canada' in text.casefold():
        return True
    else:
        return False


def make_searcher(term):
    """Returns a test that searches for term as a substring of a given string.
    Results should not be case-sensitive.
    For example, makesearcher("canada") should behave identically to canada_query.
    """
    def term_query(text):
        if term.casefold() in text.casefold():
            return True
        else:
            return False
    return term_query


def mexico_query(text):
    """Returns true if "mexico" is included as a substring and "new" is not.
    Again, results should not be case-sensitive.
    """
    if make_searcher("mexico")(text) and not make_searcher("new")(text):
        return True
    else:
        return False


#########################
# Map Drawing Functions #
#########################

def draw_state_frequencies(state_frequencies):
    """Draw all U.S. states in colors corresponding to their frequency value."""
    for name, shapes in us_states.items():
        frequency = state_frequencies.get(name, None)
        draw_state(shapes, frequency)

def draw_map_for_query(test, new_file_name=None):
    if new_file_name == None:
        random.seed()
        new_file_name = str(random.randint(0, 1000000000))
    """Draw the frequency map corresponding to the tweets that pass the test.
    """
    tweets = load_tweets(make_tweet, test, new_file_name)
    tweets_by_state = count_tweets_by_state(tweets)
    draw_state_frequencies(tweets_by_state)
    wait()



#################################
# Phase 5: Use what you've done #
#################################

# Uncomment (and edit) the line below to create a map based on a query of your choice
draw_map_for_query(make_searcher("communist"))