#!/usr/bin/env python3
import requests, hashlib, os, tempfile, io
from time import time, sleep
from tqdm import trange
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from README_TEMPLATE import README_TEMPLATE
from subprocess import check_call

st = time()

def fetch(url): 
    acc = 0
    while True:
        try:
            print(f"fetching '{url}'")
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                dat = response.content
            print("comparing hashes")
            sig = hashlib.md5()
            for line in response.iter_lines():
                sig.update(line)
            digest = sig.hexdigest()
            fp = os.path.join(tempfile.gettempdir(), hashlib.md5(digest.encode('utf-8')).hexdigest())
            if os.path.isfile(fp) and os.stat(fp).st_size > 0:
                print("no update available")
                timeout(3600)
                acc = 0
            else:
                print(f"writing to '{fp}'")
                with open(f"{fp}.tmp", 'wb') as f:
                    f.write(dat)
                os.rename(f"{fp}.tmp", fp)
                return dat
        except Exception as error:
            acc += 1
            retry(acc, error)

def timeout(s):
    timeout = trange(s, ncols=103, leave=False, ascii=' #')
    for t in timeout:
        timeout.set_description(uptime())
        sleep(1)

def uptime(): 
    ct = time()
    et = ct - st
    d = (et // 86400) % 365
    h = (et // 3600) % 24
    m = (et // 60) % 60
    s = et % 60
    d = int(d) 
    h = int(h)
    m = int(m)
    s = int(s)
    d = str(d).zfill(3)
    h = str(h).zfill(2)
    m = str(m).zfill(2)
    s = str(s).zfill(2)
    uptime = f"uptime: {d} {h}:{m}:{s}"
    return uptime

def retry(acc, error):
    print(f"\n{str(acc).zfill(2)}/10: {error}\n")
    if acc < 10:
        timeout(6)
    else:
        print("max retries exceeded")
        exit(1)

while True:

    dat = fetch('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
   
    df = pd.read_csv(io.StringIO(dat.decode('utf-8')))
    dates = np.array(df['date'], dtype='datetime64')
    total_cases = np.array(df['cases'], dtype='int64')
    total_deaths = np.array(df['deaths'], dtype='int64')

    def get_diff(arr):
        arr = np.asarray(arr)
        diff = np.diff(arr)
        arr = np.insert(diff, 0, arr[0])
        return arr

    new_cases = get_diff(total_cases)
    new_deaths = get_diff(total_deaths)

    def mk_dir(*dirs):
        for d in dirs:
            if not os.path.isdir(d):
                print(f"creating '{os.path.join(os.getcwd(), d)}'")
                os.mkdir(d)

    mk_dir('data', 'plots')

    print(f"writing to '{os.path.join(os.getcwd(), 'data')}'")

    df = pd.DataFrame({'date': dates, 'total cases': total_cases,
        'total deaths': total_deaths})
    df.to_csv('data/us_covid-19_total.csv', index=False)

    df = pd.DataFrame({'date': dates, 'new cases': new_cases, 
        'new deaths': new_deaths})
    df.to_csv('data/us_covid-19_new.csv', index=False)

    df = pd.DataFrame({'date': dates, 'total cases': total_cases, 
        'total deaths': total_deaths, 'new cases': new_cases, 'new deaths': new_deaths})
    df.to_csv('data/us_covid-19_data.csv', index=False)

    print(f"writing to '{os.path.join(os.getcwd(), 'plots')}'")

    x = dates

    y = total_cases / 1000000
    plt.figure('US Total COVID-19 Cases', figsize=(15, 8))
    plt.title('US Total COVID-19 Cases')
    plt.ylabel('Cases (in millions)')
    plt.grid(True, ls='-.')
    plt.yticks(np.arange(min(y), max(y) + 10))
    plt.plot(x, y, color='b')
    plt.savefig('plots/US_Total_COVID-19_Cases.png')

    y = total_deaths / 1000
    plt.figure('US Total COVID-19 Deaths', figsize=(15, 8))
    plt.title('US Total COVID-19 Deaths')
    plt.ylabel('Deaths (in thousands)')
    plt.grid(True, ls='-.')
    plt.yticks(np.arange(min(y), max(y) + 100, 50))
    plt.plot(x, y, color='b')
    plt.savefig('plots/US_Total_COVID-19_Deaths.png')

    y = new_cases / 1000
    plt.figure('US New COVID-19 Cases', figsize=(15, 8))
    plt.title('US New COVID-19 Cases')
    plt.ylabel('Cases (in thousands)')
    plt.grid(True, ls='-.')
    plt.yticks(np.arange(min(y), max(y) + 100, 50))
    plt.plot(x, y, color='b')
    plt.savefig('plots/US_New_COVID-19_Cases.png')

    y = new_deaths
    plt.figure('US New COVID-19 Deaths', figsize=(15, 8))
    plt.title('US New COVID-19 Deaths')
    plt.ylabel('Deaths')
    plt.grid(True, ls='-.')
    plt.yticks(np.arange(min(y), max(y) + 1000, 500))
    plt.plot(x, y, color='b')
    plt.savefig('plots/US_New_COVID-19_Deaths.png')

    cases = new_cases[-1]
    deaths = new_deaths[-1]

    cmean = np.mean(new_cases[-7:])
    dmean = np.mean(new_deaths[-7:])

    date = dates[-1]

    df_24 = pd.DataFrame({'New cases': [f'{cases:,d}'], 'New deaths': [f'{deaths:,d}']})
    df_24 = df_24.to_markdown(index=False, disable_numparse=True)

    df_avg = pd.DataFrame({'Cases': [f'{int(cmean):,d}'], 'Deaths': [f'{int(dmean):,d}']})
    df_avg = df_avg.to_markdown(index=False, disable_numparse=True)

    def write_readme(template, date, df_24, df_avg):
        print(f"writing to '{os.path.join(os.getcwd(), 'README.md')}'")
        with open('README.md', 'w') as f:
            f.write(template.format(date, df_24, df_avg))

    write_readme(README_TEMPLATE(), date, df_24, df_avg)

    def push_git():
        if os.path.isdir('.git'):
            try:
                check_call('/usr/bin/git add .', shell=True)
                check_call('/usr/bin/git commit -m "Updating data."', shell=True)
            except Exception as error:
                print(f"\n{error}\n")
            acc = 0
            while True:
                try:
                    check_call('/usr/bin/git push', shell=True)
                    break
                except Exception as error:
                    acc += 1
                    retry(acc, error)

    push_git() 

    timeout(3600)
