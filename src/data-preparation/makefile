# Makefile
# requires GNUMake32
# Installation instructions: http://tilburgsciencehub.com/setup

DATA_DIR = ../../data
TEMP_DIR = ../../gen/data-preparation/temp
OUTPUT_DIR = ../../gen/data-preparation/output

###############
# BUILD RULES #
###############

cluster: $(OUTPUT_DIR)/playlist_clusters.csv

prepare: $(TEMP_DIR)/unzipping.log

######################
# DOWNLOAD AND UNZIP #
######################

$(DATA_DIR)/data.zip: download.py
	python download.py
	
$(TEMP_DIR)/unzipping.log: unzip.py $(DATA_DIR)/data.zip
	python unzip.py

########################
# CLUSTERING PROCEDURE #
########################

$(OUTPUT_DIR)/playlist_clusters.csv: $(TEMP_DIR)/tags-playlists.csv $(TEMP_DIR)/tags-playlists-meta.csv $(TEMP_DIR)/playlists.csv 
	python playlists_association_rules.py
