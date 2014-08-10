import urllib2
import urllib
import re
import os
from pprint import pprint as pp
import csv
from bs4 import BeautifulSoup
import json
from gather import * 
import logging

JSON_INPUT_FILENAME = 'rfc.json'
JSON_OUTPUT_FILENAME = 'rfc-search.json'

search_terms = ['privacy','security','Web']

def normalize_rfc_number(number):
  just_number = number.lower().split('rfc')[1]
  normalized = 'rfc' + just_number.lstrip('0')
  return normalized

with open(JSON_INPUT_FILENAME, 'r') as jsonfile:
  entries = json.load(jsonfile)
  
  for entry in entries:
    filename = archived_txt(normalize_rfc_number(entry['rfc_number']))
    
    if not filename:
      logging.warning(entry['rfc_number'] + ' has no available file.')
      #raise Exception(entry['rfc_number'] + ' has no available file.')
      continue
    
    with open(filename, 'r') as txt_file:
      text = txt_file.read()
      
      for term in search_terms:
        matches = re.findall(term, text, flags=re.IGNORECASE)
        entry[term+'_search'] = len(matches)
  
  with open(JSON_OUTPUT_FILENAME, 'wb') as outfile:
    outfile.write(json.dumps(entries))
