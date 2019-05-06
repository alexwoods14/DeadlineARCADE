#!/usr/bin/env python3

from datetime import datetime
import sys
import requests
from iCal import iCal


def main():
    start = datetime.now()
    if("http" in sys.argv[1]):
        data = requests.get(sys.argv[1]).text# url is http feed
    else:
        with open(sys.argv[1], 'r') as content_file:
            data = content_file.read()


    cal = iCal(data)
    #print("time taken to load data:(ms) ",(datetime.now() - start).total_seconds() * 1000)

    nextDeadline = cal.next(sys.argv[2].upper(), datetime.now())

    if nextDeadline is not None:
        print(nextDeadline)
    else:
        print("Not a valid course unit")
    
    
    #MyManchester week 0 is 17th Sept 2018

main()
