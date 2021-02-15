#!/usr/bin/env python3

import numpy as np
import datetime
import pandas as pd 

def create_daily_stats():
    # Import csv files
    cases_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', dtype='int32')
    deaths_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', dtype='int32')

    # Build arrays
    cases_array = np.array(cases_daily_csv)
    cases_length = len(cases_array)
    cases_today = cases_array[cases_length - 1]
    cases_mean = np.mean(cases_array)

    deaths_array = np.array(deaths_daily_csv)
    deaths_length = len(deaths_array)
    deaths_today = deaths_array[deaths_length - 1]
    deaths_mean = np.mean(deaths_array)

    # Build DataFrames
    today = datetime.datetime.today().strftime('%m-%d-%Y')
    index_today = ['Cases', 'Deaths']
    df_today = pd.DataFrame({today: [cases_today, deaths_today]}, index=index_today) 
    df_today.index.names = ['Date']

    index_avg = ['Cases per day', 'Deaths per day']
    df_avg = pd.DataFrame({'avg': [int(cases_mean), int(deaths_mean)]}, index=index_avg)
    df_avg.index.names = ['01-21-2020 - ' + today]

    # Write to 'daily_stats.md'
    f = open("/home/nuke/git/covid-19-data/data/daily_stats.md", "w")
    f.write("###### Stats for Today\n" + df_today.to_markdown() + "\n\n###### Averages\n" + df_avg.to_markdown())
    f.close()
