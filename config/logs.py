import datetime
import logging
import pathlib

import structlog as struct
from structlog import contextvars, processors
from structlog.stdlib import BoundLogger, LoggerFactory, ProcessorFormatter


def Logger(name=None):
    return struct.get_logger(name)


class DailyFileHandler(logging.FileHandler):
    def __init__(self, log_dir, prefix=''):
        self.log_dir = pathlib.Path(log_dir)
        self.prefix = prefix
        self.date = self._today()
        super().__init__(self._build_filename(), encoding='utf-8')

    def _today(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def _build_filename(self):
        return self.log_dir / f'{self.prefix}{self.date}.log'

    def emit(self, record):
        today = self._today()
        if today != self.date:
            self.date = today
            self.stream.close()
            self.filename = str(self._build_filename())
            self.stream = self._open()
        super().emit(record)


def setup_structlog(DIR, LOG_LEVEL):
    LOG_DIR = DIR / 'logs'
    LOG_DIR.mkdir(exist_ok=True)

    struct.configure(
        processors=[
            contextvars.merge_contextvars,
            processors.add_log_level,
            processors.TimeStamper(fmt='iso'),
            processors.StackInfoRenderer(),
            processors.format_exc_info,
            ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=LoggerFactory(),
        wrapper_class=BoundLogger,
        cache_logger_on_first_use=True,
    )

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'structlog': {
                '()': ProcessorFormatter,
                'processor': processors.JSONRenderer(),
                'foreign_pre_chain': [
                    processors.TimeStamper(fmt='iso'),
                    processors.add_log_level,
                    processors.StackInfoRenderer(),
                    processors.format_exc_info,
                ],
            },
        },
        'handlers': {
            'app_file': {
                'level': LOG_LEVEL,
                'class': 'config.logs.DailyFileHandler',
                'formatter': 'structlog',
                'log_dir': LOG_DIR,
                'prefix': '',
            },
            'query_file': {
                'level': 'DEBUG',
                'class': 'config.logs.DailyFileHandler',
                'formatter': 'structlog',
                'log_dir': LOG_DIR,
                'prefix': 'query_',
            },
        },
        'root': {
            'handlers': ['app_file'],
            'level': LOG_LEVEL,
        },
        'loggers': {
            'query': {
                'handlers': ['query_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
