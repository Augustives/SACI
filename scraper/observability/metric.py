from enum import Enum


class Stages(Enum):
    TIME = 'time'
    SPACE = 'space'


class Metric:
    def __init__(self):
        self._hits = {
            'time': 0,
            'space': 0
        }
        self._total = 0

    def decorator(self, stage):
        def wrap(func):
            def inner(*args, **kwargs):
                result = func(*args, **kwargs)
                if result:
                    self._hits[stage] += 1
                    return result
            self._total += 1
            return inner
        return wrap

    def print_metric(self):
        metric = '------ METRICS ------\n'
        for key, value in self._hits.items():
            metric += (
                f'Missing {key} complexity:'
                f' {int(self._total - self._hits[key])}\n'
            )

        print(metric)
