# Analyzing RFCs and I-Ds

This project is developing code for the automated analysis of the text of Requests for Comment (RFCs) published by the Internet Engineering Task Force, as part of a larger research project studying privacy in technical standard-setting.

For more information, if you want to use these tools or collaborate on their development, please [contact Nick Doty](mailto:npdoty@ischool.berkeley.edu).

[Some basic graphs produced with this code are available online.](https://npdoty.name/rfc-analysis/graphs/)

## Usage

Scripts are not fully parameterized or user friendly. Current usage pattern:

* clone the repository
* download all RFCs (see "Getting the documents" below) as .txt into a `RFC-all` directory within the main directory of the repository
* configure by copying `config.ini.example` to `config.ini` and pointing it to your downloaded RFCs
* `python search.py` will create a file `rfc-search.json` with section titles and lengths and word search counts for every available RFC

Other functionality:

* changes to search.py allow for basic string matching against all RFCs (or similar code for all W3C TRs)
* the `graphs/` directory contains `d3.js` visualizations of some of the measurements

## Getting the documents

There are several thousand RFCs and many more drafts and other IETF docs. You can download some or all of those documents for easier local analysis.

### Rsync all the documents via `ietf-cli`

Clone the [ietf-cli](https://github.com/paulehoffman/ietf-cli), add the config file to an appropriate location (and specify where you want all the documents synced) and run `./ietf mirror` to download all RFCs, drafts and some minutes and other documents. It's more than 2 GB of data and takes at least a few minutes to download.

### Just download the RFCs

The RFC Editor maintains zip and tar files of all the RFCs, in TXT and PDF formats, for download with your browser. The compressed `RFC-all.zip` file is a couple hundred megabytes.

## See also

* [Bigbang, a toolkit for studying communications data from collaborative projects](hthttps://github.com/datactive/bigbang)
* [ietf-data, access the IETF DataTracker](https://github.com/glasgow-ipl/ietfdata)
* [IETF Tools, a list of utilities](https://tools.ietf.org/)