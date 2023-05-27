#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 13:53:03 2023

@author: arturoaltamirano808
"""

from application import app
from gunicorn.app.wsgiapp import WSGIApplication

# Create an instance of the WSGI server
server = WSGIApplication()

# Set the application callable to be used by the WSGI server
server.app = app

# Start the server
def run():
    server.run()

if __name__ == '__main__':
    run()
