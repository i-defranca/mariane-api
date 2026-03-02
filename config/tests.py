import logging
from unittest.mock import patch as p

from django.apps import apps
from django.db import connection
from pytest import mark

from config.logs import DailyFileHandler


@mark.django_db
def test_cursor_wrappers(monkeypatch):
    calls = []

    class FakeLogger:
        def __init__(self, name):
            assert name == 'query'

        def debug(self, **kwargs):
            calls.append(kwargs)

    monkeypatch.setattr('config.apps.Logger', FakeLogger)

    config = apps.get_app_config('config')
    config.ready()

    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        cursor.executemany('SELECT %s', [(1,), (2,), (3,)])

    assert len(calls) == 2
    assert calls[0]['sql'] == 'SELECT 1'
    assert calls[1]['sql'] == 'SELECT %s'


def test_daily_log_file_handler(tmp_path):
    hand = DailyFileHandler(tmp_path, 'test_')
    file = hand._build_filename()

    logger = logging.getLogger('test')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers = [hand]

    date = '2026-01-01'
    with p.object(hand, '_today', return_value=date):
        logger.info(f'test-{date}')

    assert file.exists()
    assert f'test-{date}' in file.read_text()
