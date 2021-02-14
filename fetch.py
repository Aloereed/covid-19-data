#!/usr/bin/env python3

import requests
import pandas as pd
import io

def fetch_data():
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    download = requests.get(url).content
    df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    df.to_csv("us.csv", index=False)
