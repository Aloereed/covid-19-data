def mk_dir(*der):
    import os
    for d in der:
        if os.path.isdir(d) != True:
            print(f"creating '{d}'")
            os.mkdir(d)

def fetch(url):
    import requests, os, hashlib, tempfile
    fp = os.path.join(tempfile.gettempdir(), hashlib.md5(url.encode('utf-8')).hexdigest())
    if os.path.isfile(fp) and os.stat(fp).st_size > 0:
        with open(fp, 'rb') as f:
            dat = f.read()
    else:
        print(f'fetching {url}')
        dat = requests.get(url).content
        with open(f'{fp}.tmp', 'wb') as f:
            f.write(dat)
        os.rename(f'{fp}.tmp', fp)
    return dat

def get_diff(arr):
    import numpy as np
    arr = np.asarray(arr)
    diff = np.diff(arr)
    diff = np.insert(diff, 0, arr[0])
    return diff

def write_readme(template, date, df_24, df_avg):
    with open('README.md', 'w') as f:
        print(f"writing to 'README.md'")
        f.write(template.format(date, df_24, df_avg))
