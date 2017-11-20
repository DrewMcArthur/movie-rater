"""
    scrape-themoviedb.py

    gets movie data from omdb
    currently iterates through days to get list of movie IDs 
        from their daily data dump
"""

import urllib.request, requests, gzip, ast, yaml

config = yaml.safe_load(open("config.yml"))
TMDB_API_KEY = config['tmdbAPIKEY']
OMDB_API_KEY = config['omdbAPIKEY']

def getIDs(listOfDates):
    """ return a list of movie IDs
        given listOfDates, a list of tuples in the format (MM, DD) """
    IDs = []
    for m, d in listOfDates:
        uri = "http://files.tmdb.org/p/exports/movie_ids_{:02d}_{:02d}_2017.json.gz".format(m, d)
        print(uri)

        # download the gz file with ids and load the compressed data into a string
        f = urllib.request.urlopen(uri)
        zipped_content = f.read()

        # steps to uncompress:
        # * uncompress string using gzip
        # * decode string with utf-8
        # * split string by newline into list of strings
        # * replace JSON bools to PYTHON bools (true -> True)
        # * remove last line (empty string)
        # * eval each line to get JSON object
        # * get id key from JSON row
        unzipped_content = gzip.decompress(zipped_content).decode('utf-8').split("\n")[:-1]

        IDs += [eval(line.replace("true","True").replace("false","False"))['id']
                                for line in unzipped_content]
    return IDs

def getTMDBData(ID):
    """ given a movie ID, use the movie database API to retrieve data """
    uri = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US"
    return requests.get(uri.format(ID, TMDB_API_KEY)).json()

def getOMDBData(ID):
    """ given an IMDB movie id, use the omdb api to retrieve data """
    uri = "http://www.omdbapi.com/?i={}&apikey={}"
    return requests.get(uri.format(ID, OMDB_API_KEY)).json()

def getAllData(TMDBID):
    """ given a TMDb movie ID, fetch data from TMDb and OMDb and merge the data.
    """
    data = getTMDBData(TMDBID)

    # get the OMDb data on the movie, make all keys lowercase, and skip
    # dict entries that already exist in data (e.g. title, runtime)
    # we skip them because TMDb saves runtime length as int, OMDb uses "XX min" #dumb
    omdb_data = dict([(k.lower(), v) for k, v in 
                        getOMDBData(data['imdb_id']).items() 
                        if k.lower() not in data])

    # merge data
    data.update(omdb_data)
    return data

def json_print(json, levels=0):
    """ given some json data, print it out nicely """
    if levels == 0:
        print("{")
        json_print(json, levels + 1)
        print("}")
        return 

    indent = "\t" * levels
    if type(json) is dict:
        for key, value in json.items():
            if type(value) is list:
                print(indent + "{ " + key + ": [")
                for el in value:
                    json_print(el, levels + 1)
                print(indent + "]},")
            elif type(value) is dict:
                print(indent + "{ " + key + ": ")
                json_print(value, levels + 1)
                print(indent + "},")
            else:
                print(indent + "{ " + key + ": " + str(value) + " },")

    elif type(json) is list:
        print(indent + "[")
        for obj in json:
            json_print(obj, levels + 1)
        print("],")

    else:
        print(json)

def main():
    dates = [(11, 17)]

    #IDs = getIDs(dates)
    #tmdb_data = [getTMDBData(ID) for ID in IDs]

    #IMDB_IDS = [row['imdb_id'] for row in tmdb_data]
    #omdb_data = [getOMDBData(ID) for ID in IMDB_IDS]

    row_tmdb = getTMDBData(35)
    row_omdb = getOMDBData(row_tmdb['imdb_id'])

    json_print(row_tmdb)
    json_print(row_omdb)

    print("=== start merged data ===")

    json_print(getAllData(35))

if __name__ == "__main__":
    main()
