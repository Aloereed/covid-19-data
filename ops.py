def mk_dir(*der):
    import os
    for d in der:
        if os.path.isdir(d) != True:
            print(f"creating '{d}'")
            os.mkdir(d)

def fetch(url):
    import requests
    print(f"fetching '{url}'")
    with requests.get(url) as response:
        response.raise_for_status()
        dat = response.content
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
