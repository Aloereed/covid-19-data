#!/usr/bin/env python3
import requests, hashlib, os, tempfile, io
from time import time, sleep
from tqdm import tqdm, trange
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
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
                acc = 0
                return False
            else:
                print(f"writing to '{fp}'")
                with open(f"{fp}.tmp", 'wb') as f:
                    f.write(dat)
                os.rename(f"{fp}.tmp", fp)
                return dat
        except Exception as error:
            acc += 1
            retry(acc, error)

def timeout(sec):
    for s in (t := trange(sec, ncols=103, leave=False, ascii=' #')):
        t.set_description(uptime())
        sleep(1)

def uptime(): 
    ct = time()
    et = ct - st
    d = (et // 86400) % 365
    h = (et // 3600) % 24
    m = (et // 60) % 60
    s = et % 60
    d, h, m, s = [int(i) for i in (d, h, m, s)]
    d = str(d).zfill(3)
    h, m, s = [str(i).zfill(2) for i in (h, m, s)]
    uptime = f"uptime: {d} {h}:{m}:{s}"
    return uptime

def retry(acc, error):
    print(f"\n{str(acc).zfill(2)}/10: {error}\n")
    if acc < 10:
        timeout(6)
    else:
        print("max retries exceeded")
        exit(1)

def get_array(df, col, dtype):
    arr = np.array(df[col], dtype=dtype)
    return arr

def get_arrays(df, dictionary):
    arr = [get_array(df, col, dtype) for col, dtype in dictionary.items()]
    return arr

def get_diff(arr):
    arr = np.asarray(arr)
    diff = np.diff(arr)
    arr = np.insert(diff, 0, arr[0])
    arr[arr < 0] = 0
    return arr

def get_diffs(*arrs):
    arr = [get_diff(arr) for arr in arrs]
    return arr

def write_csv(dictionary, fn):
    df = pd.DataFrame(dictionary)
    df.to_csv(fn, index=False)

def plot(dict_values, suffix, fp):
    fig, axes = plt.subplots(2, 2, figsize=(14, 8), dpi=200)
    fig.suptitle(f"{suffix} COVID-19 Data")
    x = dates
    if total_cases[-1] >= 1_000_000:
        y = total_cases / 1_000_000
        label = 'Cases (in millions)'
    else:
        y = total_cases
        label = 'Cases'
        axes[0,0].get_yaxis().set_major_formatter(
                tkr.FuncFormatter(lambda y, p: f"{int(y):,d}"))
    axes[0,0].set_title('Total Cases')
    axes[0,0].set_ylabel(label)
    axes[0,0].grid(True)
    axes[0,0].plot(x, y, color='b')
    y = new_cases
    axes[0,1].set_title('New Cases')
    axes[0,1].set_ylabel('Cases')
    axes[0,1].get_yaxis().set_major_formatter(
            tkr.FuncFormatter(lambda y, p: f"{int(y):,d}"))
    axes[0,1].grid(True)
    axes[0,1].plot(x, y, color='b')
    y = total_deaths
    axes[1,0].set_title('Total Deaths')
    axes[1,0].set_ylabel('Deaths')
    axes[1,0].get_yaxis().set_major_formatter(
            tkr.FuncFormatter(lambda y, p: f"{int(y):,d}"))
    axes[1,0].grid(True)
    axes[1,0].plot(x, y, color='b')
    y = new_deaths
    axes[1,1].set_title('New Deaths')
    axes[1,1].set_ylabel('Deaths')
    axes[1,1].get_yaxis().set_major_formatter(
            tkr.FuncFormatter(lambda y, p: f"{int(y):,d}"))
    axes[1,1].grid(True)
    axes[1,1].plot(x, y, color='b')
    plt.savefig(fp, bbox_inches='tight') 
    plt.close(fig)

def update_readme():
    tc = total_cases[-1] 
    td = total_deaths[-1]
    cases = new_cases[-1]
    deaths = new_deaths[-1]
    cmean = np.mean(new_cases[-7:])
    dmean = np.mean(new_deaths[-7:])
    date = dates[-1]
    mdy = datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d, %Y')
    md = datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d')
    today = datetime.now().strftime('%B %d, %Y')
    today = f"{today}, {clck()} EST"
    df = pd.DataFrame({"U.S": ["Cases", "Deaths"], "Total Reported": [f"{tc:,d}", 
        f"{td:,d}"], f"On {md}": [f"{cases:,d}", f"{deaths:,d}"], 
        "7-Day Average": [f"{int(cmean):,d}", f"{int(dmean):,d}"]})
    df = df.to_markdown(index=False, disable_numparse=True) 
    write_readme(README_TEMPLATE(), today, df)

def write_readme(template, date, df):
    print(f"writing to '{os.path.join(os.getcwd(), 'README.md')}'")
    with open('README.md', 'w') as f:
        f.write(template.format(date, df))

def clck():
    h = datetime.now().strftime('%H')
    h = int(h)
    m = datetime.now().strftime('%M')
    am = 'A.M'
    pm = 'P.M'
    if h > 12 and h < 24:
        h -= 12
        c = f"{h}:{m} {pm}"
    elif h == 24:
        h -= 12
        c = f"{h}:{m} {am}"
    elif h == 12:
        c = f"{h}:{m} {pm}"
    else:
        c = f"{h}:{m} {am}"
    return c

def mk_dir(*dirs):
    for d in dirs:
        if not os.path.isdir(d):
            print(f"creating '{os.path.join(os.getcwd(), d)}'")
            os.mkdir(d)

def parse(df, suffix):
    df = df.sort_values(by=[suffix])
    df = df[suffix]
    df = df.drop_duplicates()
    df = [df for df in df]
    return df

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

us_cols_dtypes = {
        'date': 'datetime64', 
        'cases': 'int64', 
        'deaths': 'int64'
        }

st_cols_dtypes = {
        'date': 'datetime64', 
        'state': 'U',
        'cases': 'int64', 
        'deaths': 'int64'
        }

while True:
    nat = fetch('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    stat = fetch('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    if nat is False and stat is False:
        timeout(3600)
    if nat is not False:
        df = pd.read_csv(io.StringIO(nat.decode('utf-8')))
        dates, total_cases, total_deaths = get_arrays(df, us_cols_dtypes)
        new_cases, new_deaths = get_diffs(total_cases, total_deaths)
        usd = { 
                'date': dates,
                'total cases': total_cases,
                'total deaths': total_deaths,
                'new cases': new_cases,
                'new deaths': new_deaths
                }
        print(f"writing to '{os.path.join(os.getcwd(), 'us.csv')}'")
        write_csv(usd, 'us.csv')
        print(f"writing to '{os.path.join(os.getcwd(), 'us.png')}'")
        plot(usd.values(), 'U.S', 'us.png')
        update_readme()
    if stat is not False:
        d = pd.read_csv(io.StringIO(stat.decode('utf-8'))) 
        states = parse(d, 'state')
        mk_dir('states')
        print(f"writing to '{os.path.join(os.getcwd(), 'states')}'")
        for state in (s := tqdm(states, ncols=103, leave=False, ascii=' #')):
            s.set_description(state)
            df = d[d['state'].str.contains(f"^{state}$", case=False)]
            dates, states, total_cases, total_deaths = get_arrays(df, st_cols_dtypes)
            new_cases, new_deaths = get_diffs(total_cases, total_deaths)
            std = {
                    'date': dates,
                    'state': states,
                    'total cases': total_cases,
                    'total deaths': total_deaths,
                    'new cases': new_cases,
                    'new deaths': new_deaths
                    }            
            write_csv(std, f"states/{state}.csv")
            plot(std.values(), state, f"states/{state}.png")
    if nat or stat is not False:
        push_git() 
        timeout(3600)
