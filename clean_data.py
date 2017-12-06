""" contains functions that, given a row of data, will filter unnecessary 
    information and reformat data in a way that allows an AI to process it
    more easily

    clean_data.py
"""

from scrape import json_print

def filterHeaders(row):
    """ given a row (dict), remove unnecessary columns from data """
    goodHeaders = [ 'adult', 'budget', 'genres', 'ratings',
                    'popularity', 'production_companies', 
                    'genre', 'country', 'year', 'runtime',
                    'production_countries', 'language',
                    'vote_average', 'vote_count', 'production',
                    'imdbvotes', 'type', 'rated', 'spoken_languages']

    if row['status'] != "Released":
        print("Weird, this movie's status is", row['status'])

    # filter out useless information
    data = {key: val for key, val in row.items() 
            if key in goodHeaders}

    for key in goodHeaders:
        if key not in data:
            data.update({"Err": "Missing header: {}".format(key)})
            return data
    return data

def processDictList(dictVals):
    """ given dicts of values of a col for a movie, return a list of the values
        input format: [{'id': XX, 'name': NAME}]
    """
    return [x['name'] for x in dictVals]

def consolidateCols(row, h1, h2):
    """ given a row and two headers, return the merged value of the two columns
    """
    if type(row[h1]) != list:
        row[h1] = row[h1].split(", ")
    if type(row[h2]) != list:
        row[h2] = row[h2].split(", ")

    row[h1] = list(set(row[h1] + row[h2]))
    del row[h2]

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
    del row['ratings']
    return row

def shapeDatum(row):
    """ given one row of data, return: (list of input data, label) """
    label = row['revenue']
    if label < 5000:
        row.update({"Err": "BADLABEL"})
        return (row, -1)

    # remove unwanted columns
    row = filterHeaders(row)

    if "Err" in row:
        return (row, label)

    row['adult'] = 1 if row['adult'] else 0

    # ratings, i.e. critical reviews
    row = processRatings(row)

    # rated, i.e. appropriate for what age level
    # if row['rated'] == "NOT RATED" or row['rated'] == "N/A":
        #row['rated'] = None

    row['imdbvotes'] = (int(row['imdbvotes'].replace(",",""))
                        if row['imdbvotes'].upper() != "N/A" else None)
    # not sure about using these numbers...
    #row['boxoffice'] = (int(row['boxoffice'][1:].replace(",","")) 
    #                    if row['boxoffice'] != "N/A" and row['boxoffice'] != 0 
    #                    else None)

    row['year'] = row['year'][:3] + "0"

    # flatten lists found in columns that contain lists of data
    #       [{id:XX, name:XXXX},{id:YY, name:YYYY}] -> [XXXX, YYYY]
    listCols = ['genres', 'production_companies', 'production_countries', 
                'spoken_languages']
    for col in listCols:
        row[col] = processDictList(row[col])

    # merge columns that contain the same information
    dupCols = [('production', 'production_companies'), 
               ('genre', 'genres'), 
               ('country', 'production_countries'), 
               ('language', 'spoken_languages')]
    for col, col2 in dupCols:
        consolidateCols(row, col, col2)

    return row, label
