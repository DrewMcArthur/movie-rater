""" contains functions that, given a row of data, will filter unnecessary 
    information and reformat data in a way that allows an AI to process it
    more easily

    clean_data.py
"""

def filterHeaders(row):
    """ given a row (dict), remove unnecessary columns from data """
    data = {}
    goodHeaders = [ 'adult', 'budget', 'genres', 'overview', 'title', 
                    'popularity', 'production_companies', 'release_date', 
                    'production_countries', 'runtime', 'spoken_languages', 
                    'status', 'tagline', 'vote_average', 'vote_count', 'year', 
                    'rated', 'released', 'genre', 'language', 'country', 
                    'awards', 'ratings', 'metascore', 'imdbrating', 'imdbvotes',
                    'type', 'dvd', 'boxoffice', 'production' ]

    # filter out useless information
    for key, val in row.items():
        if key in goodHeaders:
            data.update({key: val})

    return data

def shapeDatum(row):
    """ given one row of data, return: (list of input data, label) """
    label = row['revenue']

    # remove unwanted columns
    row = clean_data.filterHeaders(row)

    data = row.items()

    # sort the data by key
    data.sort(lambda item: item[0])

    # return a list of the data values and the label
    return ([val for key, val in data], label)

