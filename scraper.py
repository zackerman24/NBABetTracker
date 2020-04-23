# -*- coding: utf-8 -*-

"""

Next Steps:
3. Manipulate the data table to create necessary columns (e.g. just wins for
                                                          total and monthly)
4. Create necessary tables to translate team wins into "Owner" wins
5. Create graphs to show trends over time (monthly)
6. Create the table that gets updated weekly and compares to previous week's
performance.

"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime
#np.where for location


def pull_current_standings(year):
    """Pulls NBA standings at the current point in time."""
    
    comm = re.compile("<!--|--!>")
    url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html".format(year)
    page = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(re.sub("<!--|-->","",page),features='lxml')
    standings = soup.find('table', {'id':'expanded_standings'})
    
    header_row = standings.find_all('tr')[1]
    headers = [th.get_text() for th in header_row.find_all('th')][1:]
    rows = standings.find_all('tr')[2:]
    team_stats = [[td.get_text() for td in rows[i].find_all('td')]
                  for i in range(len(rows))]

    nba_standings = pd.DataFrame(team_stats, columns = headers)
    print(nba_standings)
    return nba_standings

def save_current_standings(current_standings):
    """Saves down the latest pull for current and future reference."""
    filename = '/past_data_pulls/Standings {}.pkl'.format(datetime.date.today())
    current_standings.to_pickle(filename)
    print("File saved down as {}".format(filename))


#save_current_standings(pull_current_standings(2020))