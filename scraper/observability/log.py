from logging import DEBUG, Filter, Formatter, StreamHandler, getLogger

from scraper.observability.settings import LOG_FORMAT


class AddScraperName(Filter):
    def filter(self, record):
        if not hasattr(record, 'scraper'):
            record.scraper = record.pathname.split('\\')[-2]
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
