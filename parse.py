import datetime
from gather import *
import json
import os
import pandas as pd
import re
from search import filename_from_rfc_number, iterate_rfc_files, normalize_rfc_number, JSON_INPUT_FILENAME

author_rexp = "   (\w\. [\w-]+,? ?\w+\.?)$"
affiliation_rexp = "   (\w[\w \.,\+-]+)$"
date_rexp = "   (?:\d?(\d )?)(\w+ \d\d\d\d)$"


def extract_metadata(filename):
    """
    Returns a list of author, affiliation, and date
    dicts in order that they appear in the RFC text.
    """
    
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
                metadata.append({'date' : date_match.groups()[1]})
            elif affiliation_match:
                metadata.append({'affiliation' : affiliation_match[1]})
            elif not header:
                return metadata

    raise Exception("%s : Metadata parser did not find end of whitespace header." % (filename))

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
                'date' : datetime.datetime.strptime(
                    entry['date'],
                    "%B %Y"),
                'authors' : people
            }

def main():
    records = []

    filenames = os.listdir('RFC-all')
   
    for filename in filenames:
        fn = filename_from_rfc_number(filename[:-4])
        if fn is not None:
            metadata = extract_metadata(fn)
            cm = compile_metadata(metadata)

            if cm is not None and 'authors' in cm:
                for author in cm['authors']:
                    records.append({
                        'date' : cm['date'],
                        'name' : author['name'],
                        'affiliation' : author['affiliation'],
                        'rfc' : filename[:-4]
                    })

    df = pd.DataFrame.from_records(records)
    print(df)
    df.to_csv("authors.csv")
        
if __name__== "__main__":
    main()
