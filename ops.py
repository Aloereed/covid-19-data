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
    diff = np.diff(arr)
    diff = np.insert(diff, 0, arr[0])
    return diff
