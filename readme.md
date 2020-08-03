# Clustering algorithm for the playlist ecosystem at Spotify

## Goal of this project: Update playlist clustering

For an ongoing research project on estimating the power of platforms (here:
Spotify) vis-a-vis the content providers (here: major labels), we require
a face-valid classification of 1.2m playlists on Spotify. This is important
so that we can credibly illustrate power differences across multiple categories of playlists 
(e.g., "genre" versus "mood"). 

As an input data set, we use a list of up to six tag words associated with
any of the 1.2m playlists tracked by Chartmetric.com (in April 2020). 
These keywords capture genres, and not moods/activities. 
The clustering procedure is rather rudimentary, using k-means 
clustering with fixed k.

### Requirements

- The clustering result should reflect the reality of Spotify's playlist ecosystem 
across genre, mood (e.g., "Chill") and activity (e.g., "running") playlists.
Some suggestions for assessing face validity: 
	- which playlist (names) are clustered together?
	- which tag words group together?
	- does the result tell apart genre from mood/activity playlists?
	- how big are the clusters? is there one dominating, or are there a few that stand out?
	- does the mapping somewhat correspond (and if only to some degree 
	of aggregation) with the categories at https://everynoise.com/worldbrowser.cgi?

- Currently, the classification uses only tag words as input, but meta characteristics from `playlists.csv` can be added
(e.g., even serialized playlist names). A first attempt at hard-coding activities and moods has been made.

- The clustering needs to be deterministic, i.e., re-running it with same inputs
and random seeds should always lead to the same clustering results. Is this feasible at all?

- There needs to be an evaluation table/figure that helps to label the clusters
(e.g., with most occuring tag words, etc.). Think of it is to be put in a paper
so that readers can assess the face validity of our procedure.

- Currently, the code runs on a sample of playlists (<30k); it needs to be scalable to 
classify all of the 1.2 million playlists.

- The resulting algorithm does not need to be k-means clustering; in fact, we do not
really care what algorithm it is, as long as it does a superb job in classifying the data.
 
 
## Dependencies

Please follow the installation guide on http://tilburgsciencehub.com/.

- Make. [Installation Guide](http://tilburgsciencehub.com/setup/make).
- Python. [Installation Guide](http://tilburgsciencehub.com/setup/python/).
- R. [Installation Guide](http://tilburgsciencehub.com/setup/r/).
- For R packages, see source code files (lines starting with `library`).

## Modules

- `data-preparation`: Downloads raw data, prepares data set for clustering, and runs clustering procedure.
- `analysis`: Not present yet
- `paper`: Not present yet

## How to run it

Open your command line tool:

- Navigate to the directory in which this readme file resides, by typing `pwd` (Mac) or `dir` (Windows) in terminal

  - if not, type `cd yourpath/` to change your directory to the correct one.
  
- Type `make` in the command line. 

## Directory Structure

```txt
├── data (directory with zipped raw data)
├── gen
│   ├── analysis
│   │   ├── input
│   │   ├── output
│   │   └── temp
│   ├── data-preparation
│   │   ├── input
│   │   ├── output (final output of the data-prep workflow)
│   │   └── temp (directory with unzipped raw data, and other temp files)
│   └── paper
│       ├── input
│       ├── output
│       └── temp
└── src
    ├── analysis
    ├── data-preparation [currently available]
    └── paper
```
