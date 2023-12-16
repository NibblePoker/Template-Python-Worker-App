import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Creates a logger with the given attributes and a standard formatter format.

    :param name: Name of the logger.
    :param level: Logging level used by the logger.
    :return: The newly or previously created Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Simple check that prevents a logger from having more than one formatter when using the method.
    if len(logger.handlers) == 0:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter("[%(asctime)s] [%(name)s/%(levelname).3s]: %(message)s")
        formatter.datefmt = "%H:%M:%S"
        ch.setFormatter(formatter)
        ch.setStream(sys.stdout)
        logger.addHandler(ch)
    
    return logger


def print_separator(logger: logging.Logger) -> None:
    logger.info("\033[36m-\033[94m===========================\033[36m-\033[39m")


def print_header(logger: logging.Logger, app_name: str) -> None:
    logger.info("          \033[36m_   \033[94m__  \033[36m_\033[39m")
    logger.info("     \033[96m_  \033[36m_// \033[94m/\\\\ \\ \033[36m\\\\_  \033[96m_\033[39m")
    logger.info("   \033[96m_// \033[36m/ / \033[94m/ /_\\ \\ \033[36m\\ \\ \033[96m\\\\_\033[39m")
    logger.info("  \033[96m/ / \033[36m/ / \033[94m/ ___\\\\ \\ \033[36m\\ \\ \033[96m\\ \\\033[39m")
    logger.info(" \033[96m/_/ \033[36m/_/ \033[94m/_/     \033[94m\\_\\ \033[36m\\_\\ \033[96m\\_\\\033[39m")
    print_separator(logger)
    logger.info(f"\033[36m{' ' * max(0, int((29 - len(app_name)) / 2))}{app_name}\033[39m")
    print_separator(logger)


def print_footer(logger: logging.Logger) -> None:
    logger.info("Goodbye !")
    print_separator(logger)
    logger.info(" \033[96m\\_\\ \033[36m\\_\\             \033[36m/_/ \033[96m/_/\033[39m")
