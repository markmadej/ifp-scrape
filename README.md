# ifp-scrape

This is a script designed to scrape player listing / ranking data from the official [IFP tour site](http://www.ifptour.com).

## I'm not some computer nerd, I just want the data

[Here is a spreadsheet](finalData/ifp_points_2017-11-28.xlsx) with the most current IFP points data.

## Prerequisites

You will need to have Python installed.  This most recently ran successfully using Python 2.7.14 and I have not tested it on other versions.  You will need to use `pip` to install the `selenium` package and possibly others.  

## Supported Platforms

I've only run this on a Mac - you may experience some hiccups on other platforms.  

## Script overview

The scraping process is broken down into two parts.  First is the collection of all names.  The second is going through each name and extracting the singles/doubles points for both open and women categories.  The two processes communicate by sharing a data file.  This is not the most robust design, but it suited me fine as a first attempt at this.   

### Speed caveat

Please note that this script takes a LONG time to run!  The name collection algorithm is very slow and inefficient as currently designed.  Expect both the name and point collection scripts to take multiple days to complete.  

### Name collection process

To kick off the name collection process, run this command:

```
python2 ifpnamecollection.py
```

First, the script will look for a file named `allNames.txt` in the current directory.  That contains the full list of names the program has found so far.  It will also look for a file named `sequence.data` that contains the most recent alphabetic sequence this program is using to crawl the IFP site.  Storing the current sequence in this file is what allows us to easily stop and restart this application while retaining our progress.  

As the program runs it will append newly found names to `allNames.txt`.  The script will finish running once it cycles through all alphabetic sequences.  

### Virtual environment

Install virtualenvwrapper per [their installation docs](http://virtualenvwrapper.readthedocs.io/en/latest/install.html).
```
pip2 install virtualenvwrapper
```
Then add these lines to your .bash_profile or similar:
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Then run this (from inside the ifp-scrape directory):
```
source ~/.bash_profile
mkvirtualenv -a $PWD ifp
```

### Install necessary libraries
Run this command once inside your virtual environment:
```
pip install -r requirements.txt
```

### Docker!

You have the option to run using Firefox windows that pop up on your machine, or you can [install Docker](https://docs.docker.com/engine/installation/).  If you choose the Docker route, you need to run these commands before starting the name/point scraping scripts, and you also need to run the scripts with a `-docker` flag.

```
docker pull selenium/standalone-firefox-debug
docker run -d -p 4444:4444 --shm-size 2g selenium/standalone-firefox-debug:latest
```

Run those commands first before running the scripts.

### Point collection process

To kick off the point collection process with local Firefox windows, run this:

```
python2 ifppointcollection.py -local
```

To run the script using Docker, use this command:
```
python2 ifppointcollection.py -docker
```

This script loads all names from the `allNames.txt` file (from the ifpnamecollection process).  It then loads everything in `allPoints.txt`, the aggregation of names along with the 4 associated points.  The script then loops through all names found in `allNames.txt` but not `allPoints.txt`, and it attempts to retrieve that data.  The script finishes when all of those are attempted.  

While you can have the name and point collection programs running concurrently, you'll need to restart the point collection process after the final names have been collected.  The point collection process loads those at the start of its run and will not pick up new names after that initial read.  

## Results

Once both the name and point collection scripts have run to completion, all results will be in the file `allPoints.txt`.  Each row will be in the following format:

```
[NAME]$$$$[OPEN SINGLES],[OPEN DOUBLES],[WOMENS SINGLES],[WOMENS DOUBLES]
```

Some of the names do have commas in them, so importing these into Excel or whatever via CSV import may not be that easy (hence the `$$$$` as a workaround separator).  Blame the data. ;)

## Running tests

You can run the test suite via this command:

```
python2 test.py
```
