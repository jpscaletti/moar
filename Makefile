.PHONY: test

all: clean clean-pyc test

clean: clean-pyc
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf tests/__pycache__
	find tests/assets/t -name '*.png' -exec rm -f {} \;
	find tests/assets/t -name '*.jpeg' -exec rm -f {} \;
	find . -name '.DS_Store' -exec rm -f {} \;

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '*,cover' -delete

test:
	py.test -x tests/

testcov:
	py.test --cov-config .coveragerc --cov moar tests/

coverage:
	py.test --cov-config .coveragerc --cov-report html --cov moar tests/

publish: clean
	python setup.py sdist upload

