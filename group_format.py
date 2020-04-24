#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Next Steps:
1. Create a function to generate trending graph
    - Create folders per season (so you can safely pull one season easily)
    - Create a trending table to that tracks person's wins each week
2. Add trending performance to weekly chart
3, Create the user-facing options to easily run necessary updates
    - Scrape updated standings
    - View the latest standings
    - View trended standings

"""

import pandas as pd
from reference import OwnerMatch, RoundMatch
import glob
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import re
from bs4 import BeautifulSoup
import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 100)

def pull_current_standings(season_year):
    """Pulls NBA standings at the current point in time and applies formatting."""
    
    comm = re.compile("<!--|--!>")
    url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html".format(season_year)
    page = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(re.sub("<!--|-->","",page),features='lxml')
    standings = soup.find('table', {'id':'expanded_standings'})
    
    header_row = standings.find_all('tr')[1]
    headers = [th.get_text() for th in header_row.find_all('th')][1:]
    rows = standings.find_all('tr')[2:]
    team_stats = [[td.get_text() for td in rows[i].find_all('td')]
                  for i in range(len(rows))]

    nba_standings = pd.DataFrame(team_stats, columns = headers)
    nba_standings['Wins'] = nba_standings['Overall'].str.extract('(\d+)-', expand=False).astype(int)
    nba_standings ['Owner'] = nba_standings['Team'].map(OwnerMatch)
    nba_standings['Round'] = nba_standings['Team'].map(RoundMatch)
    nba_standings.dropna(subset=['Owner'], inplace=True)
    nba_standings['Round_1_Team'] = ["Yes" if x == 'Round 1' else None for x in nba_standings['Round']]
    nba_standings['Round_2_Team'] = ["Yes" if x == 'Round 2' else None for x in nba_standings['Round']]
    return nba_standings

def save_current_standings(current_standings, season_year):
    """Saves down the latest pull for current and future reference."""
    filename = 'past_data_pulls/{}/Standings {}.pkl'.format(season_year, datetime.date.today())
    current_standings.to_pickle(filename)
    print("File saved down as {}".format(filename))

def load_latest_saved_table(season_year):  
    """Pulls in the pickle file that was last saved."""
    
    list_of_files = glob.glob('past_data_pulls/{}/*.pkl').format(season_year)
    latest_pull = max(list_of_files, key=os.path.getctime)
    latest_table = pd.read_pickle(latest_pull)
    return latest_table

def create_sum_table(formatted_table):
    """Creates table showing standings by total wins for given standings."""
    
    summed_table = formatted_table.pivot(index='Owner',columns='Round', values = 'Wins').reset_index()
    summed_table['Total Wins'] = summed_table['Round 1'] + summed_table['Round 2']
    #Probably could just drop on the Round column value, instead new column.
    r1_table = formatted_table.dropna(subset=['Round_1_Team'])
    r2_table = formatted_table.dropna(subset=['Round_2_Team'])
    summed_table = summed_table.merge(r1_table[['Owner','Team']],how='left',on='Owner',
                                      suffixes=('','_1'),validate='1:1')
    summed_table = summed_table.merge(r2_table[['Owner','Team']],how='left',on='Owner',
                                      suffixes=('','_2'),validate='1:1')
    summed_table.rename(columns={'Team':'Team_1'}, inplace=True)
    summed_table = summed_table[['Owner','Total Wins','Team_1','Round 1','Team_2','Round 2']]
    summed_table.sort_values(by='Total Wins',ascending=False,inplace=True)
    summed_table.reset_index(drop=True, inplace=True)
    return summed_table


def create_week_chart(formatted_table,summed_table):
    """Creates charts that show the 1) standings and 2) splits by team."""
    
    sns.set()
    #sns.set_style('ticks')
    sns.set_context('notebook')
    fig, ax = plt.subplots(2,1,figsize=(10,7))
    
    owner_order = summed_table.Owner.values.tolist()
    chart = sns.barplot(x='Owner',y='Wins',hue='Round',data=formatted_table,
                        order=owner_order, ax=ax[0])
    chart.set_xticklabels(chart.get_xticklabels(), rotation=40, ha='center')
    
    for bar in chart.patches:
        chart.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,
                   '{:1.0f}'.format(bar.get_height()),ha='center')
    
    total_chart = sns.barplot(x='Owner',y='Total Wins',data=summed_table, ax=ax[1])
    total_chart.set_xticklabels(chart.get_xticklabels(), rotation=40, ha='center')
    
    for bar in total_chart.patches:
        total_chart.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,
                   '{:1.0f}'.format(bar.get_height()),ha='center')
    
    fig.tight_layout(pad=3)
    
def create_trending_table(season_year):
    """Creates table summarizing each week's/pull's standings."""
    list_of_files = glob.glob('past_data_pulls/{}/*.pkl'.format(season_year))
    list_of_files.sort(key=os.path.getctime)
    owners = list(set(OwnerMatch.values()))
    trending_table = pd.DataFrame(owners)
    
    for file in list_of_files:
        file_data = pd.read_pickle(file)
        pivot = file_data.pivot(index='Owner',columns='Round',values='Wins').reset_index()
        pivot['Total Wins'] = pivot['Round 1'] + pivot['Round 2']
        trending_table = trending_table.merge(pivot[['Owner','Total Wins']],how='left',
                                              on='Owner')
        trending_table.rename(columns={'Total Wins':'Wins {}'.format(str(file).split('Standings ')[1].split('.pkl')[0])})
    
    latest_file = list_of_files[-1]
    latest_column = 'Wins {}'.format(str(latest_file).split('Standings ')[1].split('.pkl')[0])
    trending_table.sort_values(by=[latest_column],ascending=False)
    return trending_table
        
    #New formula to create chart from table