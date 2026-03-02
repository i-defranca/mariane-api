from time import perf_counter

from django.apps import AppConfig
from django.db.backends.utils import CursorWrapper

from .logs import Logger


class CoreConfig(AppConfig):
    name = 'config'

    _initialized = False

    def ready(self):
        if CoreConfig._initialized:
            return

        CoreConfig._initialized = True

        def log(sql, params, start):
            Logger('query').debug(
                sql=sql,
                params=params,
                duration_ms=round((perf_counter() - start) * 1000, 2),
            )

        execute = CursorWrapper.execute

        def wrap_execute(self, sql, params=None):
            start = perf_counter()
            try:
                return execute(self, sql, params)
            finally:
                log(sql, params, start)

        CursorWrapper.execute = wrap_execute

        executemany = CursorWrapper.executemany

        def wrap_executemany(self, sql, param_list):
            start = perf_counter()
            try:
                return executemany(self, sql, param_list)
            finally:
                log(sql, param_list, start)

        CursorWrapper.executemany = wrap_executemany
