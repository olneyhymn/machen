all: deploy

.PHONY: deploy
deploy:
	STATIC_DEPS=true pip3 install -U twitter git+https://github.com/tdhopper/NoDB.git -t .
	rm -rf concurrent/futures
	serverless deploy

.PHONY: clean
clean:
	git clean -fd
