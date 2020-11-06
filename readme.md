# Categorization of Playlists (e.g., mood versus genre playlists)

## Goal

For a research project on estimating the power of platforms vis-a-vis the content providers (here: Spotify versus major music labels), we require
a face-valid categorization of playlists on Spotify (e.g., to illustrate power differences in genre categories, compared to mood or activity categories). The raw data (retrieved from the API of Chartmetric.com) contains playlist names, and up to six associated tag words. However, absent from the data are broader categories (e.g. "EDM", "rock", "workout", "activity").

## Solution

Apply association rule mining on the tag words; use category names from Spotify's "browse" section (see also everynoise.com/worldbrowser.cgi for a list of these names) to learn categorizations from the playlists' tag words. Association rule mining allows playlists to be associated with *multiple* categories (e.g., a playlist can belong both to the "chill" and the "EDM" category).

## Details

### Inputs and outputs

- Input: List of up to six tag words associated with each playlist tracked by Chartmetric.com (in April 2020).
- Output: Playlists and their associated categories

### Description of the methodology

Our main objective is to characterize Spotify playlists in terms of genre, mood, and activity labels. As playlists consist of a variety of tracks, they typically represent multiple subgenres or mood/activity labels. For instance, the *Latin Pop Hits* playlist is associated with both a `latin` and `pop` keyword. Similarly, many workout playlists can be assigned a `dance` and `activity` keyword. 

The input data contains a list of up to six micro tag words for each playlist. In total there are 1460 unique tag words. The challenge, therefore, lies in reducing the dimensions of the data set while maintaining the major labels. 

Several methods exist to create clusters of data points that have similar values within each cluster but differ from other clusters. However, these algorithms (e.g., K-Means) classify each record in a single cluster, while most playlists belong to multiple labels. Further, clustering methods do not work well with high-dimensional sparse and binary datasets like ours <sup>1</sup>. Therefore, we adopt a different approach, in which we identify pairs of tag words that frequently occur together using association rule mining. In the marketing literature this method is also known as market basket analysis and is based on the idea that if you buy a certain group of items (e.g., bread), you are more (or less) likely to buy another group of items (e.g., butter). This approach requires an input data set in which the rows and columns are transactions and products, respectively. Cells take on the value 1 if a product occurs in a transaction and 0 otherwise. In the same way, we construct a matrix in which rows and columns represent playlists and tag words, respectively. Next, we describe the association rule mining approach we deployed. 

First, we draw a random sample of 100.000 playlists (+/- 10%) for computational reasons. Second, we filter down playlists that contain a major genre tag word (e.g., `pop`)<sup>2</sup>. We choose these tag words on the basis of the actual genres in the Spotify application. Third, we apply association rule mining to determine frequently co-occurring tag words within each of these subsets (e.g., `pop rap` → `hip hop`) <sup>3</sup>. This means that playlists that contain the tag word pop rap typically also have the tag word hip hop. Fourth, we assign all playlists that contain one or more of the tag words found in the association rules to the major genre tag word. For instance, all playlists that contain the tag word `pop rap` or `rap` are assigned to the `hip hop` cluster. Fifth, we repeat this procedure for all major genres which yields a matrix with 32 columns in which each playlist is assigned to one or more clusters <sup>4</sup>. The size of the top 10 clusters in terms of the number of playlists is presented in the table below. A matrix of the absolute and normalized label pair playlist counts is available in the `gen` folder.

*Notes:* Labels are sorted on "Playlists" which is the percentage of all playlists that are assigned to a label. Since playlists can be related to multiple labels the sum of the pecentages exceeds 100%. Market share is the number of followers of playlists in a label divided by the total number of followers.

<hr>

<sup>1</sup> K-means and K-modes yield highly unbalanced clusters in which there is one cluster that contains over 90% of all records and several small clusters. The Density-Based Spatial Clustering of Applications (DBSCAN) method runs into a similar issue in which most points are classified as noise. 

<sup>2</sup> Out of the 1,215,300 playlists 199,124 playlists do not contain any tag words at all. We dropped these records as their total market share is only 2.2%.  

<sup>3</sup> As input parameters for the Apriori algorithm we choose a minimum support level of 10%, lift greater than 1, and a minimum confidence of 90%. Inspection of the output shows that these results are face-valid (Appendix X).

<sup>4</sup> To validate our results, we apply a variety of cluster algorithms (K-Modes, K-Means, Hierarchical Clustering (ward, single linkage, complete linkage), and Bird) to the output of association rule mining. We find that the cluster performance expressed as the silhouette score is highest for the original number of columns. This also holds when we split up the data into genre (e.g., `pop`) and non-genre (e.g., `activity`) labels before we apply clustering techniques. As such, the output we got is already optimal and there is no need for further clustering. This provides additional evidence for the validity of our approach.

## Running instructions

### Dependencies

Please follow the installation guide on http://tilburgsciencehub.com/.

- Make. [Installation Guide](http://tilburgsciencehub.com/setup/make).
- Python. [Installation Guide](http://tilburgsciencehub.com/setup/python/).
- R. [Installation Guide](http://tilburgsciencehub.com/setup/r/).
- For R packages, see source code files (lines starting with `library`).
- For Python packages, see source code files (lines starting with `from ... import` or `import`)

### Running the code

Open your command line/terminal:

- Navigate to the directory in which this readme file resides, by typing `pwd` (Mac) or `dir` (Windows) in terminal

  - if not, type `cd yourpath/` to change your directory to the correct one.
  
- Type `make` in the command line.

- *Generated files:*
	- Association rules: `gen/data-preparation/output/rules.csv`
	- Playlist classification: `gen/data-preparation/output/playlist_clusters.csv`
	- Silhouette score line charts: `gen/data-preparation/output/figures`
	- Label pairs (absolute): `gen/data-preparation/output/label_pairs_abs.csv`
	- Label pairs (normalized): `gen/data-preparation/output/label_pairs_norm.csv`

### Directory Structure

```txt
├── data (directory with zipped raw data; 50MB)
├── gen
│   ├── data-preparation
│   │   ├── input
│   │   ├── output (final output of the data-prep workflow)
│   │   └── temp (directory with unzipped raw data, and other temp files)
│   └── figures
└── src
    ├── analysis
    ├── data-preparation [currently available]
    └── paper
```
