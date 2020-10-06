import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
from kmodes.kmodes import KModes
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn import metrics

#import data and draw random sample
np.random.seed(1)
df_pivot = pd.read_csv("../../gen/data-preparation/output/playlist_clusters.csv")
genres = ["afro", "alternative", "anime", "arab", "blues", "christian music", "classical", "country", "desi", "electronic/dance", "folk & acoustic", "funk", "hip hop", "indie", "jazz", "latin"]
non_genres = ["activity", "chill", "comedy", "focus", "mood", "party", "romance", "sleep", "student", "video game music"]

df_pivot_sample_ids = np.random.choice(df_pivot.index, 1000)
df_pivot_sample = df_pivot.loc[df_pivot.index.isin(df_pivot_sample_ids), df_pivot.columns[1:]]

# generate two subsets: data frame with genre and non-genre labels
df_pivot_sample_genre = df_pivot_sample[genres]
df_pivot_sample_non_genre = df_pivot_sample[non_genres]

# create figure folder if not already exists
path = "../../gen/figures"
if not os.path.exists(path):
    os.makedirs(path)

def plot_results(df, algorithm, sample):
    '''generate line chart that represents the silhouette score for a given algorithm and number of clusters'''
    pd.DataFrame([value for value in df.values()], range(2,len(sample.columns))).plot()
    plt.legend("")
    plt.ylabel('silhouette', fontsize=12)
    plt.xlabel('#clusters', fontsize=12)
    plt.title(algorithm)
    if 'activity' in sample.columns: 
        plt.savefig('../../gen/figures/non_genre_' + algorithm + '.png')
    else: 
        plt.savefig('../../gen/figures/genre_' + algorithm + '.png')

def clustering(df, method, algorithm, file_name, **kwargs):
    '''general function that accepts multiple cluster methods and computes the silhouette score for 2-33 clusters'''
    cluster_labels = {}
    silhouette_score = {}
    
    for n_clusters in range(2,len(df.columns)):
        km = method(n_clusters=n_clusters, **kwargs)
        cluster_labels[n_clusters] = km.fit_predict(df)
        silhouette_score[n_clusters] = metrics.silhouette_score(df, cluster_labels[n_clusters])
        
    # determine ideal cluster configuration
    optimum_clusters = max(silhouette_score, key=silhouette_score.get)
    optimum_silhouette = max(silhouette_score.values())
    plot_results(silhouette_score, file_name, df)
    print("{0}: optimum #clusters = {1} (silhouette {2: .3f})".format(algorithm, optimum_clusters, optimum_silhouette))
    return silhouette_score
    
# run various cluster algorithms -> more clusters = better fit -> conclusion: no need for clustering association rule mining output
def cluster_algorithms_comparison(df_pivot_sample_non_genre, df_pivot_sample_genre):
    for sample in [df_pivot_sample_non_genre, df_pivot_sample_genre]:
        print("- - - - - - - NON-GENRE - - - - - - - ") if 'activity' in sample.columns else print("- - - - - - - GENRE - - - - - - - ")
        k_modes = clustering(sample, KModes, "K-Modes", "k_modes", init="Cao", n_init=5)
        k_means = clustering(sample, KMeans, "K-Means", "k_means")
        ward = clustering(sample, AgglomerativeClustering, "Hierarchical Clustering (Ward's method)", "hc_ward", linkage="ward")
        complete_linkage = clustering(sample, AgglomerativeClustering, "Hierarchical Clustering (complete linkage)", "hc_complete", linkage="complete")
        single_linkage = clustering(sample, AgglomerativeClustering, "Hierarchical Clustering (single linkage)", "hc_single", linkage="single")
    print("FIT STATISTICS ARE STORED IN GEN/FIGURES")

cluster_algorithms_comparison(df_pivot_sample_non_genre, df_pivot_sample_genre)