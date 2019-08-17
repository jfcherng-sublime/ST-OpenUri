import sublime


class Globals(object):
    """
    @brief This class stores application-level global variables.
    """

    HAS_API_VIEW_STYLE_FOR_SCOPE = int(sublime.version()) >= 3170

    uri_regex_obj = None

    # fmt: off
    image_phantom = {
        "base64": "",
        "bytes": b"",
        "ext": "",
        "mime": "",
        "path": "",
        "ratio_wh": 0,
        "size": (0, 0),  # w, h
    }
    # fmt: on

    # fmt: off
    image_popup = {
        "base64": "",
        "bytes": b"",
        "ext": "",
        "mime": "",
        "path": "",
        "ratio_wh": 0,
        "size": (0, 0),  # w, h
    }
    # fmt: on

    # cached base64 string for colored images
    colored_image_base64 = {
        # "{img_name}@{rgba_color_code}": base64 encoded image resource,
    }
