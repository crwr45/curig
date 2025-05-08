.PHONY: install test build clean

install:
	pip install -e .

test:
	python -m pytest test/

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
