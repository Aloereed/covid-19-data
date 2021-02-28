#!/usr/bin/env python3
from ops import mk_dir, fetch, get_diff, write_readme
import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt
from README_TEMPLATE import README_TEMPLATE
import os

# create directories if they dont exist
mk_dir('data', 'plots')

# **** build data ****

# fetch data
dat = fetch('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
df = pd.read_csv(io.StringIO(dat.decode('utf-8')))

# arrays
dates = np.array(df['date'], dtype='datetime64')
total_cases = np.array(df['cases'], dtype='int64')
total_deaths = np.array(df['deaths'], dtype='int64')

# calculate new cases and deaths
new_cases = get_diff(total_cases)
new_deaths = get_diff(total_deaths)

print(f"writing to 'data'")
# create csv for total cases and deaths
df = pd.DataFrame({'date': dates, 'total cases': total_cases,
    'total deaths': total_deaths})
df.to_csv('data/us_covid-19_total.csv', index=False)

# create csv for new cases and deaths
df = pd.DataFrame({'date': dates, 'new cases': new_cases, 
    'new deaths': new_deaths})
df.to_csv('data/us_covid-19_new.csv', index=False)

# create csv for all aggregated data
df = pd.DataFrame({'date': dates, 'total cases': total_cases, 
    'total deaths': total_deaths, 'new cases': new_cases, 'new deaths': new_deaths})
df.to_csv('data/us_covid-19_data.csv', index=False)

# **** plot data ****
print(f"writing to 'plots'")
# x axis for all plots
x = dates

# plot total cases
y = total_cases / 1000000
plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
plt.title('US Total COVID-19 Cases')
plt.ylabel('Cases (in millions)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 10))
plt.plot(x, y, color='b')
plt.savefig('plots/US_Total_COVID-19_Cases.png')

# plot total deaths
y = total_deaths / 1000
plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
plt.title('US Total COVID-19 Deaths')
plt.ylabel('Deaths (in thousands)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 100, 50))
plt.plot(x, y, color='b')
plt.savefig('plots/US_Total_COVID-19_Deaths.png')

# plot new cases
y = new_cases / 1000
plt.figure('US New COVID-19 Cases', figsize=(15, 8))
plt.title('US New COVID-19 Cases')
plt.ylabel('Cases (in thousands)')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 100, 50))
plt.plot(x, y, color='b')
plt.savefig('plots/US_New_COVID-19_Cases.png')

# plot new deaths
y = new_deaths
plt.figure('US New COVID-19 Deaths', figsize=(15, 8))
plt.title('US New COVID-19 Deaths')
plt.ylabel('Deaths')
plt.grid(True, ls='-.')
plt.yticks(np.arange(min(y), max(y) + 1000, 500))
plt.plot(x, y, color='b')
plt.savefig('plots/US_New_COVID-19_Deaths.png')

# **** write to README.md ****

# new cases and deaths in the last 24 hours
cases = new_cases[-1]
deaths = new_deaths[-1]

# 7-day mean for new cases and deaths
cmean = np.mean(new_cases[-7:])
dmean = np.mean(new_deaths[-7:])

# date
date = dates[-1]

# DataFrame for new cases and deaths in the last 24 hours 
df_24 = pd.DataFrame({'New cases': [f'{cases:,d}'], 'New deaths': [f'{deaths:,d}']})
df_24 = df_24.to_markdown(index=False, disable_numparse=True)

# DataFrame for 7-day average
df_avg = pd.DataFrame({'Cases': [f'{int(cmean):,d}'], 'Deaths': [f'{int(dmean):,d}']})
df_avg = df_avg.to_markdown(index=False, disable_numparse=True)

# write to 'README.md'
write_readme(README_TEMPLATE(), date, df_24, df_avg)

# **** push to github ****
print("pushing to github")
os.system('git add . && git commit -m "Updating data." && git push')
