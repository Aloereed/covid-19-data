#!/usr/bin/env python3

import numpy as np
import pandas as pd 

def create_daily_report():
    # Import csv files
    cases_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_cases_daily.csv', dtype='int32')
    deaths_daily_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_deaths_daily.csv', dtype='int32')
    dates_csv = np.genfromtxt('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv', dtype='datetime64')

    # Build array for daily case count and mean to date
    cases_array = np.array(cases_daily_csv)
    cases_length = len(cases_array)
    cases_today = cases_array[cases_length - 1]
    cases_mean = np.mean(cases_array)

    # Build array for daily death count and mean to date
    deaths_array = np.array(deaths_daily_csv)
    deaths_length = len(deaths_array)
    deaths_today = deaths_array[deaths_length - 1]
    deaths_mean = np.mean(deaths_array)

    # Most recent date reported
    date_array = np.array(dates_csv)
    date_length = len(date_array)
    date_today = date_array[date_length - 1 ]
 
    # Dataframe for cases and deaths in the last 24 hours
    today = date_today
    index_today = ['Cases', 'Deaths']
    df_today = pd.DataFrame({str(today): [f"{cases_today:,d}", f"{deaths_today:,d}"]}, index=index_today)
    df_today.index.names = ['Date']

    # DataFrame for averages to date
    index_avg = ['Cases per day', 'Deaths per day']
    df_avg = pd.DataFrame({'avg': [f"{int(cases_mean):,d}", f"{int(deaths_mean):,d}"]}, index=index_avg)
    df_avg.index.names = ['2020-01-21 - ' + str(today)]

    # Write to 'daily_report.md'
    f = open("/home/nuke/git/covid-19-data/README.md", "w")
    f.write("# US COVID-19 [Data](https://github.com/drebrb/covid-19-data/blob/master/us_covid-19_data.csv)\n\n###### Reported numbers for " + str(today) + "\n" + df_today.to_markdown() + "\n\n###### Averages\n" + df_avg.to_markdown() + """
\n\n## [Total](https://github.com/drebrb/covid-19-data/blob/master/us_covid-19_total.csv)

### Total Cases
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Total_COVID-19_Cases.png)

### Total Deaths
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Total_COVID-19_Deaths.png)


## [Daily](https://github.com/drebrb/covid-19-data/blob/master/us_covid-19_daily.csv) 

### Daily Cases
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Daily_COVID-19_Cases.png)

### Daily Deaths
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Daily_COVID-19_Deaths.png)
""")
    f.close()
