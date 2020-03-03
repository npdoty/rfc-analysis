from gather import *
import re
from search import normalize_rfc_number

author_rexp = "   (\w\. \w+)$"
affiliation_rexp = "   (\w[\w \.]+)$"
date_rexp = "   (\w+ \d\d\d\d)$"


def parse_metadata(rfc_number):
    filename = archived_txt(rfc_number)
    print(filename)

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

def main():
    # just a smoke test
    metadata = parse_metadata("rfc8012")
    print(metadata)
        
if __name__== "__main__":
    main()
