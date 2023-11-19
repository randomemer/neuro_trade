.PHONY: venv scraper

venv:
	source ./venv/bin/activate

scraper:
	python3 ./src/scraper/main.py