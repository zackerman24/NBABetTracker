#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import datetime

recent_standings = pd.read_pickle('Standings 2020-03-28.pkl')

OwnerMatch = {
    'Atlanta Hawks': 'Neil', 
    'Boston Celtics': 'Zack', 
    'Brooklyn Nets': 'Ian', 
    'Charlotte Hornets': None, 
    'Chicago Bulls': None, 
    'Cleveland Cavaliers': None, 
    'Dallas Mavericks': 'Grant', 
    'Denver Nuggets': 'Simar', 
    'Detroit Pistons': None, 
    'Golden State Warriors': None, 
    'Houston Rockets': 'John', 
    'Indiana Pacers': 'Griffin', 
    'Los Angeles Clippers': 'Sebastian', 
    'Los Angeles Lakers': 'Ian', 
    'Memphis Grizzlies': None, 
    'Miami Heat': 'Eric', 
    'Milwaukee Bucks': 'Neil', 
    'Minnesota Timberwolves': 'Simar', 
    'New Orleans Pelicans': None, 
    'New York Knicks': None, 
    'Oklahoma City Thunder': 'Dawson', 
    'Orlando Magic': 'John', 
    'Philadelphia 76ers': 'Dawson', 
    'Phoenix Suns': 'Zack', 
    'Portland Trail Blazers': 'Sebastian', 
    'Sacramento Kings': None, 
    'San Antonio Spurs': 'Eric', 
    'Toronto Raptors': 'Grant', 
    'Utah Jazz': 'Griffin', 
    'Washington Wizards': None
    }