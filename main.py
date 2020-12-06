import logging
from task_manager import TaskManager


def main():
    logging.debug("Starting project focus")
    TaskManager.start()


if __name__ == "__main__":
    main()
