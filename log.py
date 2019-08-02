def msg(message: str) -> str:
    """
    @brief Generate plugin message.

    @param message The message

    @return The plugin message.
    """

    return "[{plugin}] {message}".format(plugin=__package__, message=message)
