default: test

# Build Docker image
build: docker_build output

# Build and push Docker image
release: docker_build docker_push output

# Image and binary can be overidden with env vars.
DOCKER_IMAGE ?= chalko/cable-modem-scraper
BINARY ?= cable-modem-scraper

# Get the latest commit.
GIT_COMMIT = $(strip $(shell git rev-parse --short HEAD))

# Get the version number from the code
CODE_VERSION = $(strip $(shell cat VERSION))

# Find out if the working directory is clean
GIT_NOT_CLEAN_CHECK = $(shell git status --porcelain)
ifneq (x$(GIT_NOT_CLEAN_CHECK), x)
DOCKER_TAG_SUFFIX = "-dirty"
endif

# If we're releasing to Docker Hub, and we're going to mark it with the latest tag, it should exactly match a version release
ifeq ($(MAKECMDGOALS),release)
# Use the version number as the release tag.
DOCKER_TAG = $(CODE_VERSION)

ifndef CODE_VERSION
$(error You need to create a VERSION file to build a release)
endif

# See what commit is tagged to match the version
VERSION_COMMIT = $(strip $(shell git rev-list $(CODE_VERSION) -n 1 | cut -c1-7))
ifneq ($(VERSION_COMMIT), $(GIT_COMMIT))
$(error echo You are trying to push a build based on commit $(GIT_COMMIT) but the tagged release version is $(VERSION_COMMIT))
endif

# Don't push to Docker Hub if this isn't a clean repo
ifneq (x$(GIT_NOT_CLEAN_CHECK), x)
$(error echo You are trying to release a build based on a dirty repo)
endif

else
# Add the commit ref for development builds. Mark as dirty if the working directory isn't clean
DOCKER_TAG = $(CODE_VERSION)-$(GIT_COMMIT)$(DOCKER_TAG_SUFFIX)
endif



docker_push:
	# Build Docker image
	docker buildx build \
	  --push \
	  --platform linux/arm/v7,linux/arm64/v8,linux/amd64 \
	  --label org.label-schema.build-date=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
	  --label org.label-schema.name="Cable Mode Scraper" \
	  --label org.label-schema.description="Scrapes the staus of a cable modem" \
	  --label org.label-schema.vcs-ref=$(GIT_COMMIT) \
	  --label org.label-schema.vcs-url="`git config --get remote.origin.url`" \
	  --label org.label-schema.vendor="e.g. ACME Inc" \
	  --label org.label-schema.version=$(CODE_VERSION) \
	  --label org.label-schema.schema-version="1.0" \
	  -t $(DOCKER_IMAGE):$(DOCKER_TAG) \
	  -t $(DOCKER_IMAGE):latest .

output:
	@echo Docker Image: $(DOCKER_IMAGE):$(DOCKER_TAG)
