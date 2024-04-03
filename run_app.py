"""
Flask Application for BioDock Visualiser Webtool
    - Authors: Ramon Reilman, Stijn Vermeulen, Yamila Timmer

This script runs the Flask application (webtool). 

Usage:
    Run this script (run_app.py) to start up the Flask web application. 
    Access the webtool through the URL displayed in the terminal.

Commandline usage: 
    - python3 run_app.py
"""
from app_functions import app

if __name__ == '__main__':
    app.run(debug=True)
