import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set the display options to show all columns
pd.set_option('display.max_columns', None)


def get_league_data():
    # Define the leagues and their respective URLs
    leagues = [
        ("https://www.transfermarkt.us/premier-league/tabelle/wettbewerb/GB1?saison_id=", "Premier League"),
        ("https://www.transfermarkt.us/serie-a/tabelle/wettbewerb/IT1?saison_id=", "Serie A"),
        ("https://www.transfermarkt.us/laliga/tabelle/wettbewerb/ES1?saison_id=", "La Liga"),
        ("https://www.transfermarkt.us/bundesliga/tabelle/wettbewerb/L1?saison_id=", "Bundesliga"),
        ("https://www.transfermarkt.us/ligue-1/tabelle/wettbewerb/FR1?saison_id=", "Ligue 1")
    ]

    # Define the range of seasons
    seasons = range(2015, 2022)

    # Maximum number of retries for making requests
    max_retries = 3

    all_tables = []  # List to store all the tables

    for url, league_name in leagues:
        for season in seasons:
            full_url = f"{url}{season}"
            retries = 0
            success = False

            # Retry the request until success or maximum retries reached
            while retries < max_retries and not success:
                try:
                    html_content = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0',
                                                                   "Accept-Language": "en-US,en;q=0.5"}).text
                    success = True
                except requests.exceptions.RequestException:
                    print(f"Error occurred while making a request. Retrying in 5 seconds...")
                    time.sleep(5)
                    retries += 1

            if not success:
                print(f"Failed to retrieve data from {full_url}. Skipping...")
                continue

            soup = BeautifulSoup(html_content, "html.parser")

            league = soup.find('h1').text.strip()
            # Define the regex pattern to extract the league name
            pattern = r"Table\s(.+?)\s\d+/\d+"

            # Use regex to find the league name in the string
            match = re.search(pattern, league)

            if match:
                league_name = match.group(1)
                league = league_name

            # Find the table containing the data
            table = soup.find_all("table")[1]

            # Extract table headers
            headers = [th.text.strip() for th in table.find_all("th")]
            headers.insert(1, '')
            headers[3] = 'Matches'
            headers[0] = 'Rank'
            headers[8] = 'Goal difference'

            rows = []
            team_ids = []

            # Extract data rows from the table
            for tr in table.find_all("tr")[1:]:
                cells = [td.text.strip() for td in tr.find_all("td")]
                rows.append(cells)

                # Extract team ID from the club URL
                club_url = tr.find("td", class_='zentriert').find("a").get('href')
                pattern = r"\/verein\/(\d+)\/saison_id\/\d+"
                match = re.search(pattern, club_url)
                if match:
                    team_id = int(match.group(1))
                    team_ids.append(team_id)

            # Create a DataFrame from the extracted data
            df = pd.DataFrame(rows, columns=headers)
            # df = df.drop('', axis=1)  # managing conflict

            df.insert(2, "Season", f'{season}-{season + 1}')
            df.insert(1, "League", league)
            df.insert(3, "club_id", team_ids)

            all_tables.append(df)  # Append the current table to the list

    # Concatenate all the tables into a single DataFrame
    merged_df = pd.concat(all_tables, ignore_index=True)

    return merged_df


# get_league_data()
data = get_league_data()
# Save the data to a JSON file
data.to_json('league_data.json', orient='records', indent=4)
