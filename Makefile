include ../api-secrets/gpxmerge.env
export $(shell sed 's/=.*//' ../api-secrets/gpxmerge.env)

TRACES_DIR = traces

all: data

data:
	@mkdir -p $(TRACES_DIR)

	@echo "*" > $(TRACES_DIR)/.gitignore
	@echo "!.gitignore" >> $(TRACES_DIR)/.gitignore

	@gdown --folder https://drive.google.com/drive/folders/$(GPX_FOLDER_ID) -O $(TRACES_DIR)

.PHONY: data
