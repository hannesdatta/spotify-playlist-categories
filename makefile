all: data-preparation

.PHONY: data-preparation

data-preparation:
	$(MAKE) -C src/data-preparation
