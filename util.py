import logging
import sys

set_of_logs = set()
consoleHandler = logging.StreamHandler()
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s")
consoleHandler.setFormatter(logFormatter)

def get_logging(name: str, level):
    log = logging.getLogger(name)

    if (name in set_of_logs) is False:
        set_of_logs.add(name)
        log.addHandler(consoleHandler)
        log.setLevel(level)
        log.propagate = False
    return log

