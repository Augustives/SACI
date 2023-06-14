# SACI - Scraper of Algorithms and Complexitys


## Config
* Please create your python virtual env and install the requirements by running:
  ```make requirements```

## Commands
* Run all scrapers:
  ```make run_scraper```

* Run a specific scraper in a specific URL:
  ```make scraper_url url=<url> scraper=<scraper>```

* Run the results analysis of a specific URL:
  ```make results_analysis scraper=<scraper>```

* Make the results boilerplate for manual filling:
  ```manual_results_boilerplate scraper=<scraper>```