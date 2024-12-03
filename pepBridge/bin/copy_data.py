#!/usr/bin/env python3

import os
import shutil
import pkg_resources

def copy_files():
    ''' copy_files - routine that copy the *.csv and *.ini files 
    to the current directory.
    '''

    # Define source directories
    data_dir   = pkg_resources.resource_filename('pepBridge', 'data')
    config_dir = pkg_resources.resource_filename('pepBridge', 'config_files')
    current_dir= os.getcwd()

    # Copy CSV files from the data directory 
    # to the current directory.
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith(".csv"):
                src = os.path.join(data_dir, file)
                dest = os.path.join(current_dir, file)
                shutil.copy(src, dest)
                print(f"Copied: {src} -> {dest}")

    # Copy INI files from the config_files directory 
    # to the current directory
    if os.path.exists(config_dir):
        for file in os.listdir(config_dir):
            if file.endswith(".ini"):
                src = os.path.join(config_dir, file)
                dest = os.path.join(current_dir, file)
                shutil.copy(src, dest)
                print(f"Copied: {src} -> {dest}")

if __name__ == "__main__":
    copy_files()
