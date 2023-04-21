PYTHON :=
	ifeq ($(OS),Windows_NT)
		PYTHON = venv/Scripts/python
		PIP = venv/Scripts/pip
	else
		PYTHON = venv/bin/python3
		PIP = venv/bin/pip
	endif

requirements: requirements.txt
	$(PIP) install -r requirements.txt

run_scraper:
	$(PYTHON) -m main

scrape_url:
	$(PYTHON) -m scraper.scripts --script=scrape_url --url=$(url) --scraper=$(scraper)

results_analysis:
	$(PYTHON) -m scraper.scripts --script=results_analysis --scraper=$(scraper)

manual_results_boilerplate:
	$(PYTHON) -m scraper.scripts --script=manual_results_boilerplate


.PHONY: run_scraper