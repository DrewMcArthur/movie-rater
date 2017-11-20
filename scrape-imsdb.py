"""
scrape-imsdb.py

gets movie scripts from thei nternet movie script databases
"""

from bs4 import BeautifulSoup
import regex as re
import requests

def getLinks(address):
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')

    links = []
    # navigate to the table holding the movie links
    html = soup.select("html body table")[1]
    body = list(list(html.children)[1].children)[1]
    table = list(list(body.children)[39].children)

    #delete after debugging
    string = str(list(table[3].children)[0])
    string = re.findall("\"(.+?)\"", string)[0]
    string = string.split("/")
    string = string[2].split(" ")
    string[-1] = "." + string[-1].split(".")[1]
    string = "-".join(string)
    links.append(string)
    #delete after debugging

    # for i in range(3,len(table)):
    # """ extract each link in the table, and clean it up for usage"""
    #     string = str(list(table[i].children)[0])
    #     string = re.findall("\"(.+?)\"", string)[0]
    #     string = string.split("/")
    #     string = string[2].split(" ")
    #     string[-1] = "." + string[-1].split(".")[1]
    #     string = "-".join(string)
    #     links.append(string)

    return links

def getScripts(links):
    link = links[0]
    print("http://www.imsdb.com/scripts/" + link)
    page = requests.get("http://www.imsdb.com/scripts/" + link)

    scripts = []

    soup = BeautifulSoup(page.content, 'html.parser')
    html = soup.find(class_ = 'scrtext')
    print html
    script = html.select('pre')[0]
    print script.get_text()

    return scripts


def main():
    address = "http://www.imsdb.com/all%20scripts/"
    links = getLinks(address)
    print "got links"
    scripts = getScripts(links)

if __name__ == "__main__":
    main()
