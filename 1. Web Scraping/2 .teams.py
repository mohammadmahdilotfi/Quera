from bs4 import BeautifulSoup
import requests
import re
import json

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

leagues = ['premier-league','la-liga','serie-a','bundesliga','ligue-1']

#/juventus-turin/startseite/verein/506/saison_id/2021
pattern = r"\/verein\/(\d+)\/saison_id\/\d+"
#/serge-gnabry/profil/spieler/159471
pattern_player = r"\/profil\/spieler\/(\d+)"

res_teams = []

for league in leagues :
    for year in range(2015,2022):
        url = f'https://www.transfermarkt.us/{league}/startseite/wettbewerb/GB1/plus/?saison_id={year}'
        page = requests.get(url,headers=HEADERS).text
        soup = BeautifulSoup(page,'html.parser')
        teams = soup.select('#yw1 .no-border-links a:nth-child(1)')
        for count,team in enumerate(teams):
            data_team = {}

            url = f'https://www.transfermarkt.us'+team.get('href')
            page = requests.get(url,headers=HEADERS).text
            soup = BeautifulSoup(page,'html.parser')
            match = re.search(pattern, url)
            if match:
                team_id = match.group(1)
                data_team['id'] = int(team_id)
            data_team['year'] = f'{year}/{year+1}'
            data_team['league'] = f'{league}'
            data_team['team_name'] = team.get('title')
            cups = soup.select('.data-header__success-image')
            cups_num = soup.select('.data-header__success-number')
            cups_list = [cup.get('title') for cup in cups]
            cups_num_list = [num.text for num in cups_num]
            data_team['cups'] = [[value,int(num_value)] for value,num_value in zip(cups_list,cups_num_list)]
            data_team['national_team_players'] = int(soup.select('.data-header__label:nth-child(1) a')[0].text)
            market = soup.select('.data-header__market-value-wrapper')[0]
            data_team['market_value'] = market.find('span').string + market.find('span').find_next_sibling(text=True) + market.find('span').find_next_sibling('span').string
            data_team['average_age'] = float(soup.select('.data-header__items:nth-child(1) .data-header__label:nth-child(2) .data-header__content')[0].text)
            players = soup.select('.nowrap a')
            players_link_list = [player.get('href') for player in players]
            players_link_list = players_link_list[::2]
            data_team['players_links'] = players_link_list
            players_list = [player.text for player in players]
            players_list = players_list[::2]
            data_team['players'] = players_list
            test = []
            for x in players_link_list:
                match2 = re.search(pattern_player,x)
                if match2:
                    player_id= match2.group(1)
                    test.append(player_id)
            data_team['players_ids'] = test
                    

            print(data_team)
            res_teams.append(data_team)

print('**************************************')
print('Finish scrape')
print('**************************************')

with open("teams.json", "w") as file:
    file.write(json.dumps(res_teams))
    print('Finish save')






