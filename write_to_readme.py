#!/usr/bin/env python3

from build_data import new_cases, new_deaths, dates
import numpy as np
import pandas as pd

# New Cases in the last 24 hours
cases_array = new_cases
length = len(new_cases)
new_cases = new_cases[length - 1]
new_cases = f'{new_cases:,d}'

# New Deaths in the last 24 hours
deaths_array = new_deaths
length = len(new_deaths)
new_deaths = new_deaths[length - 1]
new_deaths = f'{new_deaths:,d}'

# 7-day mean (new cases)
cl7d = cases_array[-7:]
cases_mean = np.mean(cl7d)
cases_mean = int(cases_mean)
cases_mean = f'{cases_mean:,d}'

# 7-day mean (new deaths)
dl7d = deaths_array[-7:]
deaths_mean = np.mean(dl7d)
deaths_mean = int(deaths_mean)
deaths_mean = f'{deaths_mean:,d}'

# Date
length = len(dates)
date = dates[length - 1]
date = str(date)

# DataFrame for new cases and deaths in the last 24 hours 
df_24 = pd.DataFrame({'New Cases': [new_cases], 'New Deaths': [new_deaths]})
df_24 = df_24.to_markdown(index=False, disable_numparse=True)

# DataFrame for 7-day average
df_avg = pd.DataFrame({'Cases': [cases_mean], 'Deaths': [deaths_mean]})
df_avg = df_avg.to_markdown(index=False, disable_numparse=True)

# Write to 'README.md'
f = open('README.md', 'w')
f.write("""# US COVID-19 [Data](https://github.com/drebrb/covid-19-data/blob/master/data/us_covid-19_data.csv)
\n###### Reported numbers for """ + date + "\n" + df_24 + "\n\n###### 7-day average\n" + df_avg +
"""
\n## [Total Cases and Deaths](https://github.com/drebrb/covid-19-data/blob/master/data/us_covid-19_total.csv)

### Cases
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Total_COVID-19_Cases.png)

### Deaths
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_Total_COVID-19_Deaths.png)

## [New Cases and Deaths](https://github.com/drebrb/covid-19-data/blob/master/data/us_covid-19_new.csv) 

### Cases
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_New_COVID-19_Cases.png)

### Deaths
![Plot](https://github.com/drebrb/covid-19-data/blob/master/plots/US_New_COVID-19_Deaths.png)
""")
f.close()
