from gather import *
import json
import os
import re
from search import filename_from_rfc_number, iterate_rfc_files, normalize_rfc_number, JSON_INPUT_FILENAME

author_rexp = "   (\w\. \w+)$"
affiliation_rexp = "   (\w[\w \.]+)$"
date_rexp = "   (\w+ \d\d\d\d)$"


def extract_metadata(rfc_filename):
    """
    Returns a list of author, affiliation, and date
    dicts in order that they appear in the RFC text.
    """

    filename = filename_from_rfc_number(rfc_filename[:-4])

    with open(filename, 'r') as txt_file:
        lines = txt_file.readlines()

        # track whitespace heaer before metadata
        header = True
        metadata = []

        for line in lines:
            author_match = re.search(author_rexp, line)
            affiliation_match = re.search(affiliation_rexp, line)
            date_match = re.search(date_rexp, line)
        
            if author_match:
                metadata.append({'author' : author_match[1]})
                header = False
            elif date_match:
                ## Note: date regexp is strictly more restrictive
                ## than affiliation regexp, so has to be tested first
                metadata.append({'date' : date_match[1]})
            elif affiliation_match:
                metadata.append({'affiliation' : affiliation_match[1]})
            elif not header:
                return metadata

    raise Exception("Metadata parser did not find end of whitespace header.")

def compile_metadata(metadata):
    """
    Input: List of name, affiliation, and date dicts
    Output: object with
        parsed date and
        matched names and affiliations.
    """
    names = []
    people = []

    for entry in metadata:
        if 'author' in entry:
            names.append(entry['author'])
        elif 'affiliation' in entry:
            for name in names:
                people.append({
                    'name' : name,
                    'affiliation' : entry['affiliation']
                })
            names = []
        elif 'date' in entry:
            return {
                'date' : entry['date'],
                'authors' : people
            }

def main():

    filenames = os.listdir('RFC-all')
   
    for filename in filenames:
        metadata = extract_metadata(filename)
        cm = compile_metadata(metadata)
        print(cm)
        
if __name__== "__main__":
    main()
