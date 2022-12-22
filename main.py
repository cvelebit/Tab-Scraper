# interface
from search import GT_Search
from scraper import GT_Scraper, toWord
from output import Docx, TerminalOut

def Search():
    search = GT_Search()
    search.get(input("Input search words seperated by single spaces: "))
    search.parse()
    search.scrape()
    search.print(limit=10)
    url, title, artist = search.select()
    return url

def Scrape(url):
    crawler = GT_Scraper()
    crawler.get(url)
    crawler.parse()
    song = crawler.scrape()

    while True:
        inp = input("Output: Terminal - 't' or Word - 'w': ")
        if inp == "t":
            TerminalOut(song)
            break
        elif inp == "w":
            toWord(song)
            break
        else:
            print("Invalid input")

url = Search()
Scrape(url)