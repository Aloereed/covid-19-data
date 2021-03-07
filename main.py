#!/usr/bin/env python3
import requests, hashlib, os, tempfile, io
from time import time, sleep
from tqdm import tqdm, trange
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
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

def get_diff(arr):
    arr = np.asarray(arr)
    diff = np.diff(arr)
    arr = np.insert(diff, 0, arr[0])
    return arr

def mk_dir(*dirs):
    for d in dirs:
        if not os.path.isdir(d):
            print(f"creating '{os.path.join(os.getcwd(), d)}'")
            os.mkdir(d)

while True:

    dat = fetch('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
   
    df = pd.read_csv(io.StringIO(dat.decode('utf-8')))
    dates = np.array(df['date'], dtype='datetime64')
    total_cases = np.array(df['cases'], dtype='int64')
    total_deaths = np.array(df['deaths'], dtype='int64')

    new_cases = get_diff(total_cases)
    new_deaths = get_diff(total_deaths)

    print(f"writing to 'us.csv'")

    df = pd.DataFrame({'date': dates, 'total cases': total_cases, 
        'total deaths': total_deaths, 'new cases': new_cases, 'new deaths': new_deaths})
    df.to_csv('us.csv', index=False)

    mk_dir('plots')

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

    tc = total_cases[-1]
    td = total_deaths[-1]

    cases = new_cases[-1]
    deaths = new_deaths[-1]

    cmean = np.mean(new_cases[-7:])
    dmean = np.mean(new_deaths[-7:])

    date = dates[-1]
    mdy = datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d, %Y')
    md = datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d')

    df = pd.DataFrame({"U.S": ["Cases", "Deaths"], "Total Reported": [f"{tc:,d}", f"{td:,d}"], 
        f"On {md}": [f"{cases:,d}", f"{deaths:,d}"], "7-Day Average": [f"{int(cmean):,d}",
            f"{int(dmean):,d}"]})
    df = df.to_markdown(index=False, disable_numparse=True)

    def write_readme(template, date, df):
        print(f"writing to '{os.path.join(os.getcwd(), 'README.md')}'")
        with open('README.md', 'w') as f:
            f.write(template.format(date, df))

    write_readme(README_TEMPLATE(), mdy, df)

    dat = fetch('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df = pd.read_csv(io.StringIO(dat.decode('utf-8')))
    
    def ls(df, suffix):
        df = df.sort_values(by=[suffix])
        df = df[suffix]
        df = df.drop_duplicates()
        df = [df for df in df]
        return df
                                                                                                 
    states = ls(df, 'state')
                                                                                                 
    def write_states(states, df):
        mk_dir('states')
        print(f"writing to '{os.path.join(os.getcwd(), 'states')}'")
        d = df
        s = tqdm(states, ncols=103, leave=False, ascii=' #')
        for state in s:
            df = d[d['state'].str.contains(state, case=False)]
            dates = np.array(df['date'], dtype='datetime64')
            states = np.array(df['state'])
            total_cases = np.array(df['cases'], dtype='int64')
            total_deaths = np.array(df['deaths'], dtype='int64')
            new_cases = get_diff(total_cases)
            new_deaths = get_diff(total_deaths)
            df = pd.DataFrame({'date': dates, 'state': states, 'total cases': total_cases, 
                'total deaths': total_deaths, 'new cases': new_cases, 'new deaths': new_deaths})
            df.to_csv(f"states/{state}.csv", index=False)
            s.set_description(state)
                                                                                                 
    write_states(states, df)

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
