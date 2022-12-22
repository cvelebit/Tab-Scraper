# search for valid urls given keywords
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

GT_searchURL = "https://www.ultimate-guitar.com/search.php?search_type=title&value="
GT_result_class = ("div", "LQUZJ") # inside article, then inside div
GT_artist_result_class = ("a","aPPf7 jtEAE lBssT") # within result class, in div, in span
GT_song_result_class = ("a","aPPf7 HT3w5 lBssT")# within result class, in div, in header, in span, in span
GT_type_result_class = ("div","lIKMM PdXKY")# within result class


class GT_Search:
    def __init__(self):
        self.BrowserOptions = Options()
        self.BrowserOptions.add_argument("--headless") # opens chrome in background - no pop up
        self.BrowserOptions.add_argument("--log-level=1") # basically says it's not google's FLoC tracking tech
        self.Browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = self.BrowserOptions)
        self._results = []

    def get(self, searchString):
        searchString.replace(' ', '%20')
        self.Browser.get(GT_searchURL+searchString)
        self.html = self.Browser.execute_script("return document.body.innerHTML;")
        self.Browser.close()

    def parse(self, html=None):
        if html != None:
            self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def scrape(self, soup=None):
        if soup != None:
            self.soup = soup
        search_results = self.soup.findAll(GT_result_class[0], class_= GT_result_class[1])
        for search_result in search_results[1:]: #don't need header
            try:
                artist = search_result.find(GT_artist_result_class[0], class_= GT_artist_result_class[1])
                artist_text = artist.text
            except:
                artist_text = self._results[-1]["artist"]
            try:
                song = search_result.find(GT_song_result_class[0], class_= GT_song_result_class[1])
                type = search_result.contents[-1]
                self._results.append({
                    "artist": artist_text,
                    "title": song.text,
                    "url":song.get("href"),
                    "type":type.text
                })
            except Exception as e:
                print("ERROR: Song not found\n" + e)
        
    def print(self, data=None, limit=None):
        if data != None:
            self._results=data
        if len(self._results) == 0:
            print("ERROR: No results found")
        c = 1
         
        print()
        for result in self._results[:limit]:
            print("#" + str(c) + " :: " + result["title"] + " by " + result["artist"] + " - " + result["type"])
            c+=1
        print()
    
    def select(self, index=None):
        if index == None:
            inp = input('\nChoose a result (number) or exit ("exit"): ')
            if inp != "exit":
                while True:
                    try:
                        index = int(inp)
                        break
                    except Exception as e:
                        print('Invalid input - try again or exit ("exit")/n' + e)    
        return self._results[index-1]["url"], self._results[index-1]['title'], self._results[index-1]['artist']
            
if __name__ == '__main__':        
    search = GT_Search()
    search.get(input("Input search words seperated by single spaces: "))
    search.parse()
    search.scrape()
    search.print(limit=10)
    url, title, artist = search.select()
    print(url + "\n")
