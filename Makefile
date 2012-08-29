.PHONY: clean clean-pyc test upload doc

all: clean clean-pyc test

clean: clean-pyc
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf tests/res/t
	find . -name '.DS_Store' -exec rm -f {} \;

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

test:
	rm -rf tests/res/t
	python runtests.py tests
	rm -rf tests/__pycache__

upload: clean
	python setup.py sdist upload

doc:
	cd doc; rm -rf build; clay build
	cd _pages; git checkout gh-pages; cp -r ../doc/build/html/* .;  git add .; git commit -m "Update doc"; git push origin gh-pages
	git add doc _pages; git commit -m "Update doc"; git push origin master
