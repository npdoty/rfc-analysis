This project is developing code for the automated analysis of the text of Requests for Comment (RFCs) published by the Internet Engineering Task Force, as part of a larger research project studying privacy in technical standard-setting.

For more information, if you want to use these tools or collaborate on their development, please [contact Nick Doty](mailto:npdoty@ischool.berkeley.edu).

[Some basic graphs produced with this code are available online.](https://npdoty.name/rfc-analysis/graphs/)

## Usage

Scripts are not fully parameterized or user friendly. Current usage pattern:

* clone the repository
* download all RFCs as .txt into a `RFC-all` directory within the main directory of the repository
* (optional: downloaded an updated version of rfc-index.xml from the IETF)
* `python search.py` will create a file `rfc-search.json` with the section titles and lengths for every available RFC

Other functionality:

* changes to search.py allow for basic string matching against all RFCs (or similar code for all W3C TRs)
* the `graphs/` directory contains `d3.js` visualizations of some of the measurements

## See also

[Bigbang, a toolkit for studying communications data from collaborative projects](https://github.com/sbenthall/bigbang/)