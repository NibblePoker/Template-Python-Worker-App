#!/usr/local/bin/python

# Imports
import os
import signal
import sys
import time

from nibblepoker.config import Config
import nibblepoker.exit_codes as exit_codes
from nibblepoker.logger import get_logger, print_header, print_separator, print_footer
from nibblepoker.worker import Worker

from my_app.workers.example import create_example_worker


# Globals
is_end_signal_raised = False
end_signal_to_use: int = -1


# Application's code
# > Loading the config file
config = Config("../config.json")

# > Preparing the config and logger
logger = get_logger("main", config.get_config("logging_level_main", 20))

# > Printing the logs header
print_header(logger, "My App")

# > Changing the CWD to app.py's location.
# !> Mainly done for Docker since I couldn't be bothered to write a bash script for it.
logger.info("Correcting CWD...")
try:
    logger.debug("* Original: '{}'".format(os.getcwd()))
    logger.debug("* Final: '{}'".format(os.path.dirname(os.path.realpath(__file__))))
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
except Exception as err:
    logger.error("Failed to change the current working directory !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_CWD_FAILURE)

# > Preparing workers.
logger.info("Preparing workers...")
workers: list[Worker] = list()
workers.append(create_example_worker(
    config=config,
    name_suffix="demo",
    sleep_count=5,
    sleep_length_ms=750,
))


# > Preparing and registering the signal handler
def sigint_term_handler(sig, frame):
    logger.info('SIGINT or SIGTERM received !')
    logger.debug('Setting the global kill-switch and waiting for main loop !')
    global is_end_signal_raised
    is_end_signal_raised = True
    global end_signal_to_use
    end_signal_to_use = sig


logger.info("Registering SIG handlers...")
signal.signal(signal.SIGINT, sigint_term_handler)
signal.signal(signal.SIGTERM, sigint_term_handler)

# > Starting workers
logger.info("Starting workers...")
print_separator(logger)
for worker in workers:
    worker.run()

# > Main loop
logger.info("Entering main loop...")
while True:
    # Checking if any thread is running.
    are_workers_dead = False

    for worker in workers:
        if not worker.is_running():
            are_workers_dead = True

    if are_workers_dead:
        logger.debug("Found some non-running threads, preparing the exit variables...")
        is_end_signal_raised = True
        end_signal_to_use = signal.SIGINT

    # Waiting a bit to avoid wasting CPU cycles.
    time.sleep(1)

    # Checking if the application should exit.
    if is_end_signal_raised:
        logger.info("Exiting main loop...")

        for worker in workers:
            worker.end_signal_to_process = end_signal_to_use

        # Waiting for the threads do die.
        for worker in workers:
            while worker.is_running():
                time.sleep(0.1)

        break


# > Printing the logs footer
print_footer(logger)

# > Exiting properly
sys.exit(exit_codes.NO_ERROR)
