install:
	python setup.py install

install-dev:
	pip install -qr requirements.development.txt

check:
	pyflakes ./
	pep8 --repeat --show-source ./

.PHONY: check install install-dev
