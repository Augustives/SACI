from logging import getLogger, Formatter, StreamHandler, Filter, DEBUG
from scraper.logger.settings import LOG_FORMAT


class AddScraperName(Filter):
    def filter(self, record):
        if not hasattr(record, 'scraper'):
            record.scraper = 'teste derive scraper'
        return True


def build_log(logger_name):
    log_handler = StreamHandler()
    log_handler.setLevel(DEBUG)
    log_handler.setFormatter(Formatter(LOG_FORMAT))

    log = getLogger(logger_name)
    log.addFilter(AddScraperName())
    log.addHandler(log_handler)
    return log


scraper_log = build_log('scraper_log')
