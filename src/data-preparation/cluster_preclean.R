library(data.table)

dir.create('../../gen/data-preparation/output')

tags <- fread('../../gen/data-preparation/temp/tags-playlists.csv')
tags[, source:='tagwords']

meta <- fread('../../gen/data-preparation/temp/tags-playlists-meta.csv')

# Load playlist meta data
playlists <- fread('../../gen/data-preparation/temp/playlists.csv')
playlists[, follower_rank:=frankv(followers,na.last=T,order=-1L)]


moods <- c('mood', 'fuzzy', 'feel', 'rage', 'anger', 'annoyance', 'angry', 'annoying', 'aggresive', 'vigilance', 'anticipitation', 'anticipating', 'interest', 'interesting', 'optimism', 'optimistic', 'ecstasy', 'joy', 'serenity', 'love', 'admiration', 'trust', 'acceptance', 'accepting', 'submission', 'terror', 'fear', 'apprehension', 'awe', 'amazement', 'amaze', 'amazing', 'surprise', 'surprising', 'distraction', 'distracting', 'disapproval', 'disaproving', 'disaprove', 'grief', 'sadness', 'sad', 'pensiveness', 'pensive', 'remorse', 'loathing', 'loath', 'disgust', 'boredom', 'boring', 'bored', 'contempt', 'chill', 'active', 'cheerful', 'reflective', 'gloomy', 'humorous', 'humor', 'melancholy', 'idyllic', 'romantic', 'mysterious', 'ominous', 'calm', 'lighthearted', 'hope', 'hopeful', 'fearful', 'tense', 'lonely', 'alone', 'happy', 'good', 'bad', 'suave', 'vibe', 'breakup', 'depressed', 'depression', 'emo', 'bored', 'heart broken')
activities <- c('sing', 'drive', 'dance', 'work', 'study', 'concentrate', 'read', 'workout', 'gym', 'party', 'sport', 'relax', 'cook', 'unwind', 'driving', 'roadtrip', 'vacation', 'flying', 'fly', 'sleep', 'travel', 'road', 'trip', 'training', 'train', 'eat', 'kitchen', 'run', 'dream', 'activity', 'active', 'ride', 'dancing', 'listen', 'discover', 'wake', 'up', 'wakeup', 'shower', 'riding', 'start', 'drink', 'jogging', 'jog', 'bbq', 'gaming', 'game', 'office', 'cycling', 'camping', 'fishing', 'hunting', 'fish', 'hunt', 'karaoke', 'poker', 'playing', 'cards')

tmp <- lapply(moods, function(x) data.table(tag_name=x, id=playlists[grepl(paste0(x,'$|',x,'[ ]'), name, ignore.case=T)]$id))
mood_tags <- rbindlist(tmp,fill=T)[, type:='mood']

tmp <- lapply(activities, function(x) data.table(tag_name=x, id=playlists[grepl(paste0(x,'$|',x,'[ ]'), name, ignore.case=T)]$id))
activity_tags <- rbindlist(tmp,fill=T)[, type:='activity']

setkey(meta, tagid)
setkey(tags, tagid)
tags[meta, tag_name:=i.tag]

tags[, type:='tags']

new_tags = rbindlist(list(tags[, c('id','followers','tag_name','type')],mood_tags,activity_tags),fill=T)

setkey(new_tags,id)
setkey(playlists, id)
new_tags[playlists, ':=' (followers=i.followers, followerrank=i.follower_rank)]

# clean tag names
library(stringr)
new_tags[, tag_name2:=gsub('[ ]','', str_squish((str_replace_all(tag_name, regex("\\W+"), " "))))]


# group low-popularity keywords together - not needed for final implementation, but done here to speed it up
new_tags[, tagid_new:=.GRP,by=c('type','tag_name2')]

# compute input for similarity computations (playlist X tag occurence)
new_tags[, value:=1]
#tags[, value:= log(tagimportance+1)]

plXtags = dcast(new_tags, id~type+tagid_new, fun.aggregate=function(x) 1, fill = 0, value.var='value')

fwrite(plXtags, '../../gen/data-preparation/temp/playlist-tags.csv')

Sys.time()
