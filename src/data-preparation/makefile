# Makefile
# requires GNUMake32
# Installation instructions: http://tilburgsciencehub.com/setup

DATA_DIR = ../../data
TEMP_DIR = ../../gen/data-preparation/temp
OUTPUT_DIR = ../../gen/data-preparation/output
OUTPUT_FIGURES = ../../gen/figures

###############
# BUILD RULES #
###############

all: figures

figures: $(OUTPUT_FIGURES)/genre_k_mode.png

associationrules: $(OUTPUT_DIR)/playlist_clusters.csv

prep: $(TEMP_DIR)/unzipping.log

######################
# DOWNLOAD AND UNZIP #
######################

$(DATA_DIR)/data.zip: download.py
	python download.py
	
$(TEMP_DIR)/unzipping.log $(TEMP_DIR)/tags-playlists.csv $(TEMP_DIR)/tags-playlists-meta.csv $(TEMP_DIR)/playlists.csv: unzip.py $(DATA_DIR)/data.zip
	python unzip.py

########################
# CLUSTERING PROCEDURE #
########################

$(OUTPUT_DIR)/playlist_clusters.csv $(OUTPUT_DIR)/label_pairs_abs.csv $(OUTPUT_DIR)/label_pairs_norm.csv: $(TEMP_DIR)/tags-playlists.csv $(TEMP_DIR)/tags-playlists-meta.csv $(TEMP_DIR)/playlists.csv 
	python playlists_association_rules.py

$(OUTPUT_FIGURES)/genre_k_mode.png: $(OUTPUT_DIR)/playlist_clusters.csv
	python cluster.py



