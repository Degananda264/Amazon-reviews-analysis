# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:00:44 2020

@author: degananda.reddy
"""

from waitress import serve
import flask_api

serve(flask_api.app,port=8000,threads=6)