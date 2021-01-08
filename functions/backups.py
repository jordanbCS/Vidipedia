#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# backups.py
# 
# created: on Mon Jan 4, 2020  
# @author: Jordan
#
# 1. Run ./videos.sh on the intermediary server
# 2. rsync the files to CloudLocation after creating an archive
# 3. Use their API to interact with the archives.
#
#

import subprocess
import numpy as np
import pandas as pd


CloudLocation = 'example.net'
API_name = 'c148' 
keySubDomain = '36-b20d-be5-dfd'
user = 'ssh_user'
ArchiveLocation = \
    "ssh://" + user + "@" + keySubDomain + ".buffer." + API_name + ".io:./buffer"


## SQL db dump  


# run: mysql Vidipedia -B -e "select source from hwdms_media where 1;" | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > public_html/archives/hwdms_media.csv

# run: sed -e 's/\"//g' -e 's/source//g' -e '/^\s*$/d' hwdms_media.csv > VideoArchiveBatch.txt

VidTable = pd.read_csv('VideoArchiveBatch.txt', sep=" ", header=None)

## VidipediaMaybes  

subprocess.call(["youtube-dl", "-ct", "-i","--batch-file", "VideoArchiveBatch.txt"])


## Cloud archive  

subprocess.call(["rsync", "-avp", "--progress","--stats", "-e", 
                 "ssh -p 24712", "Vidipedia",  ArchiveLocation])

