#!/usr/bin/env python3
import requests
import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt
import os

# **** Build data ****

# Fetch data
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))

# Extract each column individually
date = df['date']
cases = df['cases']
deaths = df['deaths']

# Calculate new cases
total_cases = np.array(cases)
new_cases = np.diff(total_cases)
new_cases = np.insert(new_cases, 0, 1)

# Calculate new deaths
total_deaths = np.array(deaths)
new_deaths = np.diff(total_deaths)
new_deaths = np.insert(new_deaths, 0, 0)

# Create csv for total cases and deaths
df = pd.DataFrame({'date': date, 'total cases': total_cases,
    'total deaths': total_deaths})
df.to_csv('data/us_covid-19_total.csv', index=False)

# Create csv for new cases and deaths
df = pd.DataFrame({'date': date, 'new cases': new_cases, 
    'new deaths': new_deaths})
df.to_csv('data/us_covid-19_new.csv', index=False)

# Create csv for all aggregated data
df = pd.DataFrame({'date': date, 'total cases': total_cases, 
    'total deaths': total_deaths, 'new cases': new_cases, 'new deaths': new_deaths})
df.to_csv('data/us_covid-19_data.csv', index=False)

# **** Plot data ****

# x axis for all plots
x = np.array(date, dtype='datetime64')

# Plot Total Cases
y = total_cases / 1000000
plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
plt.title('US Total COVID-19 Cases')
plt.ylabel('Cases (in millions)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 10))
plt.plot(x, y, color='b')
plt.savefig('plots/US_Total_COVID-19_Cases.png')

# Plot Total Deaths
y = total_deaths / 1000
plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
plt.title('US Total COVID-19 Deaths')
plt.ylabel('Deaths (in thousands)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 100, 50))
plt.plot(x, y, color='b')
plt.savefig('plots/US_Total_COVID-19_Deaths.png')

# Plot New Cases
y = new_cases / 1000
plt.figure('US New COVID-19 Cases', figsize=(15, 8))
plt.title('US New COVID-19 Cases')
plt.ylabel('Cases (in thousands)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 100, 50))
plt.plot(x, y, color='b')
plt.savefig('plots/US_New_COVID-19_Cases.png')

# Plot New Deaths
y = new_deaths
plt.figure('US New COVID-19 Deaths', figsize=(15, 8))
plt.title('US New COVID-19 Deaths')
plt.ylabel('Deaths')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 1000, 500))
plt.plot(x, y, color='b')
plt.savefig('plots/US_New_COVID-19_Deaths.png')

# **** Write to README.md ****

# New cases and deaths in the last 24 hours
cases = new_cases[-1]
deaths = new_deaths[-1]

# 7-day mean for new cases and deaths
cmean = np.mean(new_cases[-7:])
dmean = np.mean(new_deaths[-7:])

# Date
date = x[-1]

# DataFrame for new cases and deaths in the last 24 hours 
df_24 = pd.DataFrame({'New cases': [f'{cases:,d}'], 'New deaths': [f'{deaths:,d}']})
df_24 = df_24.to_markdown(index=False, disable_numparse=True)

# DataFrame for 7-day average
df_avg = pd.DataFrame({'Cases': [f'{int(cmean):,d}'], 'Deaths': [f'{int(dmean):,d}']})
df_avg = df_avg.to_markdown(index=False, disable_numparse=True)

# Write to 'README.md'
f = open('README.md', 'w')
f.write(f'''# US COVID-19 [Data](https://github.com/drebrb/covid-19-data/blob/master/data/us_covid-19_data.csv)
###### Reported numbers for {str(date)} 
{df_24}
###### 7-day average 
{df_avg}
## [Total Cases and Deaths](https://github.com/drebrb/covid-19-data/blob/master/data/us_covid-19_total.csv)
### Cases
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Total_COVID-19_Cases.png)
### Deaths
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Total_COVID-19_Deaths.png)
## [New Cases and Deaths](https://github.com/drebrb/covid-19-data/blob/master/data/us_covid-19_new.csv) 
### Cases
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_New_COVID-19_Cases.png)
### Deaths
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_New_COVID-19_Deaths.png)''')
f.close()

# **** push to github ****

os.system('git add . && git commit -m "Updating data." && git push')
