#!/usr/bin/env python3

import os

# Check for necessary directories
dirs = ('data', 'plots')

for name in (dirs):
    isdir = os.path.isdir(name)

    if isdir != True:
        print("Error: '" + name + "' needs to be created.")
        exit(1)

# Update data
os.system('build_data.py')

# Plot data to png files
os.system('plot_data.py')

# Write to README
os.system('write_to_readme.py')

# push to github
os.system('git add . && git commit -m "Updating data." && git push')
