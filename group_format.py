#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from scraper import *
from reference import *
import glob
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 100)

def load_latest_table():  
    """Pulls in the pickle file that was last saved."""
    
    list_of_files = glob.glob('*.pkl')
    latest_pull = max(list_of_files, key=os.path.getctime)
    latest_table = pd.read_pickle(latest_pull)
    return latest_table

def format_table(original_table):
    """Formats table to include necessary group attributes, such as owner & round."""
    
    original_table['Wins'] = original_table['Overall'].str.extract('(\d+)-', expand=False).astype(int)
    original_table ['Owner'] = original_table['Team'].map(OwnerMatch)
    original_table['Round'] = original_table['Team'].map(RoundMatch)
    original_table.dropna(subset=['Owner'], inplace=True)
    original_table['Round_1_Team'] = ["Yes" if x == 'Round 1' else None for x in original_table['Round']]
    original_table['Round_2_Team'] = ["Yes" if x == 'Round 2' else None for x in original_table['Round']]
    return original_table

def sum_table(formatted_table):
    """Creates table showing standings by total wins."""
    
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


f_table = format_table(load_latest_table())
table = sum_table(format_table(load_latest_table()))
print(table)


def week_chart(formatted_table,summed_table):
    """Creates a chart that shows the standings and split by team."""
    
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

week_chart(f_table,table)