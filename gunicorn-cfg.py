# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - present ENG.Baraka.us
"""

import multiprocessing

# Bind to the address and port
bind = '0.0.0.0:5005'

# Number of workers (use CPU cores count * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Log settings
accesslog = '-'         # Log to stdout
errorlog = '-'          # Log to stderr
loglevel = 'debug'     # Set to 'info' or 'warning' for production
capture_output = True
enable_stdio_inheritance = True

# Timeout settings (default is 30 seconds, you can adjust as needed)
timeout = 120
