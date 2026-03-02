import logging
from unittest.mock import patch as p

from config.logs import DailyFileHandler


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
