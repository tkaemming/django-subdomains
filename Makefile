install:
	python setup.py install

install-dev:
	pip install -qr requirements.development.txt

check:
	pyflakes ./
	pep8 --repeat --show-source ./

test:
	python tests/manage.py test --verbosity=2

.PHONY: check install install-dev test
