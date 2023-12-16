# Standard exit codes
NO_ERROR = 0
""" Standard exit code returned when everything went well."""

# Custom exit codes
ERROR_CWD_FAILURE = 1000
""" Returned when the application failed to changed its current working directory. """

ERROR_CONFIG_ERROR = 1003
""" Returned when the application encountered an error when parsing the config file's content. """

ERROR_RUNNING_AS_ROOT = 1005
""" Returned when the application is running as 'root' when it shouldn't. """
