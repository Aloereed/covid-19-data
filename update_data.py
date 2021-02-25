#!/usr/bin/env python3

import os

# Check for necessary directories
dirs = ('data', 'plots')

for name in (dirs):
    isdir = os.path.isdir(name)

    if isdir != True:
        print("Error: '" + name + "' needs to be created.")
        exit(1)

# Check OS
if os.name == 'nt':
    a = ''

else:
    a = 'python3 '

# Update data
os.system(a + 'build_data.py')

# Plot data to png files
os.system(a + 'plot_data.py')

# Write to README
os.system(a + 'write_to_readme.py')

# push to github
os.system('git add . && git commit -m "Updating data." && git push')
