import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import re
import os
from pprint import pprint as pp
import csv
from bs4 import BeautifulSoup
import json
from gather import *
from datetime import *

RFC_INDEX_FILENAME = 'rfc-index.xml'

with open(RFC_INDEX_FILENAME, 'r') as xmlfile:
  xml = xmlfile.read()

  soup = BeautifulSoup(xml)
  
  rows = soup('rfc-entry')

  entries = list()

  for row in rows:
    try:
      entry = dict()
      entry['rfc_number'] = str(row.find('doc-id').string)
      pp(entry['rfc_number'])
      entry['title'] = str(row.find('title').string)
    
      date_string = ' '.join(
        ['01',
         str(row.select('date > month')[0].string),
         str(row.select('date > year')[0].string)])
      date_published = datetime.strptime(date_string, '%d %B %Y')
      entry['date_published'] = date_published.strftime('%Y-%m-%d')
      entries.append(entry)

      pp(len(entries))
    except Exception as e:
      print("%s: %s" % (entry['rfc_number'], e))

  # entries = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in entries)]

  with open('rfc.json', 'wb') as jsonfile:
    jsonfile.write(json.dumps(entries))