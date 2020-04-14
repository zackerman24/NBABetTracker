#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:14:42 2020

@author: Zackerman24
"""

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'wahoowa-2017'