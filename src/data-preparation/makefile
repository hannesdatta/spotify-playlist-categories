# Makefile
# requires GNUMake32
# Installation instructions: http://tilburgsciencehub.com/setup

DATA_DIR = ../../data
TEMP_DIR = ../../gen/data-preparation/temp
OUTPUT_DIR = ../../gen/data-preparation/output

###############
# BUILD RULES #
###############

cluster: $(OUTPUT_DIR)/cluster_output.csv

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

$(TEMP_DIR)/playlist-tags.csv: cluster_preclean.R $(TEMP_DIR)/unzipping.log
	R --vanilla --args "" < "cluster_preclean.R"

$(OUTPUT_DIR)/cluster_output.csv: cluster_kmeans.py $(TEMP_DIR)/playlist-tags.csv
	python cluster_kmeans.py
