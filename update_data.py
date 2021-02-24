#!/usr/bin/env python3

from build_data import *
from plot_data import *
from write_to_readme import *
from ops import *

# Check for necessary directories
isdir('data')
isdir('plots')

# Update data
build_data()

# Plot data to png files
plot_data()

# Write to README
write_to_readme()

# push to github
os.system('git add . && git commit -m "Updating data." && git push')
