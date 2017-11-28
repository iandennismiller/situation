# situation (c) Ian Dennis Miller

SHELL=/bin/bash
MOD_NAME=situation
TEST_CMD=SETTINGS=$$PWD/etc/testing.conf nosetests -w $(MOD_NAME)
#  --with-coverage --cover-package=$(MOD_NAME)

install:
	python setup.py install

requirements:
	pip install -r requirements.txt

develop:
	pip install -r .requirements-dev.txt

clean:
	rm -rf build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete

docs:
	rm -rf build/sphinx
	sphinx-build -b html docs build/sphinx

watch:
	watchmedo shell-command -R -p "*.py" -c 'date; $(TEST_CMD) -c etc/tests-single.cfg; date' .

test:
	$(TEST_CMD) -c etc/tests.cfg

single:
	$(TEST_CMD) -c etc/tests-single.cfg

tox:
	tox

release:
	# 1. create ~/.pypirc
	# 2. python setup.py register # notify pypi of new package
	python setup.py sdist upload

coverage:
	SETTINGS=$$PWD/etc/testing.conf nosetests -c etc/tests.cfg --with-xcoverage \
		--cover-package=$(MOD_NAME) --cover-tests

# create a homebrew install script
homebrew:
	bin/poet-homebrew.sh
	cp /tmp/situation.rb etc/situation.rb

.PHONY: clean install test watch docs release tox develop homebrew coverage
