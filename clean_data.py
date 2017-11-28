""" contains functions that, given a row of data, will filter unnecessary 
    information and reformat data in a way that allows an AI to process it
    more easily

    clean_data.py
"""

from scrape import json_print

def filterHeaders(row):
    """ given a row (dict), remove unnecessary columns from data """
    goodHeaders = [ 'adult', 'budget', 'genres', 'overview', 'title', 'ratings',
                    'popularity', 'production_companies', 'release_date', 'dvd',
                    'released', 'genre', 'country', 'year', 'awards', 'runtime',
                    'production_countries', 'language', 'tagline', 'status', 
                    'vote_average', 'vote_count', 'boxoffice', 'production',
                    'metascore', 'imdbrating', 'imdbvotes', 'type', 'rated' ]

    # filter out useless information
    data = {key: val for key, val in row.items() 
            if key in goodHeaders}

    return data

def processIDList(listVals):
    """ given a list of values of a col for a movie, return a list of the values
        input format: [{'id': XX, 'name': NAME}]
    """
    return [x['name'] for x in listVals]

def processRatings(row):
    """ given a row, process data in the ratings column and create new columns 
        based on the information found. """
    sources = {'Internet Movie Database': ('IMDb_rating', 
                                           lambda v: float(v[:-3])/10),
            'Rotten Tomatoes': ('RT_rating', lambda v: float(v[:-1])/100), 
            'Metacritic': ('MC_rating', lambda v: float(v[:-4])/100)}
    for rating in row['ratings']:
        if rating['Source'] not in sources:
            print("Error! {} not a supported source, quitting..."
                    .format(rating['Source']))
            exit()
        else:
            row[sources[rating['Source']][0]] = \
                sources[rating['Source']][1](rating['Value'])
    row.pop('ratings', None)

def shapeDatum(row):
    """ given one row of data, return: (list of input data, label) """
    label = row['revenue']

    # remove unwanted columns
    row = filterHeaders(row)


    # flatten lists found in columns that contain lists of data
    #       [{id:XX, name:XXXX},{id:YY, name:YYYY}] -> [XXXX, YYYY]
    listCols = ['genres', 'production_companies', 'production_countries', 
                'spoken_languages']
    for col in listCols:
        row[col] = processIDList(row[col])

    row['ratings'] = processRatings(row)

    if ", ".join(row['spoken_languages']) != row['language']:
        print("DOESN'T MATCH:", row['title'])
        print(row['spoken_languages'])
        print("           == " + row['language'])

    data = list(row.items())

    # sort the data by key
    data.sort(key=lambda item: item[0])

    # return a list of the data values and the label
    return ([val for key, val in data], label)

