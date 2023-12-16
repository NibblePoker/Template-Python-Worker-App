import time

from nibblepoker.config import Config
from nibblepoker.logger import get_logger
from nibblepoker.worker import Worker


class ExampleWorker(Worker):
    sleep_length_ms: int
    sleep_count: int

    def __init__(self, config, name, entry_point, sleep_length_ms: int, sleep_count: int):
        super().__init__(config, name, entry_point)

        # Logger setup
        self.logger_thread = get_logger(name, config.get_config("logging_level_thread_example", 20))

        # Attributes assignment
        self.sleep_length_ms = sleep_length_ms
        self.sleep_count = sleep_count


def create_example_worker(config: Config, name_suffix: str = "", sleep_length_ms: int = 1500,
                          sleep_count: int = 5) -> ExampleWorker:
    return ExampleWorker(
        config=config,
        name=("example-worker-"+name_suffix).rstrip("-"),
        entry_point=__thread_example_worker,
        sleep_length_ms=sleep_length_ms,
        sleep_count=sleep_count,
    )


def __thread_example_worker(worker: ExampleWorker, **args):
    worker.logger_thread.debug("Started thread !")

    while worker.end_signal_to_process == -1:
        # Preventing CPU hogging
        time.sleep(0.01)

        # Doing our task
        if worker.sleep_count > 0:
            worker.logger_thread.debug("Mimimimimimimi...")
            time.sleep(worker.sleep_length_ms / 1000)
            worker.sleep_count -= 1
        else:
            worker.logger_thread.debug("Time to wake up !")
            break

    worker.logger_thread.debug(f"Closing thread ! => {worker.last_return_code}")
