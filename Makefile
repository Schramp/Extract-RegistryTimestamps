PLUGINS_DIR=/hansken/distribution/extraction-plugins
IMAGE_NAME=extraction-plugin-examples-registry-filetime

.DEFAULT_GOAL := default

.PHONY: clean
clean: ## clean all build artifacts
	@rm -rf .tox
	@rm -rf .runner
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -f tests.log

.PHONY: install
install: ## build and test python package
	@tox -e py38
	@tox install

.PHONY: docker
docker: ## build plugin docker image
	@docker build -t $(IMAGE_NAME) -f Dockerfile "."
	@docker save "$(IMAGE_NAME):latest" -o "dist/$(IMAGE_NAME).tgz"

.PHONY: integration-test
integration-test:
	@tox -e integration

.PHONY: deploy
deploy: ## deploy plugin to hansken minikube
	@make docker
	@make integration-test
	@minikube ssh "mkdir -p $(PLUGINS_DIR)"
	@scp -q -i "$$(minikube ssh-key)" dist/*.tgz "docker@$$(minikube ip):$(PLUGINS_DIR)"
	@minikube ssh "docker load < $(PLUGINS_DIR)/*.tgz"

.PHONY: default
default:
	@make clean install docker integration-test
