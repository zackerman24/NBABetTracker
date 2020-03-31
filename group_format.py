#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from scraper import *
from reference import OwnerMatch
import glob
import os

def load_latest_table():  
    """Pulls in the pickle file that was last saved."""
    
    list_of_files = glob.glob('/Users/Zackerman24/Desktop/NBABetTracker/*.pkl')
    latest_pull = max(list_of_files, key=os.path.getctime)
    latest_table = pd.read_pickle(latest_pull)
    return latest_table

#Code to begin reformatter
print(load_latest_table())