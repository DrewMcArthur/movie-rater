"""
    scrape-themoviedb.py

    gets movie data from omdb
    currently iterates through days to get list of movie IDs 
        from their daily data dump
"""

import urllib.request, requests, gzip, ast, yaml

config = yaml.safe_load(open("config.yml"))
APIKEY = config['tmdbAPIKEY']

# the movie database: tmdb

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

def getMovieData(ID):
    """ given a movie ID, use the movie database API to retrieve data """
    uri = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US"
    return requests.get(uri.format(ID, APIKEY)).json()

def main():
    dates = [(11, 17)]
    IDs = getIDs(dates)

    print("We got {} movie IDs!!!".format(len(IDs)))
    print(getMovieData(IDs[0]))
    #data = [getMovieData(ID) for ID in IDs]
    #print(data[0])

if __name__ == "__main__":
    main()
