"""
scrape-mss.py

gets movie scripts from moviescriptsandscreenplays.comm
"""

from bs4 import BeautifulSoup
import regex as re
import requests

def getLinks(address):
    """ gets all the links to scripts from the table on the mss website """
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')

    links = []
    # navigate to the table holding the links
    # table = soup.find_all("table")[4]
    # print(type(table))
    # print(len(list(table.children)))
    # print(list(table.children))
    html = soup.select("html body table")
    print(list(list(list(html[2].children)[1].children)[1]))

    # get a list of all the movies from the table
    # movies = len(list(table.children))
    # print(movies)


def main():
    address = ["http://www.moviescriptsandscreenplays.com/index.html#top",
        "http://www.moviescriptsandscreenplays.com/movie-scripts.html",
        "http://www.moviescriptsandscreenplays.com/movie-scripts2.html"]
    links = []
    titles = []
    scripts = []

    # get the links from the pages of the mss
    links.append(getLinks(address[0]))


if __name__ == "__main__":
    main()
