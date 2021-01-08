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


# Videos.sh --[

## SQL db dump  

# run: mysql Vidipedia -B -e "select source from hwdms_media where 1;" | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > public_html/archives/hwdms_media.csv
# run: sed -e 's/\"//g' -e 's/source//g' -e '/^\s*$/d' hwdms_media.csv > VideoArchiveBatch1.txt

subprocess.call(["youtube-dl", "-ct", "-i","--batch-file", "VideoArchiveBatch1.txt"])
VidTable = pd.read_csv('VideoArchiveBatch1.txt', sep=" ", header=None)

## VidipediaMaybes  

# run: youtube-dl -j --flat-playlist "https://www.youtube.com/playlist?list=PLh9Uewtj3bwnhCo31QWjqrHTkoyHydCCI" | jq -r '.id' | sed 's_^_https://youtu.be/_' > VideoArchiveBatch2.txt 
subprocess.call(["youtube-dl", "-ct", "-i","--batch-file", "VideoArchiveBatch2.txt"])
VidTableMaybes = pd.read_csv('VideoArchiveBatch2.txt', sep=" ", header=None)

# ]--

## Cloud archive  

subprocess.call(["rsync", "-avp", "--progress","--stats", "-e", 
                 "ssh -p 24712", "Vidipedia",  ArchiveLocation])

