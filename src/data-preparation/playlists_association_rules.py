import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# ---------------------------- #
#       DATA PREPARATION       #
# ---------------------------- #

# mood and activity keywords
moods = {'mood', 'fuzzy', 'feel', 'rage', 'anger', 'angry', 'annoying', 'aggresive', 'interest', 'interesting', 'optimism', 'optimistic', 'ecstasy', 'joy', 'serenity', 'love', 'trust', 'acceptance', 'accepting', 'submission', 'terror', 'fear', 'awe', 'amaze', 'amazing', 'surprise', 'surprising', 'distraction', 'distracting', 'grief', 'sadness', 'sad', 'pensiveness', 'pensive', 'remorse', 'loathing', 'disgust', 'boredom', 'boring', 'bored', 'chill', 'active', 'cheerful', 'reflective', 'gloomy', 'humorous', 'humor', 'melancholy', 'romantic', 'mysterious', 'ominous', 'calm', 'lighthearted', 'hope', 'hopeful', 'fearful', 'tense', 'lonely', 'alone', 'happy', 'good', 'bad', 'suave', 'vibe', 'breakup', 'depressed', 'depression', 'emo', 'bored', 'heart broken'}
activities = {'sing', 'drive', 'dance', 'work', 'study', 'concentrate', 'read', 'workout', 'gym', 'party', 'sport', 'relax', 'cook', 'unwind', 'driving', 'roadtrip', 'vacation', 'flying', 'fly', 'sleep', 'travel', 'road', 'trip', 'training', 'train', 'eat', 'kitchen', 'run', 'dream', 'activity', 'active', 'ride', 'dancing', 'listen', 'discover', 'wake', 'up', 'wakeup', 'shower', 'riding', 'start', 'drink', 'jogging', 'jog', 'bbq', 'gaming', 'game', 'office', 'cycling', 'camping', 'fishing', 'hunting', 'fish', 'hunt', 'karaoke', 'poker', 'playing', 'cards'}

# derived from Everynoise World Browser (http://everynoise.com/worldbrowser.cgi)
genres = ['afro', 'alternative', 'anime', 'arab', 'blues', 'chill', 'christian music', 'classical', 'comedy', 'country', 'desi', 'electronic/dance', 'focus', 'folk & acoustic', 'funk', 'video game music', 'hip hop', 'indie', 'jazz', 'latin', 'metal', 'party', 'pop', 'punk', 'r&b', 'regional mexican', 'rock', 'romance', 'sleep', 'soul', 'student']    

# read data and prepare dataset
print("import data")
playlists = pd.read_csv('../../gen/data-preparation/temp/playlists.csv') # N=1,215,300
tags_playlists = pd.read_csv('../../gen/data-preparation/temp/tags-playlists.csv') # 1,016,176 unique playlist ids (thus 199,124 playlists do not have any playlist tagword) - see below
tags_playlists_meta = pd.read_csv('../../gen/data-preparation/temp/tags-playlists-meta.csv')
df = (pd.merge(tags_playlists, tags_playlists_meta, left_on='tagid', right_on='tagid')[['id', 'tagid', 'tag']]
    .sort_values('id')
    .reset_index(drop=True))

# playlists without tag words make up only 2.2% of the total market share (leaving out these playlists can therefore be justified)
unique_tags_playlists = set(tags_playlists.id.unique())
missing_ids = [id for id in playlists.id if id not in unique_tags_playlists]

followers_missing = playlists.loc[playlists.id.isin(missing_ids), 'followers'].sum()
total_followers = playlists.followers.sum()
print("market share playlists without any tag words: {0:.1f}%".format(followers_missing / total_followers * 100))

# remove leading and trailing spaces and hyphens
df['tag'] = df['tag'].apply(lambda x: x.strip(" ")).apply(lambda x: x.replace("-", " "))

# create a random sample of playlists
np.random.seed(1) # for reproducbility (every time the same sample and thus identical association rules)
df_ids = df['id'].unique()
df_sample_ids = np.random.choice(df_ids, 100000)
df_sample = df[df.id.isin(df_sample_ids)]

# turn data into pivot table as input for association rule mining (rows: playlists, columns: tags) 
basket = (df_sample.groupby(['id', 'tag'])['tagid']
   .count().unstack().reset_index().fillna(0)
   .set_index('id', drop=True))


# ---------------------------- #
#       MOODS & ACTIVITIES     #
# ---------------------------- #

def moods_activities_playlists(moods_activities):
    '''identify moods and activities playlists from playlist names (i.e., check if keywords appear in the playlist name)'''
    output = pd.DataFrame()
    
    for tag in moods_activities:
        matches = playlists[playlists.name.str.match(tag + "$|" + tag + "[ ]") == True].copy()
        if 'mood' in moods_activities:
            matches['cluster'] = 'mood'
        else: 
            matches['cluster'] = 'activity'
        output = pd.concat([output, matches]).reset_index(drop=True)
    return output[['id', 'cluster']]

# determine playlist ids related to moods (N=2867) and activities (N=2707) playlists
moods_matches = moods_activities_playlists(moods) 
activities_matches = moods_activities_playlists(activities) 
print("identified " + str(len(moods_matches)) + " moods playlists and " + str(len(activities_matches)) + " activities playlists")


# ---------------------------- #
#   ASSOCIATION RULE MINING    #
# ---------------------------- #

