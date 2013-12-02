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
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

test:
	py.test --cov-config .coveragerc --cov moar tests/

publish: clean
	python setup.py sdist upload

publish-doc:
	cd doc && clay build
	cp -R doc/build/* doc/gh-pages/
	rm -rf doc/build
	cd doc/gh-pages && \
	git add --all . && \
	git commit -am "Update documentation" && \
	git push origin gh-pages
