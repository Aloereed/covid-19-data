#!/usr/bin/env python3

import requests
import pandas as pd
import io
import numpy as np

def build_data():
    # Fetch data
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    download = requests.get(url).content
    df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    df.to_csv("us.csv", index=False)

    # Paths to csv's
    fetched_data_path = ('/home/nuke/git/covid-19-data/us.csv')
    dates_path = ('/home/nuke/git/covid-19-data/data/us_covid-19_dates.csv')
    total_cases_path = ('/home/nuke/git/covid-19-data/data/us_covid-19_total_cases.csv')
    total_deaths_path = ('/home/nuke/git/covid-19-data/data/us_covid-19_total_deaths.csv')
    new_cases_path = ('/home/nuke/git/covid-19-data/data/us_covid-19_new_cases.csv')
    new_deaths_path = ('/home/nuke/git/covid-19-data/data/us_covid-19_new_deaths.csv')

    # Extract each column individually
    dates = pd.read_csv(fetched_data_path, usecols=['date'])
    total_cases = pd.read_csv(fetched_data_path, usecols=['cases'])
    total_deaths = pd.read_csv(fetched_data_path, usecols=['deaths'])

    # Create csv's for extracted columns
    dates.to_csv(dates_path, header=False, index=False)
    total_cases.to_csv(total_cases_path, header=False, index=False)
    total_deaths.to_csv(total_deaths_path, header=False, index=False)

    # csv files needed to build arrays
    total_cases_csv = np.genfromtxt(total_cases_path, dtype='int32')
    total_deaths_csv = np.genfromtxt(total_deaths_path, dtype='int32')

    # Calculate new cases
    total_cases = np.array(total_cases_csv)
    new_cases = np.diff(total_cases)
    new_cases = np.insert(new_cases, 0, 1)

    # Calculate new deaths
    total_deaths = np.array(total_deaths_csv)
    new_deaths = np.diff(total_deaths)
    new_deaths = np.insert(new_deaths, 0, 0)

    # Create csv's for new cases and deaths
    np.savetxt(new_cases_path, new_cases, fmt='%d')
    np.savetxt(new_deaths_path, new_deaths, fmt='%d')

    # csv files needed to aggregate all data
    total_cases = pd.read_csv(total_cases_path, header=None, dtype=str)
    total_deaths = pd.read_csv(total_deaths_path, header=None, dtype=str)
    new_cases = pd.read_csv(new_cases_path, header=None, dtype=str)
    new_deaths = pd.read_csv(new_deaths_path, header=None, dtype=str)

    # Create csv for total cases and deaths
    df = pd.read_csv(dates_path, names=['date'])
    df["total cases"] = total_cases
    df["total deaths"] = total_deaths
    df.to_csv('/home/nuke/git/covid-19-data/data/us_covid-19_total.csv', index=False)
    
    # Create csv for new cases and deaths
    df = pd.read_csv(dates_path, names=['date'])
    df["new cases"] = new_cases
    df["new deaths"] = new_deaths
    df.to_csv('/home/nuke/git/covid-19-data/data/us_covid-19_new.csv', index=False)

    # Create csv for all aggregated data
    df = pd.read_csv(dates_path, names=['date'])
    df["total cases"] = total_cases
    df["total deaths"] = total_deaths
    df["new cases"] = new_cases
    df["new deaths"] = new_deaths 
    df.to_csv('/home/nuke/git/covid-19-data/data/us_covid-19_data.csv', index=False)
