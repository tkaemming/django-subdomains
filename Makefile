install:
	python setup.py install

lint:
	pip install --use-mirrors flake8
	flake8 ./subdomains

test:
	python setup.py test

publish:
	git tag $$(python setup.py --version)
	git push --tags
	python setup.py sdist upload

.PHONY: install publish lint test
