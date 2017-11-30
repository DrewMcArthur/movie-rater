"""
scrape-imsdb.py

gets movie scripts from the internet movie script databases
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

    try:
        for i in range(3,len(table)):
            """ extract each link in the table, and clean it up for usage"""
            string = str(list(table[i].children)[0])
            string = re.findall("\"(.+?)\"", string)[0]
            string = string.split("/")
            string = string[2].split(" ")
            string, end = string[:-1], string[-1]
            end = end.split(".")[-1]
            string.append(end)
            string, end = string[:-2], string[-2:]
            end = ".".join(end)
            string.append(end)
            string = "-".join(string)
            links.append(string)
        return links
    except:
        return links

def getScripts(links):
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
        soup = BeautifulSoup(page.content, 'html.parser')
        html = soup.find(class_ = 'scrtext')
        script = html.select('pre')[0]
        script = script.get_text()
        scripts.append(script)

    return scripts


def main():
    address = "http://www.imsdb.com/all%20scripts/"
    links = getLinks(address)
    print("got links")
    scripts = getScripts(links)
    print("got scripts")
    if (len(scripts) == len(links)):
        print("TRUE")
    for i in range(len(links)):
        openfile = open("scripts/" + links[i], "w")
        openfile.write(scripts[i])

if __name__ == "__main__":
    main()
