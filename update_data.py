#!/usr/bin/env python3

from build_data import *
from plot_data import *
from daily_report import *
import os

# Update data
build_data()

# Plot data to png files
plot_data()

# Write to daily report
create_daily_report()

# Commit to github
os.system('git add . && git commit -m "Updating data." && git push')
