import urllib.request, urllib.parse, urllib.error
import re
import os
from pprint import pprint as pp

ARCHIVE_DIR = "RFC-all"

def archived_txt(rfc_number):
  arc_file = os.path.join(ARCHIVE_DIR, rfc_number.lower() + '.txt')
  if os.path.isfile(arc_file):
    return arc_file
  return None

def archive_directory(list_name):
  arc_dir = os.path.join(ARCHIVE_DIR,list_name)
  if not os.path.exists(arc_dir):
      os.makedirs(arc_dir)
  return arc_dir