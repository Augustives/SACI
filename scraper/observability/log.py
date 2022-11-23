import platform

from logging import DEBUG, Filter, Formatter, StreamHandler, getLogger

from scraper.observability.settings import (SCRAPER_LOG_FORMAT,
                                            SESSION_LOG_FORMAT)


class AddScraperName(Filter):
    def filter(self, record):
        if not hasattr(record, 'scraper'):
            split_char = '\\' if 'Windows' in platform.platform() else '/'
            record.scraper = record.pathname.split(split_char)[-2]
        return True


def build_scraper_log(logger_name):
    log_handler = StreamHandler()
    log_handler.setLevel(DEBUG)
    log_handler.setFormatter(Formatter(SCRAPER_LOG_FORMAT))

    log = getLogger(logger_name)
    log.addFilter(AddScraperName())
    log.addHandler(log_handler)
    return log


def build_session_log(logger_name):
    log_handler = StreamHandler()
    log_handler.setLevel(DEBUG)
    log_handler.setFormatter(Formatter(SESSION_LOG_FORMAT))

    log = getLogger(logger_name)
    log.addHandler(log_handler)
    return log


scraper_log = build_scraper_log('scraper_log')
session_log = build_session_log('session_log')
