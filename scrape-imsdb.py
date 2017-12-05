"""
scrape-imsdb.py

gets movie scripts from the internet movie script databases
"""

from bs4 import BeautifulSoup
import regex as re
import requests

def getLinks(address):
    """ gets all the links from the table on the "all scripts"
    page on imsdb """
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')

    links = []
    # navigate to the table holding the movie links
    html = soup.select("html body table")[1]
    body = list(list(html.children)[1].children)[1]
    table = list(list(body.children)[39].children)

    # #delete after debugging
    # string = str(list(table[3].children)[0])
    # string = re.findall("\"(.+?)\"", string)[0]
    # string = string.split("/")
    # string = string[2].split(" ")
    # string, end = string[:-1], string[-1]
    # end = end.split(".")[-1]
    # string.append(end)
    # string, end = string[:-2], string[-2:]
    # end = ".".join(end)
    # string.append(end)
    # string = "-".join(string)
    # links.append(string)
    # #delete after debugging
    # return links

    # use a try-except to make sure if we go out of range we jsut leave
    try:
        for i in range(3,len(table)):
            """ extract each link in the table, and clean it up for usage"""
            string = str(list(table[i].children)[0])
            # get to line in the table that the title is in
            string = re.findall("\"(.+?)\"", string)[0]
            # find the title in that line of html
            string = string.split("/")
            # clean up the title to make it a usable link
            string = string[2].split(" ")
            string, end = string[:-1], string[-1]
            end = end.split(".")[-1]
            string.append(end)
            string, end = string[:-2], string[-2:]
            end = ".".join(end)
            string.append(end)
            string = "-".join(string)
            # add the now usable link to links
            links.append(string)
        return links
    except:
        return links

def getScripts(links):
    """ the script from each script page of imsdb """
    link = links[0]
    page = requests.get("http://www.imsdb.com/scripts/" + link)
    scripts = []

    # soup = BeautifulSoup(page.content, 'html.parser')
    # html = soup.find(class_ = 'scrtext')
    # script = html.select('pre')[0]
    # script = script.get_text()
    # print(type(script))
    # scripts.append(script)


    for i in range(len(links)):
        # convert page into BeautifulSoup Object
        soup = BeautifulSoup(page.content, 'html.parser')
        # get the html table body from the soup
        html = soup.find(class_ = 'scrtext')
        # get the script from the table
        script = html.select('pre')[0]
        # get the text from the soup object
        script = script.get_text()
        scripts.append(script)

    return scripts


def main():
    address = "http://www.imsdb.com/all%20scripts/"
    titles = []
    links = getLinks(address)
    print("got links")
    print(len(links))
    scripts = getScripts(links)
    print(len(scripts))
    print("got scripts")
    # if (len(scripts) == len(links)):
    #     print("TRUE")
    for i in range(len(links)):
        try:
            titles.append(links[i].split(".")[0])
        except:
            titles.append(links[i])
        openfile = open("scripts/" + titles[i], "w")
        openfile.write(scripts[i])

if __name__ == "__main__":
    main()
