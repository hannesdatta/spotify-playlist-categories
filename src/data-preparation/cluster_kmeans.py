from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans as KMeansFast
import dask.dataframe
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import random


print('loading data')
data = dask.dataframe.read_csv('../../gen/data-preparation/temp/playlist-tags.csv')

print('converting to numpy')
df = data.compute()
X = df.to_numpy()[:,1:]
X.shape


def fixed_k(k):
    print('starting k-means algorithm with ' + str(k) + ' classes...')
    
    # KMeansFast is a much faster algorithm than KMeans (it learns
    # on a sample.
    
    # kmeans = KMeans(n_clusters=10, random_state=0, n_jobs=-2).fit(X)
    kmeans = KMeansFast(n_clusters=k, random_state=0).fit(X)
    
    print('Done clustering. Now writing result to file.')
    out=pd.DataFrame({'id': df.iloc[:,0], 'cluster_id': kmeans.labels_+1})
        
    out.to_csv('../../gen/data-preparation/output/cluster_output.csv', index = False)
    print('Done.')

# taken from: https://anaconda.org/milesgranger/gap-statistic/notebook
def optimalK(data, nrefs=3, minClusters = 10, maxClusters=20):
    """
    Calculates KMeans optimal K using Gap Statistic from Tibshirani, Walther, Hastie
    Params:
        data: ndarry of shape (n_samples, n_features)
        nrefs: number of sample reference datasets to create
        maxClusters: Maximum number of clusters to test for
    Returns: (gaps, optimalK)
    """
    
    clusterRange = range(minClusters, maxClusters+1)
    
    gaps = np.zeros((len(clusterRange),))
    resultsdf = pd.DataFrame({'clusterCount':[], 'gap':[]})
    for gap_index, k in enumerate(clusterRange):
        print('Calculating for cluster size ' + str(k))
        # Holder for reference dispersion results
        refDisps = np.zeros(nrefs)

        # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
        for i in range(nrefs):
            
            # Create new random reference set
            randomReference = np.random.random_sample(size=data.shape)
            
            # Fit to it
            km = KMeansFast(k)
            km.fit(randomReference)
            
            refDisp = km.inertia_
            refDisps[i] = refDisp

        # Fit cluster to original data and create dispersion
        km = KMeansFast(k)
        km.fit(data)
        
        preds = km.labels_
        
        origDisp = km.inertia_
        
        # Calculate gap statistic
        gap = np.log(np.mean(refDisps)) - np.log(origDisp)

        # Assign this loop's gap statistic to gaps
        gaps[gap_index] = gap
        #
        if (k>1): 
            sil=silhouette_score(data, preds) 
        else:
            sil = 0
        
        resultsdf = resultsdf.append({'clusterCount':k, 
                                      'gap':gap, 
                                      'inertia': km.inertia_,
                                      'silhouette': sil}, ignore_index=True)

    return (clusterRange[gaps.argmax()], resultsdf)  # Plus 1 because index of 0 means 1 cluster is optimal, index 2 = 3 clusters are optimal


# Set random seed
random.seed(1234)

# Learn k 
# k, gapdf = optimalK(X, nrefs=3,minClusters=5, maxClusters=7)
# print(gapdf)

# Estimate w/ k
# do not use optimal k right now; but fix to 5.
fixed_k(5)
