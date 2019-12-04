all: deploy

.PHONY: deploy
deploy:
	STATIC_DEPS=true pip3 install -U twitter requests nodb -t .
	pip3 uninstall futures
	pip3 uninstall concurrent
	serverless deploy

.PHONY: clean
clean:
	git clean -fd
