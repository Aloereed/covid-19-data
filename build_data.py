#!/usr/bin/env python3

import requests
import pandas as pd
import io
import numpy as np

# Fetch data
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))

# Extract each column individually
dates = df['date']
total_cases = df['cases']
total_deaths = df['deaths']

# Calculate new cases
total_cases = np.array(total_cases)
new_cases = np.diff(total_cases)
new_cases = np.insert(new_cases, 0, 1)

# Calculate new deaths
total_deaths = np.array(total_deaths)
new_deaths = np.diff(total_deaths)
new_deaths = np.insert(new_deaths, 0, 0)

# Create csv for total cases and deaths
d = {'date': dates, 'total cases': total_cases, 'total deaths': total_deaths}
df = pd.DataFrame(data=d)
df.to_csv('data/us_covid-19_total.csv', index=False)

# Create csv for new cases and deaths
d = {'date': dates, 'new cases': new_cases, 'new deaths': new_deaths}
df = pd.DataFrame(data=d)
df.to_csv('data/us_covid-19_new.csv', index=False)

# Create csv for all aggregated data
d = {'date': dates, 'total cases': total_cases, 'total deaths': total_deaths,
        'new cases': new_cases, 'new deaths': new_deaths}
df = pd.DataFrame(data=d)
df.to_csv('data/us_covid-19_data.csv', index=False)
