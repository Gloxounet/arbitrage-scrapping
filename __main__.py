import requests
from bs4 import BeautifulSoup

COTES_URL = 'http://www.cotes.fr/football/France-Ligue-1-ed3'
COTES_URL_LDC = "http://www.cotes.fr/football/Ligue-des-Champions-ed7"


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

######################################################## CLASSES ########################################################

class Cote :
    def __init__(self,bookmaker:str,cotes:list[float]) -> None:
        self.bookmaker = bookmaker
        if len(cotes) != 3 : raise AttributeError(message='cotes not length 3')
        self.c1 = cotes[0]
        self.c2 = cotes[1]
        self.c3 = cotes[2]
    
    def __str__(self) -> str:
        return f"{self.bookmaker} : {self.c1}/{self.c2}/{self.c3}"

class Match :
    def __init__(self,eq1:str,eq2:str,cotes:list[Cote]) -> None:
        self.eq1 = eq1
        self.eq2 = eq2

        self.cotes = cotes
    
    def __str__(self) -> str:
        return f"{self.eq1}-{self.eq2}"
    
    def printCotes(self) -> str:
        for cote in self.cotes :
            print(cote)

######################################################## FONCTION ########################################################

def getTeamsFromMatch(obj):
    names =  obj.findAll('a',{'class':'otn'})
    team_names =  [name.string for name in names]
    return team_names[0],team_names[1]

def getCotesFromMatch(obj)->Cote:
    #Get bookmaker
    bookmaker = obj['title'].split(' ')[-1]

    #Get cotes
    cotes_html = obj.findAll('td',{'class':'bet'})
    cotes = [float(cote.text) for cote in cotes_html]

    return Cote(bookmaker=bookmaker,cotes=cotes)

def getAllMatches(match_titles,bets):
    nb_match = len(match_titles)
    matchs = []
    for m_index in range(nb_match) :
        cotes = []
        for i in range(8):
            cotes.append(getCotesFromMatch(bets[i]))

        eq1,eq2 = getTeamsFromMatch(match_titles[m_index])

        matchs.append(Match(eq1,eq2,cotes))
    return matchs

def cotesScrap(url:str)->list[Match]:

    #Make request
    res = requests.get(url, headers=headers)
    
    #HTML Parser
    soup = BeautifulSoup(res.text, 'html.parser')
    
    bets = soup.find(id='oddetail').findAll('table',{'class':'bettable'})[0]

    #Get necessary elements on Cotes.fr
    match_titles = bets.findAll('tr',{'style':'background-color:white'})
    bets = bets.findAll('tr',{'class':'trout'})

    return getAllMatches(match_titles=match_titles,bets=bets)

######################################################## MAIN ########################################################

if __name__ == "__main__":
    matchs = cotesScrap(COTES_URL_LDC)
    for match in matchs:
        print(match)