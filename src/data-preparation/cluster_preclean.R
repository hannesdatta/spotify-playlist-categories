library(data.table)

dir.create('../../gen/data-preparation/output')

tags <- fread('../../gen/data-preparation/temp/tags-playlists.csv')

meta <- fread('../../gen/data-preparation/temp/tags-playlists-meta.csv')

# Load playlist meta data
playlists <- fread('../../gen/data-preparation/temp/playlists.csv')

# Create playlist types (mood/activity/genre)
playlists[, playlist_type_mood := 0]
playlists[grepl('mood|fuzzy|feel|rage|anger|annoyance|angry|annoying|aggresive|vigilance|anticipitation|anticipating|interest|interesting|optimism|optimistic|ecstasy|joy|serenity|love|admiration|trust|acceptance|accepting|submission|terror|fear|apprehension|awe|amazement|amaze|amazing|surprise|surprising|distraction|distracting|disapproval|disaproving|disaprove|grief|sadness|sad|pensiveness|pensive|remorse|loathing|loath|disgust|boredom|boring|bored|contempt|chill|active|cheerful|reflective|gloomy|humorous|humor|melancholy|idyllic|romantic|mysterious|ominous|calm|lighthearted|hope|hopeful|fearful|tense|lonely|alone|happy|good|bad|suave|vibe|breakup|depressed|depression|emo|bored|heart broken', name, ignore.case=T), playlist_type_mood:=1]

playlists[, playlist_type_activity := 0]
playlists[grepl('sing|drive|dance|work|study|concentrate|read|workout|gym|party|sport|relax|cook|unwind|driving|roadtrip|vacation|flying|fly|sleep|travel|road|trip|training|train|eat|kitchen|run|dream|activity|active|ride|dancing|listen|discover|wake|up|wakeup|shower|riding|start|drink|jogging|jog|bbq|gaming|game|office|cycling|camping|fishing|hunting|fish|hunt|karaoke|poker|playing|cards',name, ignore.case=T), playlist_type_activity := 1]

playlists[, playlist_type_genre:=0]
playlists[playlist_type_activity==0&playlist_type_mood==0, playlist_type_genre:=1]

playlists[, list(.N),by=c('playlist_type_activity', 'playlist_type_mood', 'playlist_type_genre')]

# Select only keywords that fall within the x percentile (kick out low-frequency keywords)
meta[, selected:=F]
meta[percentile<=.99, selected := T]

setkey(tags, tagid)
setkey(meta, tagid)
tags[meta, selected:=i.selected]

# group low-popularity keywords together - not needed for final implementation, but done here to speed it up
tags[, tagid_new:=tagid]
tags[selected==F, tagid_new:=999999]

nrow(meta)
nrow(meta[selected==T]) # reduce #tag words

# compute input for similarity computations (playlist X tag occurence)
tags[, value:=1]
#tags[, value:= log(tagimportance+1)]

# important: remove condition of only using it on 30k - use on entire set!
plXtags = dcast(tags[followerrank<=30000], id~tagid_new, fun.aggregate=function(x) 1, fill = 0, value.var='value')

fwrite(plXtags, '../../gen/data-preparation/temp/playlist-tags.csv')

Sys.time()
