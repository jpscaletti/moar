.PHONY: clean clean-pyc test upload

all: clear clean-pyc test

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf tests/__pycache__
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-pyc:
	rm -rf tests/__pycache__
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	python runtests.py

upload:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf tests/__pycache__
	cd docs; clay build; cd ..
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name ".DS_Store" -exec rm -rf {} \;
	python setup.py sdist upload
