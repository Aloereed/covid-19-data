def mk_dir(*dirs):
    import os
    for d in dirs:
        if not os.path.isdir(d):
            print(f"creating '{os.path.join(os.getcwd(), d)}'")
            os.mkdir(d)

def fetch(url, start_time):
    import requests, hashlib, os, tempfile
    from time import sleep
    from tqdm import trange
    from timeit import default_timer as timer
    while True:
        print(f"fetching '{url}'")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            dat = response.content
        print("comparing hashes")
        sig = hashlib.sha256()
        for line in response.iter_lines():
            sig.update(line)
        digest = sig.hexdigest()
        fp = os.path.join(tempfile.gettempdir(), hashlib.sha256(digest.encode('utf-8')).hexdigest())
        if os.path.isfile(fp) and os.stat(fp).st_size > 0:
            print("no update available")
            for i in trange(3600, ncols=80):
                sleep(1)
            update_time = timer()
            print(f'uptime: {update_time - start_time}')
        else:
            print(f"writing to '{fp}'")
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
    print(f"writing to '{os.path.join(os.getcwd(), 'README.md')}'")
    with open('README.md', 'w') as f:
        f.write(template.format(date, df_24, df_avg))

def git_push():
    import os
    if os.path.isdir('.git'):
        print("pushing to github")
        os.system('git pull && git add . && git commit -m "Updating data." && git push')
