# Clustering Algorithm for the Playlist Ecosystem at Spotify

## Goal & Relevance

For an ongoing research project on estimating the power of platforms (here: Spotify) vis-a-vis the content providers (here: major labels), we require
a face-valid classification of 1.2m playlists on Spotify. This is important so that we can credibly illustrate power differences across multiple categories of playlists (e.g., "genre" versus "mood"). As an input data set, we use a list of up to six tag words associated with each playlist tracked by Chartmetric.com (in April 2020). Below we describe the method used to classify each playlist to one or more clusters. 

## Methodology

Our main objective is to construct a set of clusters that well-represent all music genres, moods, and activities. As an input data set, we use a list of up to six tag words associated with each playlist which can be converted into a boolean matrix of 1.2m rows by 1460 columns. Rows and columns denote individual playlists and tag words, respectively. Cells take on the value 1 if a tag word in the column is present in a playlist and 0 otherwise. This high-dimensional data requires us to apply dimensionality reduction and feature engineering techniques before clustering because i) the pairwise distance matrix cannot be computed for a data set of this size, ii) data sparsity yields highly imbalanced clusters, and iii) mood and activity playlists are not captured by the available tag words. 

First, we draw a random sample of 100.000 playlists (+/- 10%). Second, we reduce the number of dimensions by identifying common relationships in Spotify music genres ([Everynoise](https://everynoise.com/worldbrowser.cgi)). More specifically, for each genre we apply association rule mining to determine frequently co-occurring tag words (e.g., “dance pop” and “pop”). Then, we assign all playlists that contain any of the tag words found in the association rules to the given genre. This way we reduce the number of columns from 1460 to 31. Third, we seek for common phrases related to mood and activity playlists (e.g., “chill” and “workout”) in the playlist names and assign matching records a “mood” and “activity label”, respectively. 

## Results

* Out of the 1,215,300 playlists 199,124 playlists do not contain any tag words at all. We dropped these records as their total market share is only 2.2%.  
* Given a minimum support and confidence level of 1% and 90% respectively, we derive 503 association rules across 31 labels. For instance, all playlists that contain any of the following tagwords are assigned to the `afro` cluster: `afrobeat`, `afropop`, `alternative r&b`, `indie r&b`, `kwaito house`, `south african hip hop`, `south african pop`, or `world`. 
* We derived a total of 2867 mood and 2707 activities playlists from the playlist names.
* Playlists are assigned to 1-16 clusters (12.3% of the playlists are unclassified as none of their tag words were related to an association rule). The table below indicates to how many clusters each playlist is assigned.

| #Clusters | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 
| :--- | :--- | :--- | :--- | :--- | :--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- |
| Percentage | 23.1% | 12.7% | 11.8% | 18.0% | 5.5% | 4.3% | 6.3% | 2.4% | 3.3% | 10.4% | 1.5% | 0.4% | 0.4% | 0.1% | <0.1% | <0.1% | 

* There is high variability in cluster sizes ranging from 0.3% (`activity`) to 54.2% (`pop`). Note that playlists are assigned to multiple columns. Hence, the sum of the percentages exceeds 100%.

| `activity` | `afro` | `alternative` | `anime` | `arab` | `blues` | `chill` | `christian music` | `classical` | `comedy` | `country` | `desi` | `electronic / dance` | `focus` | `folk & acoustic` | `funk` | `hip hop` | `indie` | `jazz` | `latin` | `metal` | `mood` | `party` | `pop` | `punk` | `r&b` | `regional mexican` | `rock` | `romance` | `sleep` | `soul` | `student` | `video game music` | 
|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|
|0.3%|1.8%|28.1%|1.1%|0.1%|34.1%|4.4%|2.5%|4.4%|21.1%|19.5%|1.3%|6.8%|7.7%|6.5%|11.2%|23.8%|16.8%|6.6%|13.9%|9.3%|0.3%|7.1%|54.2%|19.4%|24.7%|1.4%|44.8%|13.9%|1.6%|26.7%|15.4%|2.3%|

* We applied a variety of cluster algorithms (K-Modes, K-Means, Hierarchical Clustering (ward, single linkage, complete linkage), and Bird) on the output file of the association rule mining. However, the cluster results consistently indicate that there is no need for further clustering. That is, the silhouette score is highest for the original number of columns. 

 
## Dependencies

Please follow the installation guide on http://tilburgsciencehub.com/.

- Make. [Installation Guide](http://tilburgsciencehub.com/setup/make).
- Python. [Installation Guide](http://tilburgsciencehub.com/setup/python/).
- R. [Installation Guide](http://tilburgsciencehub.com/setup/r/).
- For R packages, see source code files (lines starting with `library`).

## How to run it

Open your command line tool:

- Navigate to the directory in which this readme file resides, by typing `pwd` (Mac) or `dir` (Windows) in terminal

  - if not, type `cd yourpath/` to change your directory to the correct one.
  
- Type `make` in the command line.

- *Generated files:*
	- Association rules: `gen/data-preparation/output/rules.csv`
	- Playlist classification: `gen/data-preparation/output/playlist_clusters.csv`
	- Silhouette score line charts: `gen/data-preparation/output/figures`

## Directory Structure

```txt
├── data (directory with zipped raw data)
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
