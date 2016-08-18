# Makefile for Orbital
all: build

build:
	cd src/laniakea && dub build --parallel --compiler=ldc2
	cd src/synchrotron && dub build --parallel --compiler=ldc2
	#cd frontend && dub build --parallel

test:
	#cd shared && dub test
	cd synchrotron && dub test
	#cd frontend && dub test

clean:
	rm -rf build/

	rm -f shared/dub.selections.json
	rm -f synchrotron/dub.selections.json
	rm -f frontend/dub.selections.json

	rm -rf shared/.dub
	rm -rf synchrotron/.dub
	rm -rf frontend/.dub

install:
	@echo "Implement me!"

.PHONY: build clean test install
