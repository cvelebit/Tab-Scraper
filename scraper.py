# scrape and format song content given a url
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from output import Docx, TerminalOut

GT_song_body = ("pre", "tK8GG Ty_RP")
GT_line = ("span", "y68er") #single line
GT_content_line = ("span", "fsG7q") #a span with chords and lyrics contained as spans

class GT_Scraper:
    def __init__(self):
        self.BrowserOptions = Options()
        self.BrowserOptions.add_argument("--headless") #opens chrome in background - no pop up
        self.BrowserOptions.add_argument("--log-level=1") #basically says it's not google's FLoC tracking tech
        self.Browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = self.BrowserOptions)
        self.song = []
 
    def get(self, url):
        self.Browser.get(url)
        self.html = self.Browser.execute_script("return document.body.innerHTML;")
        self.Browser.close()

    def parse(self, html=None):
        if html != None:
            self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def scrape(self, soup=None):
        if soup != None:
            self.soup = soup
        body = (self.soup).find(GT_song_body[0], {"class": GT_song_body[1]})
        lines = body.findChildren("span", recursive=False)
        data = []
        for line in lines:
            text = str(line.text)
            if text.strip() == "\r\n" or text.strip() == "":
                continue #empty line

            elif (re.search('\[(.*?)\]', text)) != None:
                if data != []:
                    self.song.append((structure, (*data, ))) #previous structure, data loaded into tuple
                    data = []
                r = re.search('\[(.*?)\]', text)
                structure = text[r.span(1)[0]:r.span(1)[1]] #type of structure
                 
            elif GT_content_line[1] in line["class"]:
                text = text.split("\r\n")
                text[1] = text[1].replace("/u205f", " ") #GT uses unicode space, but might be fine with docx
                data.append(("chords", text[0])) #chords for the line
                data.append(("lyrics", text[1])) #lyrics for the line

            else:
                data.append(("chords", text.strip("\r\n")))
        if data != []:
            self.song.append((structure, (*data, )))
        return self.song


def toWord(song):
    doc = Docx()
    for structure in song:
        doc.writeLine(structure[0], "church_lyric")
        for line in structure[1]:
            if line[0] == "chords":
                doc.writeLine(line[1], "church_chord")
            else:
                doc.writeLine(line[1], "church_lyric")
    doc.save()


if __name__ == '__main__':        
    crawler = GT_Scraper()
    crawler.get("https://tabs.ultimate-guitar.com/tab/maverick-city-music/jireh-chords-4103701")
    #crawler.get("https://tabs.ultimate-guitar.com/tab/rick-astley/never-gonna-give-you-up-official-2251635")
    crawler.parse()
    song = crawler.scrape()

    #TerminalOut(song)

    toWord(song)