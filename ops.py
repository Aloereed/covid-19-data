#!/usr/bin/env python3

import os

def path(file_name):
    cwd = os.getcwd()
    path = os.path.join(cwd, file_name)
    
    return path

def isdir(dir_name):
    isdir = os.path.isdir(dir_name)

    if isdir != True:
        print("Error: '" + dir_name + "' needs to be created.")
        exit(1)
