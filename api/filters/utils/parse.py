from datetime import date, timedelta

from rest_framework.exceptions import ParseError


def month(value):
    try:
        y, m = map(int, value.split('-'))

        first = date(y, m, 1)

        next_y = y if m < 12 else y + 1
        next_m = m + 1 if m < 12 else 1

        last = date(next_y, next_m, 1) - timedelta(days=1)

        return first, last
    except ValueError as exc:
        raise ParseError({'month': ['Invalid format [yyyy-mm]']}) from exc
