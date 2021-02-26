#!/usr/bin/env python3

import os
import build_data, plot_data, write_to_readme

# Check for necessary directories
dirs = ('data', 'plots')
for name in (dirs):
    isdir = os.path.isdir(name)
    if isdir != True:
        print("Error: '" + name + "' needs to be created.")
        if name == 'plots':
            exit(1)

# Update data
build_data

# Plot data to png files
plot_data

# Write to README
write_to_readme

# push to github
os.system('git add . && git commit -m "Updating data." && git push')
