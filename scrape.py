"""
    scrape-themoviedb.py

    gets movie data from omdb
    currently iterates through days to get list of movie IDs 
        from their daily data dump
"""

import urllib.request, requests, gzip, ast, yaml, pickle, time, os.path

config = yaml.safe_load(open("config.yml"))
TMDB_API_KEY = config['tmdbAPIKEY']
OMDB_API_KEY = config['omdbAPIKEY']

def getIDs(m, d):
    """ return a list of movie IDs
        given listOfDates, a list of tuples in the format (MM, DD) """
    IDs = []

    uri = "http://files.tmdb.org/p/exports/movie_ids_{:02d}_{:02d}_2017.json.gz"
    uri = uri.format(m, d)
    print("Retrieving data export from:")
    print("     " + uri)

    # download the gz file with ids and load the compressed data
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
    unzipped_content = (gzip.decompress(zipped_content)
                            .decode('utf-8')
                            .split("\n")[:-1])

    IDs += [eval(line.replace("true","True").replace("false","False"))['id']
                            for line in unzipped_content]
    return list(set(IDs))

def getDataFromDB(ID, DB):
    """ given a movie ID, use an API to retrieve data from a specified DB """
    if type(ID) is list:
        return [getDataFromDB(i, DB) for i in ID]

    # database-specific uri calculations
    # tbh not really sure of url vs uri, but uri sounds cooler
    if DB == "TMDB":
        uri = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US"
        uri = uri.format(ID, TMDB_API_KEY)
    elif DB == "OMDB":
        uri = "http://www.omdbapi.com/?i={}&apikey={}"
        uri = uri.format(ID, OMDB_API_KEY)
    else:
        print("Error: {} not a supported database.".format(DB))
        exit()

    # get the data, and handle missing data
    r = requests.get(uri)
    if r.status_code == 200:
        # print("Success! Retrieved movie ID {} from DB {}.".format(ID, DB))
        return r.json()
    elif r.status_code == 524:
        print("{} Server timeout on ID {}, waiting and then retrying..."
                    .format(DB, ID))
        time.sleep(1)
        return getDataFromDB(ID, DB)
    else:
        # if there's an error,
        res = input("Err retrieving movie {} from {}, status code: {}. Retry? "
                    .format(ID, DB, r.status_code))
        # either try again
        if res == "" or res.lower() == "y":
            print("     Retrying...")
            return getDataFromDB(ID, DB)
        # or give some json data describing the error.
        else:
            print("     Skipping.")
            return {"ID": ID, "error code": r.status_code, "database": DB,
                    "comment": "Error retrieving data."}

def getAllData(TMDBID):
    """ given a TMDb movie ID, fetch data from TMDb and OMDb and merge the data.
        if TMDBID is a list, we return a list of the data for each ID """

    if type(TMDBID) is list:
        data = []
        for i, ID in enumerate(TMDBID):
            data.append(getAllData(ID))
            print("Fetched data for {0:.1f}% of movies."
                            .format(i/(len(TMDBID)/100)), end="\r")
        return data

    data = getDataFromDB(TMDBID, "TMDB")

    # get the OMDb data on the movie, make all keys lowercase, and skip
    # dict entries that already exist in data (e.g. title, runtime)
    # we skip them because TMDb saves runtime length as int, OMDb uses "XX min" 
    # dumb
    omdb_data = dict([(k.lower(), v) for k, v in 
                        getDataFromDB(data['imdb_id'], "OMDB").items() 
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

    indent = "  " * levels
    if type(json) is dict:
        print(indent + "{")
        for key, value in json.items():
            if type(value) is list:
                print(indent + "  " + key + ": [")
                for el in value:
                    json_print(el, levels + 2)
                print(indent + "  ],")
            elif type(value) is dict:
                print(indent + "  " + key + ": ")
                json_print(value, levels + 2)
            else:
                print(indent + "  " + key + ": " + str(value) + ",")
        print(indent + "},")

    elif type(json) is list:
        print(indent + "[")
        for obj in json:
            json_print(obj, levels + 1)
        print(indent + "],")

    else:
        print(json)

def writeToFile(info, filename):
    """ given some variable info that contains data to be saved,
        and a filename, open the file and save the data via pickle. """
    with open(filename, 'wb') as handle:
        pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)

def readFromFile(filename):
    """ given a filename, read the pickle data from the file and return it """
    with open(filename, 'rb') as handle:
        return pickle.load(handle)

def main():
    """ get movie IDs from tmdb data dump, use those IDs to get
        data from tmdb and omdb, then write that data to files
        in groups of 1000   """
    # e.g. getting data for an individual movie
    # row_tmdb = getDataFromDB(35, "TMDB")
    # row_omdb = getDataFromDB(row_tmdb['imdb_id'], "OMDB")

    # e.g. get and print data for movie id 35
    # json_print(getAllData(35))

    # e.g. get all data for the first 100 IDs, and print the first five rows
    #data = getAllData(IDs[:100])
    #json_print(data[:5])

    # e.g. download IDs from tmdb, then write list to file
    m, d = 11, 27
    idFile = "data-stores/m_IDs_{}_{}.pkl".format(m, d)
    if os.path.isfile(idFile):
        IDs = readFromFile(idFile)
    else:
        IDs = getIDs(m, d)
        writeToFile(IDs, idFile)

    # then save the data we retrieved into pickle files, 
    # in groups of 1k for performance
    for i in range(len(IDs) // 1000):
        print("retrieveing and writing data at piece:", i)
        data = getAllData(IDs[i*1000:(i+1)*1000])
        writeToFile(data, "data-stores/m_data_{}.pkl".format(i))

if __name__ == "__main__":
    main()
