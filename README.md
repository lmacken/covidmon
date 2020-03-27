# 🦠 COVID-19 Monitor

A simple tool to monitor COVID-19 case status across many locations.

It auto-refreshes twice a day, and uses https://covid19api.com for data.

![screenshot](https://github.com/lmacken/covidmon/raw/master/screenshot.png "COVID-19 Monitor1")

    Found 24 entries for Denver
                              Country          Province      Lat      Lon  Cases     Status
    Date
    2020-03-26 00:00:00+00:00      US  Colorado, Denver  39.7602 -104.873    262  confirmed
    2020-03-26 00:00:00+00:00      US  Colorado, Denver  39.7602 -104.873      0  recovered
    2020-03-26 00:00:00+00:00      US  Colorado, Denver  39.7602 -104.873      3     deaths

    Found 12 entries for Massachusetts, Hampden
                              Country                Province      Lat      Lon  Cases     Status
    Date
    2020-03-26 00:00:00+00:00      US  Massachusetts, Hampden  42.1344 -72.6324     55  confirmed
    2020-03-26 00:00:00+00:00      US  Massachusetts, Hampden  42.1344 -72.6324      1     deaths
    2020-03-26 00:00:00+00:00      US  Massachusetts, Hampden  42.1344 -72.6324      0  recovered


## Installing

    git clone git@github.com:lmacken/covidmon.git
    cd covidmon
    python3 -m venv py3env
    source py3env/bin/activate
    pip install -r requirements.txt


## Running

    python dashboard.py
