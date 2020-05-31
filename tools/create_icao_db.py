#!/usr/bin/env python3

# Downloads http://registry.faa.gov/database/ReleasableAircraft.zip and extracts it in ram
# to generate the aircraft ICAO database.
# 
# Primarily used to during kismet release tagging to generate the aircraft db

import csv
import urllib.request
import io
import zipfile

import os
import sys

acft={}
mdl={}

with urllib.request.urlopen("http://registry.faa.gov/database/ReleasableAircraft.zip") as response, io.BytesIO() as mem_zf:
    # Copy into an in-memory zipfile
    data = response.read()
    mem_zf.write(data)

    # open as a zip
    zipf = zipfile.ZipFile(mem_zf)

    with io.TextIOWrapper(zipf.open('ACFTREF.txt', 'r')) as csvfile:
        aircraft = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(aircraft, None)

        for row in aircraft:
            acft[row[0]] = row[1].rstrip() + " " + row[2].rstrip()
            mdl[row[0]] = '"' + row[2].rstrip() + '"'

    num_rows = 0

    with io.TextIOWrapper(zipf.open('MASTER.txt', 'r')) as csvfile:
        airplanes = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(airplanes, None)

        for row in airplanes:
            num_rows = num_rows + 1
            print(row[33].rstrip().lower()+'\t'+row[0]+'\t'+mdl[row[2]]+'\t"' + acft[row[2]] + '"\t"' +row[6].rstrip()+'"' + '\n')

