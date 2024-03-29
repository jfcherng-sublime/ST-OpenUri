from __future__ import annotations

import logging

from .shared import global_get

LOG_FORMAT = "[%(name)s][%(levelname)s] %(message)s"
LOG_LEVEL_DEFAULT = "INFO"


def init_plugin_logger() -> logging.Logger:
    """
    @brief Initiate a plugin logger.

    @return The initiated plugin logger.
    """
    from .constants import PLUGIN_NAME

    def set_logger_hander(logger: logging.Logger) -> None:
        # remove all existing log handlers
        for handler in logger.handlers:
            logger.removeHandler(handler)

        logging_handler = logging.StreamHandler()
        logging_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(logging_handler)

    logging.addLevelName(5, "DEBUG_LOW")
    logging.addLevelName(1001, "NOTHING")
    logger = logging.getLogger(PLUGIN_NAME)
    logger.propagate = False  # prevent appear multiple same log messages
    set_logger_hander(logger)

    return logger


def apply_user_log_level(logger: logging.Logger) -> None:
    """
    @brief Apply user-set "log_level" to the logger.

    @param logger The logger
    """
    from .settings import get_setting

    log_level = get_setting("log_level").upper()

    if not isinstance(logging.getLevelName(log_level), int):
        logger.warning(f'Unknown "log_level": {log_level} (assumed "{LOG_LEVEL_DEFAULT}")')
        log_level = LOG_LEVEL_DEFAULT

    # temporary set to INFO level for logging log_level changed
    logger.setLevel("INFO")
    logger.info(f"Set log level: {log_level}")
    logger.setLevel(log_level)


def log(level: str, msg: str) -> None:
    """
    @brief A shorhand for logging message with the global logger.

    @param level The log level
    @param msg   The message
    """
    level_upper = level.upper()
    level_int = logging.getLevelName(level_upper)

    if not isinstance(level_int, int):
        raise ValueError(f'Unknown log level "{level}" whose message is: {msg}')

    global_get("logger").log(level_int, msg)


def msg(msg: str) -> str:
    """
    @brief Generate plugin message.

    @param msg The message

    @return The plugin message.
    """
    from .constants import PLUGIN_NAME

    return f"[{PLUGIN_NAME}] {msg}"
