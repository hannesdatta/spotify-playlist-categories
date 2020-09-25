# Clustering Algorithm for the Playlist Ecosystem at Spotify

## Goal & Relevance

For an ongoing research project on estimating the power of platforms (here: Spotify) vis-a-vis the content providers (here: major labels), we require
a face-valid classification of 1.2m playlists on Spotify. This is important so that we can credibly illustrate power differences across multiple categories of playlists (e.g., "genre" versus "mood"). As an input data set, we use a list of up to six tag words associated with each playlist tracked by Chartmetric.com (in April 2020). Below we describe the method used to classify each playlist to one or more clusters. 

## Methodology

Our main objective is to characterize Spotify playlists in terms of genre, mood, and activity labels. As playlists consist of a variety of tracks they typically represent multiple subgenres and labels. For instance, the *Latin Pop Hits* playlist is associated with both a `latin` and `pop` label. Similarly, many workout playlists can be assigned a `dance` and `activity` label. However, our input data only contains a list of up to six micro tag words for each playlist. In total there are 1460 unique tag words. The challenge, therefore, lies in reducing the dimensions of the data set while maintaining the major labels. 

Several methods exist to create clusters of data points that have similar values within-group, but differ from other clusters. These cluster algorithms typically require a pairwise distance matrix as input data. Given the high-dimensional data structure of ours (1.2M rows x 1460 columns), however, the distance matrix cannot be computed. More scalable cluster methods exist (e.g., K-means), but they do not work well with sparse and binary datasets like ours <sup>1</sup>. Therefore, we adopt a different approach in we identify pairs of tag words that frequently occur together using association rule mining. In the marketing literature this method is also known as market basket analysis and is based on the idea that if you buy a certain group of items (e.g., bread), you are more (or less) likely to buy another group of items (e.g., butter). This approach requires a input data set in which the rows and columns are transactions and products, respectively. Cells take on the value 1 if a product occurs in a transaction and 0 otherwise. In the same way, we construct a matrix in which rows and columns represent playlists and tag words, respectively. Next, we describe the association rule mining approach we used. 

First, we draw a random sample of 100.000 playlists. Second, we filter down playlists that contain a major genre tag word (e.g., `pop`). We choose these tag words on the basis of the actual genres in the Spotify application. Third, we apply association rule mining to determine frequently co-occurring tag words within each subset (e.g., `dance pop` → `pop`) <sup>2</sup>. This means that playlists that contain the tag word dance pop typically also have the tag word pop. Fourth, we assign all playlists that contain one or more of the tag words found in the association rules to the major genre tag word. For instance, all playlists that contain the tag word dance pop, pop rock, rap, or hip hop are assigned to the pop cluster. Fifth, we repeat this process for all major genres which yields a matrix with 32 columns in which each playlist is assigned to one or more labels <sup>3</sup>. 


<sup>1</sup> K-means and K-mode yield highly unbalanced clusters in which there is one cluster that contains over 90% of all records and several small clusters. The Density-Based Spatial Clustering of Applications (DBSCAN) method runs into a similar issue in which most points are classified as noise. 

<sup>2</sup> As input parameters of the algorithm we choose a minimum support level of 10%, lift greater than 1, and a minimum confidence of 90%. 

<sup>3</sup> To validate our results, we applied K-modes clustering to the output of association rule mining for various levels of K. We find that the cluster performance expressed as the silhouette score is highest for the original number of columns. As such, the output we got is already optimal and there is no need for further clustering. This provides additional evidence for the validity of our approach. The size of the top 10 clusters in terms of the number of playlists and market share is presented in Table 1.

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
