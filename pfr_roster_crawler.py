from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd
import time

def addRoster(team_abbr):
    r = requests.get("https://www.pro-football-reference.com/teams/"+team_abbr+"/2022_roster.htm")
    soup = BeautifulSoup(r.content, 'html.parser' )
    for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
       if "<tr>" in comment:
            roster = comment
    table = BeautifulSoup(roster, 'html.parser')
    rows = table.find_all("tr")
    rows.pop()
    def parseHeight(height):
        if height:
            height.split()
            return(int(height[0])*12+int(height[2]))
    for row in rows:
        data = row.findAll("td")
        if data:
            id_val=data[0]["data-append-csv"]
            name=data[0].getText()
            age=data[1].getText()
            pos=data[2].getText()
            played=data[3].getText()
            started=data[4].getText()
            weight=data[5].getText()
            height=parseHeight(data[6].getText())
            college=data[7].getText()
            birth=data[8]["csk"]
            exp=data[9].getText()
            draft_info=data[11].getText()
            curTeam=team_abbr

            df.loc[id_val]=pd.Series({'Name':name,'Age':age,'Pos':pos,'Team':curTeam,'GamesPlayed':played,'GamesStarted':started,'Weight':weight,'Height':height,'College':college,'Birthdate':birth,'Experience':exp,'DraftInfo':draft_info})

df = pd.DataFrame(columns=['Name','Age','Pos','Team','GamesPlayed','GamesStarted','Weight','Height','College','Birthdate','Experience','DraftInfo'])


teams=["buf","mia","nwe","nyj",'jax','oti','clt','htx','cin','rav','pit','cle','kan','sdg','rai','den','phi','dal','nyg','was','tam','car','nor','atl','det','min','gnb','chi','sfo','sea','ram','car']
for i in range(len(teams)):
    print(str((100/32)*i) + "/100")
    #bot-detection sleep timer
    time.sleep(1.5)
    addRoster(teams[i])

df.to_csv('nfl_players.csv')