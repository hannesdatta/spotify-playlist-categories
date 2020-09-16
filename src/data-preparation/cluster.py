import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
from kmodes.kmodes import KModes
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import Birch
from sklearn import metrics

#import data and draw random sample
np.random.seed(1)
df_pivot = pd.read_csv("../../gen/data-preparation/output/playlist_clusters.csv")
df_pivot_sample_ids = np.random.choice(df_pivot.index, 100)
df_pivot_sample = df_pivot.loc[df_pivot.index.isin(df_pivot_sample_ids), df_pivot.columns[1:]]

# create figure folder if not already exists
path = "../../gen/figures"
if not os.path.exists(path):
    os.makedirs(path)

def plot_results(df, algorithm, df_pivot_sample):
    '''generate line chart that represents the silhouette score for a given algorithm and number of clusters'''
    pd.DataFrame([value for value in df.values()], range(2,len(df_pivot_sample.columns))).plot()
    plt.legend("")
    plt.ylabel('silhouette', fontsize=12)
    plt.xlabel('#clusters', fontsize=12)
    plt.title(algorithm)
    plt.savefig('../../gen/figures/' + algorithm + '.png')

def clustering(df, method, algorithm, file_name, **kwargs):
    '''general function that accepts multiple cluster methods and computes the silhouette score for 2-33 clusters'''
    cluster_labels = {}
    silhouette_score = {}
    
    for n_clusters in range(2,len(df_pivot_sample.columns)):
        km = method(n_clusters=n_clusters, **kwargs)
        cluster_labels[n_clusters] = km.fit_predict(df)
        silhouette_score[n_clusters] = metrics.silhouette_score(df_pivot_sample, cluster_labels[n_clusters])
        
    # determine ideal cluster configuration
    optimum_clusters = max(silhouette_score, key=silhouette_score.get)
    optimum_silhouette = max(silhouette_score.values())
    plot_results(silhouette_score, file_name, df_pivot_sample)
    print("{0}: optimum #clusters = {1} (silhouette {2: .3f})".format(algorithm, optimum_clusters, optimum_silhouette))
    return silhouette_score
    
# run various cluster algorithms -> more clusters = better fit -> conclusion: no need for clustering association rule mining output
k_modes = clustering(df_pivot_sample, KModes, "K-Modes", "k_modes", init="Cao", n_init=5)
k_means = clustering(df_pivot_sample, KMeans, "K-Means", "k_means")
ward = clustering(df_pivot_sample, AgglomerativeClustering, "Hierarchical Clustering (Ward's method)", "hc_ward", linkage="ward")
complete_linkage = clustering(df_pivot_sample, AgglomerativeClustering, "Hierarchical Clustering (complete linkage)", "hc_complete", linkage="complete")
single_linkage = clustering(df_pivot_sample, AgglomerativeClustering, "Hierarchical Clustering (single linkage)", "hc_single", linkage="single")
birch = clustering(df_pivot_sample, Birch, "Birch", "birch")