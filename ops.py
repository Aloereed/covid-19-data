def mk_dir(*der):
    import os
    for d in der:
        if not os.path.isdir(d):
            print(f"creating '{os.path.join(os.getcwd(), d)}'")
            os.mkdir(d)

def fetch(url):
    import requests, hashlib, os, tempfile
    print("comparing hashes")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        r = response
    sig = hashlib.sha256()
    for line in r.iter_lines():
        sig.update(line)
    digest = sig.hexdigest()
    fp = os.path.join(tempfile.gettempdir(), hashlib.sha256(digest.encode('utf-8')).hexdigest())
    if os.path.isfile(fp) and os.stat(fp).st_size > 0:
        print(f"reading '{fp}'")
        with open(fp, 'rb') as f:
            dat = f.read()
    else:
        print(f"writing to '{tempfile.gettempdir()}'")
        with requests.get(url) as response:
            response.raise_for_status()
            dat = response.content
        with open(f"{fp}.tmp", 'wb') as f:
            f.write(dat)
        os.rename(f"{fp}.tmp", fp)
    return dat

def get_diff(arr):
    import numpy as np
    arr = np.asarray(arr)
    diff = np.diff(arr)
    arr = np.insert(diff, 0, arr[0])
    return arr

def write_readme(template, date, df_24, df_avg):
    import os
    with open('README.md', 'w') as f:
        print(f"writing to '{os.path.join(os.getcwd(), 'README.md')}'")
        f.write(template.format(date, df_24, df_avg))
