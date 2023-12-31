# Imports
import logging
import threading
from typing import Callable, Optional

from .config import Config
from .logger import get_logger


# Classes
class Worker:
    """
    Generic worker class used to represent any Worker when its specific role is not relevant.

    :param name: Name of the worker used in logging.
    :param entry_point: Method that is run as a new thread by the worker.
    """

    name: str
    """
    Worker's name used as-is in logging related tasks.
    """

    entry_point: Optional[Callable]
    """
    Method that is run as a new thread by the worker.
    
    This method should have the following signature:\n
    `my_thread(worker: Worker, **args)`
    """

    thread: Optional[threading.Thread]
    """
    Worker's thread when ran.
    """

    lock: threading.Lock
    """
    Generic Lock object used to potentially synchronise tasks between the main and worker's threads.
    
    **Unused by default.**
    """

    logger_worker: logging.Logger
    """
    Logger for the Worker object.
    """

    logger_thread: Optional[logging.Logger]
    """
    Logger for the worker's thread.
    
    It must be instantiated by the worker's thread when ran for the first time.
    """

    last_return_code: int
    """
    Return code grabbed from the worker's thread or from the application it ran.
    """

    end_signal_to_process: int
    """
    Value set by the main thread to indicate that the thread should stop as soon as possible.
    
    It should be ignored if set to `-1`.
    """

    config: Config
    """
    Common shared config passed to the constructor.
    """


    def __init__(self, config: Config, name: str = "error.name.not.set", entry_point: Optional[Callable] = None):
        """
        :param name: Name of the worker used in logging.
        :param entry_point: Method that is run as a new thread by the worker.
        """
        
        # Preliminary checks
        if type(name) is not str:
            raise TypeError("The 'name' variable is not a String !")
        if (not callable(entry_point)) and (entry_point is not None):
            raise TypeError("The 'entry_point' variable is neither a Callable or None !")
        
        # Attributes assignment
        self.name = name
        self.entry_point = entry_point
        self.thread = None
        self.lock = threading.Lock()
        self.logger_worker = get_logger(name, config.get_config("logging_level_worker", 20))
        self.logger_thread = None
        self.last_return_code = 0
        self.end_signal_to_process = -1
        self.config = config
        
        # Final checks
        if entry_point is None:
            self.logger_worker.warning("The 'entry_point' attribute is None !")
    
    def run(self, **args) -> bool:
        """
        Starts a thread for the current worker if none are currently running and if 'entry_point' is callable.
        :param args: Arguments that need to be passed to the new thread.
        :return: True or False depending on whether the thread was started.
        """
        self.logger_worker.debug("Checking to prepare the Thread launch...")
        
        if self.thread is not None:
            if self.is_running():
                self.logger_worker.warning("A thread is already running on this worker !")
                return False
            else:
                self.logger_worker.debug("A thread has finished running, quickly cleaning up some stuff !")
                self.thread._target = None
                self.thread = None
        
        if self.entry_point is None:
            self.logger_worker.error("Unable to call the entrypoint method ! (None attribute)")
            return False
        
        if not callable(self.entry_point):
            self.logger_worker.error("Unable to call the entrypoint method ! (Not callable)")
            return False
        
        self.logger_worker.debug("Starting thread...")
        self.thread = threading.Thread(target=self.entry_point, args=(self, *args))
        self.thread.start()
        return True
    
    def is_running(self) -> bool:
        """
        Checks if the worker currently has its thread running.

        :return: True or False depending on whether the worker is currently running a thread.
        """
        if self.thread is not None:
            return self.thread.is_alive()
        return False