def tag_word_analysis(basket, genre, min_confidence, min_support):
    ''''
    1. select all playlists that contain a given main genre (e.g., pop)
    2. derive association rules of length 2, of which the lift exceeds 1, the confidence is greater than 90%, and the support exceeds a given level
    3. consider association rules of which the consequent is the main genre (e.g., dance pop -> pop)
    '''
    tag_cluster = pd.DataFrame()

    basket_genre = basket[basket[genre] == 1] # all playlists that contain the main genre
    frequent_itemsets = apriori(basket_genre, min_support=min_support, use_colnames=True, max_len=2)
    rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1).sort_values(['confidence', 'support'], ascending=False).reset_index(drop=True)
    rules = rules.loc[rules['confidence'] >= min_confidence, ['antecedents', 'consequents']]

    # restructure frozen set 
    for counter in range(len(rules)):
        antecedent, = rules.loc[counter, 'antecedents']
        consequent, = rules.loc[counter, 'consequents']
        if consequent == genre and antecedent not in genres: 
            tag_cluster_temp = pd.DataFrame([[antecedent, genre], [genre, genre]], columns=['tag', 'cluster'])
            tag_cluster = pd.concat([tag_cluster_temp, tag_cluster])
    tag_cluster = tag_cluster.drop_duplicates()
    
    return tag_cluster
    
# determine association rules within each main genre (note that one tagword may be associated with multiple clusters (e.g., soft rock -> rock & soft rock -> pop))
min_support=0.1 # changing the support level has a major impact on the outcomes (higher support = fewer association rules = fewer clusters)
min_confidence = .9
print("starting association rule mining with minimum confidence of " + str(min_confidence) + " and minimum support of " + str(min_support))
tag_clusters = pd.concat([tag_word_analysis(basket, genre, min_support=min_support, min_confidence=min_confidence) for genre in genres])
print("exported " + str(len(tag_clusters)) + " total association rules")
tag_clusters.to_csv("../../gen/data-preparation/output/rules.csv", index=False)


# ------------------------------- #
#  ASSIGN PLAYLISTS TO CLUSTERS   #
# ------------------------------- #

# add clusters to playlists 
df_cluster = pd.merge(df, tag_clusters, left_on='tag', right_on='tag')[['id', 'tagid', 'tag', 'cluster']]

# calculate number of playlists without any cluster (because none of the tagwords are related to any of the association rules; choosing a lower minimum support level will remedy this problem to a certain extent)
all_playlists = len(tags_playlists.id.unique())
num_playlists_output = len(df_cluster.id.unique())
print("{0:.1f}% of all playlists is not assigned to any cluster".format((all_playlists - num_playlists_output) / all_playlists * 100))

# reshape data frame (rows: playlists, columns: clusters)
playlist_cluster = pd.concat([activities_matches, moods_matches, df_cluster[['id', 'cluster']]]).drop_duplicates()
playlist_cluster['values'] = 1
df_pivot = playlist_cluster.pivot(index='id', columns='cluster', values='values').fillna(0)

# export results
print("export data")
df_pivot.to_csv("../../gen/data-preparation/output/playlist_clusters.csv")


# ------------------------------- #
#       CLUSTER STATISTICS		  #
# ------------------------------- #

def calculate_cluster_indices(df_pivot):
    return {column: df_pivot.index[(df_pivot[column ] == 1)].tolist() for column in df_pivot.columns}


def cluster_stats(df_pivot, playlists):
    # collect playlist ids for each label
    cluster_indices = calculate_cluster_indices(df_pivot)

    # total number of followers of playlists included in final sample
    total_market_size = playlists.loc[playlists.id.isin(df_pivot.index), 'followers'].sum()

    # calculate number of followers and market share for each cluster
    cluster_stats = pd.DataFrame()
    for keys, values in cluster_indices.items():
        cluster_temp = pd.DataFrame({'label':keys, 
                                'num_playlists':len(values), 
                                'market_share': playlists.loc[playlists.id.isin(cluster_indices[keys]), 'followers'].sum() / total_market_size * 100}, 
                               index=[0])
        cluster_stats = pd.concat([cluster_temp, cluster_stats])
    
    cluster_stats['perc_playlists'] = cluster_stats['num_playlists'] / len(df_pivot) * 100
    print(cluster_stats.sort_values('perc_playlists', ascending=False).reset_index(drop=True))
    return cluster_stats


def label_pairs(df_pivot, absolute=True):
    cluster_indices = calculate_cluster_indices(df_pivot)
    
    if absolute:  # cells are absolute playlist counts
        matrix = [df_pivot.loc[df_pivot.index.isin(cluster_indices[label])].sum(axis=0) for label in df_pivot.columns]

    else:  # normalized (cells are playlist counts relative to diagonal)
        matrix = [df_pivot.loc[df_pivot.index.isin(cluster_indices[label])].sum(axis=0) / 
                  df_pivot.loc[df_pivot.index.isin(cluster_indices[label])].sum(axis=0)[label]
                  for label in df_pivot.columns]

    return pd.DataFrame(matrix).set_index(df_pivot.columns)

print('export cluster stats')
cluster_stats(df_pivot, playlists).to_csv("../../gen/data-preparation/output/cluster_stats.csv")

print('export label pairs')
label_pairs(df_pivot, True).to_csv("../../gen/data-preparation/output/label_pairs_abs.csv")
label_pairs(df_pivot, False).to_csv("../../gen/data-preparation/output/label_pairs_norm.csv")



