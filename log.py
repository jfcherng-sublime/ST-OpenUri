def msg(message: str) -> str:
    """
    @brief Generate plugin message.

    @param message The message

    @return The plugin message.
    """

    from .settings import get_package_name

    return "[{plugin}] {message}".format(plugin=get_package_name(), message=message)
