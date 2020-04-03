#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from scraper import *
from reference import *
import glob
import numpy as np
import os

def load_latest_table():  
    """Pulls in the pickle file that was last saved."""
    
    list_of_files = glob.glob('*.pkl')
    latest_pull = max(list_of_files, key=os.path.getctime)
    latest_table = pd.read_pickle(latest_pull)
    return latest_table

# table = load_latest_table())

#Code to begin reformatter

def format_table(original_table):
    """Formats table to include necessary group attributes, such as owner & round."""
    
    original_table['Wins'] = original_table['Overall'].str.extract('(\d+)-', expand=False).astype(int)
    original_table ['Owner'] = original_table['Team'].map(OwnerMatch)
    original_table['Round'] = original_table['Team'].map(RoundMatch)
    original_table.dropna(subset=['Owner'], inplace=True)
    return original_table

def sum_table(formatted_table):
    """Creates table showing standings by total wins."""
    
    summed_table = formatted_table.pivot(index='Owner',columns='Round', values = 'Wins').reset_index()
    summed_table['Total Wins'] = summed_table['Round 1'] + summed_table['Round 2']
    summed_table.sort_values(by='Total Wins',ascending=False,inplace=True).reset_index()
    return summed_table

print(sum_table(format_table(load_latest_table())))

def week_chart(summed_table):
    """Creates a chart that shows the standings and split by team."""
    
    