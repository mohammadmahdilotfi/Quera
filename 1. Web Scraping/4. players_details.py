from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd 
import re
import json
from time import time

HEADERS = {'User-Agent': 'Mozilla/5.0'}
pattern = r'^#\d+'
pos_pattern = r'^(Attack|midfield|Defender|) - (.+)$'
player_id_pattern = r"\/profil\/spieler\/(\d+)"
def cleaner(string:str)->str:
    string = string.replace("\xa0"," ").replace('\u00e9','').replace('\u011f','').replace("\n"," ").replace("  ","").replace('\u00e1','').replace(":","").replace('\u20ac','')
    return string.strip()


def player_crawler(url):
#     url = 'https://www.transfermarkt.com/ali-gabr/profil/spieler/122980'
    page = requests.get(url,headers=HEADERS).text
    soup = BeautifulSoup(page,'html.parser')
    #Name
    player_keys = ['Player_ID','Name','Team_ID','Date of birth','Place of birth','Age','Height',
                 'Citizenship','Position','Foot','Nationality','Caps','Goals',
                'Current club','Joined','Outfitter','Main position','Other position',
                'Current market value','Highest market value']
    player_vals = [np.nan for i in range(len(player_keys))]
    player_details = dict()
    for i in range(len(player_keys)):
        player_details[player_keys[i]] = player_vals[i]
    records = {'Name':cleaner(re.sub(pattern, '', cleaner(soup.select(".data-header__headline-wrapper")[0].text)))}
    ##Player_ID
    player_id = np.nan
    match = re.search(player_id_pattern,url)
    if match:
        player_id = match.group(1)
    records['Player_ID'] = player_id
    try:
        records['Nationality'] = cleaner(soup.select("#main > main > header > div.data-header__info-box > div > ul:nth-child(3) > li:nth-child(1) > span > a")[0].text)
    except:
        pass
    try:
        match = re.search(r'/(\d+)$', soup.select('.data-header__club a')[0].get('href'))
        if match:
            records['Team_ID'] = match.group(1)            
    except:
        records['Team_ID'] = -1
    titles = []
    for item in soup.select(".info-table__content--regular"):
        titles.append(cleaner(item.text).strip())
    details = []
    for item in soup.select(".info-table__content--bold"):
        details.append(cleaner(item.text))
    for item,text in zip(titles,details):
        records[item] = text
    try:
        del records["Social-Media"]
    except:
        pass
    try:
        records["Caps"] = cleaner(soup.select("#main > main > header > div.data-header__info-box > div > ul:nth-child(3) > li:nth-child(2) > a:nth-child(1)")[0].text)
    except: 
        records["Caps"] = np.nan
    try:
        records["Goals"] = cleaner(soup.select(".data-header__content--highlight+ .data-header__content--highlight")[0].text)
    except: 
        records["Goals"] = np.nan
    #Positions 
    try:
        records["Main position"] = cleaner(soup.select(".detail-position__position")[0].text)
    except:
        pass
    try:
        records["Other position"] = [cleaner(pos.text) for pos in soup.select(".detail-position__position .detail-position__position")]
    except:
        pass
    # Values 
    try:
        records["Current market value"] = cleaner(soup.select(".tm-player-market-value-development__current-value")[0].text)
    except:
        pass
    try:
        records["Highest market value"] = cleaner(soup.select(".tm-player-market-value-development__max-value")[0].text)
    except:
        pass
    #Cizitenship 
    try:
        records['Citizenship'] = re.findall('[A-Z][^A-Z]*', records['Citizenship'])
    except:
        pass
    ## Positioning
    try:
        match = re.match(pos_pattern, records['Position'])
        if match:
            records['Position'] = match.group(1)
        else:
            records['Position'] = "Goalkeeper" 
    except:
        pass
    for key in records.keys():
        if key in player_keys:
            player_details[key] = records[key]
        else:
            pass
    return player_details


with open('links.txt', 'r') as p_links:
    links = p_links.readlines()
start = time()
final_details = []
counter = 0
for link in links:
    content = player_crawler(link.removesuffix('\n'))
    final_details.append(content)
    print(counter,'is appended')
    counter+=1
with open("player_details.json", "w") as file:
    file.write(json.dumps(final_details))
    print('All good!')
print(time() - start)


