import logging

LOG_FORMAT = "[%(name)s][%(levelname)s] %(message)s"
LOG_LEVEL_DEFAULT = "INFO"


def init_plugin_logger() -> logging.Logger:
    """
    @brief Initiate a plugin logger.

    @return The initiated plugin logger.
    """

    from .settings import get_package_name

    def set_logger_hander(logger: logging.Logger) -> None:
        # remove all existing log handlers
        for handler in logger.handlers:
            logger.removeHandler(handler)

        logging_handler = logging.StreamHandler()
        logging_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(logging_handler)

    logging.addLevelName(101, "NOTHING")
    logger = logging.getLogger(get_package_name())
    logger.propagate = False  # prevent appear multiple same log messages
    set_logger_hander(logger)

    return logger


def apply_user_log_level(logger: logging.Logger) -> None:
    """
    @brief Apply user-set "log_level" to the logger.

    @param logger The logger
    """

    from .settings import get_setting

    log_level = get_setting("log_level")

    if not isinstance(logging.getLevelName(log_level), int):
        logger.warning(
            'Unknown "log_level": {log_level} (assumed "{default}")'.format(
                log_level=log_level, default=LOG_LEVEL_DEFAULT
            )
        )
        log_level = LOG_LEVEL_DEFAULT

    # temporary set to INFO level for logging log_level changed
    logger.setLevel("INFO")
    logger.info("Set log level: {}".format(log_level))
    logger.setLevel(log_level)


def msg(message: str) -> str:
    """
    @brief Generate plugin message.

    @param message The message

    @return The plugin message.
    """

    from .settings import get_package_name

    return "[{plugin}] {message}".format(plugin=get_package_name(), message=message)


def print_msg(message: str, show_message: bool = True) -> None:
    """
    @brief Print plugin message to ST's console.

    @param message      The message
    @param show_message Whether to print the message
    """

    if show_message:
        print(msg(message))
