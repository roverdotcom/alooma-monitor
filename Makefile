PKG_NAME = roverdotcom/alooma-monitor:latest
cur-dir := $(shell pwd)

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

docker:
	touch local.config
	docker build $(DOCKER_BUILD_OPTS) -t $(PKG_NAME) .

# Build the docker container, install the package, and open a shell inside it for testing
docker-shell: docker
	docker run --rm --env-file local.config -it $(DOCKER_RUN_OPTS) $(PKG_NAME) /bin/sh

docker-test: docker
	docker run --rm $(DOCKER_RUN_OPTS) $(PKG_NAME) nosetests

docker-run: docker
	docker run --rm --env-file local.config -it $(DOCKER_RUN_OPTS) $(PKG_NAME)

docker-push: docker
	docker push $(PKG_NAME)

.DEFAULT_GOAL := docker-test
