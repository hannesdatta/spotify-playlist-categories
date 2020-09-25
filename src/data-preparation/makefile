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

figure: $(OUTPUT_FIGURES)/k_mode.png

cluster: $(OUTPUT_DIR)/playlist_clusters.csv

label_pairs_abs: $(OUTPUT_DIR)/label_pairs_abs.csv

label_pairs_norm: $(OUTPUT_DIR)/label_pairs_norm.csv

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

$(OUTPUT_DIR)/label_pairs_abs.csv: $(TEMP_DIR)/tags-playlists.csv $(TEMP_DIR)/tags-playlists-meta.csv $(TEMP_DIR)/playlists.csv 
	python playlists_association_rules.py

$(OUTPUT_DIR)/label_pairs_norm.csv: $(TEMP_DIR)/tags-playlists.csv $(TEMP_DIR)/tags-playlists-meta.csv $(TEMP_DIR)/playlists.csv 
	python playlists_association_rules.py

$(OUTPUT_FIGURES)/k_mode.png: $(OUTPUT_DIR)/playlist_clusters.csv
	python cluster.py



