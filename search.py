import urllib.request, urllib.error, urllib.parse
import re
import os
from pprint import pprint as pp
import csv
from bs4 import BeautifulSoup
import json
from gather import * 
import logging
import xml.etree.ElementTree
from optparse import OptionParser

JSON_OUTPUT_FILENAME = 'rfc-search.json'
RFC_INDEX_FILENAME = 'rfc-index.xml'

search_terms = ['privacy','security','Web']

def main():
  parser = OptionParser()
  parser.add_option("-r", "--rfc", 
                    action="store_true", 
                    dest="search_rfcs", 
                    default=False, 
                    help="Search all RFCs listed in the local RFC index.")
  parser.add_option("-i", "--id", 
                    action="store_true", 
                    dest="search_ids", 
                    default=False, 
                    help="Search Internet-Drafts, as specified in configuration.")
  # parser.add_option("-s", "--section", 
  #                   action="store_true", 
  #                   dest="sections", 
  #                   default=True, 
  #                   help="Parse sections and their lengths.")
  # parser.add_option("-t", "--terms", 
  #                   action="store_true", 
  #                   dest="terms", 
  #                   default=True, 
  #                   help="Search for term frequency.")

  (options, args) = parser.parse_args()

  if (options.search_rfcs == False) and (options.search_ids == False):
    parser.error('Must search either RFCs or I-Ds.')

  if options.search_rfcs:
    search_rfcs()

  if options.search_ids:
    raise NotImplementedError

def normalize_rfc_number(number):
  just_number = number.lower().split('rfc')[1]
  normalized = 'rfc' + just_number.lstrip('0')
  return normalized

def search_rfcs():
  with open(os.path.join(ARCHIVE_DIR, RFC_INDEX_FILENAME), 'r') as xmlfile:
    root = xml.etree.ElementTree.parse(xmlfile)
    
    ns = {'rfc':'http://www.rfc-editor.org/rfc-index'}
    entries_elements = root.findall('.//rfc:rfc-entry', ns)
    entries = []

    for entry_element in entries_elements:
      doc_id = entry_element.find('./rfc:doc-id', ns)
      filename = archived_txt(normalize_rfc_number(doc_id.text))
      
      entry = {'rfc_number': doc_id.text,
              'title': entry_element.find('./rfc:title', ns).text,
              'year': entry_element.find('.//rfc:year', ns).text
              }

      if not filename:
        logging.warning(doc_id.text + ' has no available file.')
        continue
      
      with open(filename, 'r', errors='replace') as txt_file:    
        lines = txt_file.readlines()
        logging.info(filename)
        entry['lines'] = len(lines)
        
        # identifying the section titles
        potential_section_name = False
        current_section_name = ''
        section_name = ''
        empty_line = False
        previous_empty_line = False
        line_count = 0
        entry['sections'] = {}
        
        for line in lines:
          if re.match('\s+$', line):
            empty_line = True
          else:
            empty_line = False
          
          if potential_section_name and empty_line:
            logging.info(section_name)
            entry['sections'][current_section_name] = line_count
            current_section_name = section_name
            line_count = 1
            potential_section_name = False
            previous_empty_line = empty_line
            continue
          
          match = re.match('\d+\.?\s+([A-Z].+)$', line)
          non_numbered_match = re.match('([A-Z][\w\s\d-]+)$', line)
          if match:
            if not re.search('\.\.\.', line) and (not re.search('\s\s+\d+\s$', line)) and previous_empty_line:
              # multiple dots or multiple spaces before a number is a ToC entry, 
              # previous line should be blank
              potential_section_name = True
              section_name = match.group(1).strip()
            else:
              potential_section_name = False
          elif non_numbered_match:
            if not re.search('\s\s', line) and previous_empty_line: 
              # shouldn't have multiple consecutive spaces, previous line should be blank
              potential_section_name = True
              section_name = non_numbered_match.group(1).strip()
            else:
              potential_section_name = False
          else:
            potential_section_name = False  
          
          previous_empty_line = empty_line
          line_count += 1
        
      with open(filename, 'r', errors='replace') as txt_file:
        text = txt_file.read()

        for term in search_terms:
          matches = re.findall(term, text, flags=re.IGNORECASE)
          entry[term+'_search'] = len(matches)  

      entries.append(entry)    
    
    with open(JSON_OUTPUT_FILENAME, 'w') as outfile:
      json.dump(entries, outfile)

if __name__ == "__main__":
    main()