all: deploy

.PHONY: deploy
deploy:
	STATIC_DEPS=true pip3 install -U twitter git+https://github.com/Miserlou/NoDB.git@4616921 -t .
	rm -rf concurrent/futures
	serverless deploy

.PHONY: clean
clean:
	git clean -fd
