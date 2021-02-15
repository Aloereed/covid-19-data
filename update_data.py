#!/usr/bin/env python3

from build_data import*
from plot_data import*
from daily_report import*

# Update data
build_data()

# Plot data to png files
plot_cases_total()
plot_deaths_total()
plot_cases_daily()
plot_deaths_daily()

# Write to daily report
create_daily_report()
