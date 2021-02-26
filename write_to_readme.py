#!/usr/bin/env python3

from build_data import new_cases, new_deaths, date
import numpy as np
import pandas as pd

# New cases and deaths in the last 24 hours
cases = new_cases[-1]
deaths = new_deaths[-1]

# 7-day mean for new cases and deaths
cmean = np.mean(new_cases[-7:])
dmean = np.mean(new_deaths[-7:])

# Date
date = np.array(date, dtype='datetime64')
date = date[-1]

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
