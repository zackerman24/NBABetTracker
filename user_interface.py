#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:52:27 2020

@author: Zackerman24
"""

from group_format import *
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

user_options = """
1. Scrape and save latest NBA standings data.
2. Generate a table and chart with the latest saved standings.
3. Generate a table and chart with trended standings through latest save.
"""

print("""
Welcome to the NBA Bet Tracker Application.
If you'd like to quit at any time, enter 'exit'.""")

available_selections = [1,2,3]

while True:
    print("Your options are:/n" + user_options)
    user_selection = input("Please make your number selection: ")
    
    if user_selection not in available_selections:
        print("That was an invalid selection, please try again.")
        continue
    
    elif user_selection = 1:
        year = input("Please provide the ending year of the desired season: ")