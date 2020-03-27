# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
comm = re.compile("<!--|--!>")

year = 2020

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