import base64
import io
import re
import sublime
from typing import ByteString, List
from .Globals import global_get, global_set
from .libs import png
from .settings import get_image_color
from .utils import simple_decorator


def get_colored_image_base64_by_color(img_name: str, rgba_code: str) -> str:
    """
    @brief Get the colored image in base64 string by RGBA color code.

    @param img_name  The image name
    @param rgba_code The color code in #RRGGBBAA

    @return The image base64 string
    """

    cache_key = "{name};{color}".format(name=img_name, color=rgba_code)

    if not rgba_code:
        return global_get("images.%s.base64" % img_name)

    cached = "images.@cache.%s" % cache_key

    if global_get(cached, None) is None:
        img_bytes = global_get("images.%s.bytes" % img_name)
        img_bytes = change_png_bytes_color(img_bytes, rgba_code)
        img_base64 = base64.b64encode(img_bytes).decode()

        global_set(cached, img_base64)

    return global_get(cached)


def get_colored_image_base64_by_region(img_name: str, region: sublime.Region) -> str:
    """
    @brief Get the colored image in base64 string by region.

    @param img_name The image name
    @param region   The region

    @return The image base64 string
    """

    return get_colored_image_base64_by_color(img_name, get_image_color(img_name, region))


def change_png_bytes_color(img_bytes: ByteString, rgba_code: str) -> ByteString:
    """
    @brief Change all colors in the PNG bytes to the new color.

    @param img_bytes The PNG image bytes
    @param rgba_code The color code in the form of #RRGGBBAA

    @return Color-changed PNG image bytes.
    """

    if not rgba_code:
        return img_bytes

    if not re.match(r"#[0-9a-fA-F]{8}$", rgba_code):
        raise ValueError("Invalid RGBA color code: " + rgba_code)

    def render_pixel(
        rgba_src: List[int], rgba_dst: List[int], invert_gray: bool = False
    ) -> List[int]:
        gray = calculate_gray(rgba_src)
        if invert_gray:
            gray = 0xFF - gray

        # ">> 8" is an approximation for "/ 0xFF" in following calculations
        return [
            int(rgba_dst[0] * gray) >> 8,
            int(rgba_dst[1] * gray) >> 8,
            int(rgba_dst[2] * gray) >> 8,
            int(rgba_dst[3] * rgba_src[3]) >> 8,
        ]

    invert_gray = not is_img_light(img_bytes)  # invert for dark image to get a solid looking
    rgba_dst = [int(rgba_code[i : i + 2], 16) for i in range(1, 9, 2)]
    w, h, rows_src, img_info = png.Reader(bytes=img_bytes).asRGBA()

    rows_dst = []
    for row_src in rows_src:
        row_dst = []
        for i in range(0, len(row_src), 4):
            row_dst.extend(render_pixel(row_src[i : i + 4], rgba_dst, invert_gray))
        rows_dst.append(row_dst)

    buf = io.BytesIO()
    png.from_array(rows_dst, "RGBA").write(buf)

    return buf.getvalue()


def calculate_gray(rgb: List[int]) -> int:
    """
    @brief Calculate the gray scale of a color.
    @see   https://atlaboratary.blogspot.com/2013/08/rgb-g-rey-l-gray-r0.html

    @param rgb The rgb color in list form

    @return The gray scale.
    """

    return int(rgb[0] * 38 + rgb[1] * 75 + rgb[2] * 15) >> 7


def is_img_light(img_bytes: ByteString) -> bool:
    """
    @brief Determine if image is light colored.

    @param img_bytes The image bytes

    @return True if image is light, False otherwise.
    """

    w, h, rows, img_info = png.Reader(bytes=img_bytes).asRGBA()

    gray_sum = 0
    for row in rows:
        for i in range(0, len(row), 4):
            gray_sum += calculate_gray(row[i : i + 4])

    return (gray_sum << 1) > 0xFF * w * h


def add_alpha_to_rgb(color_code: str) -> str:
    """
    @brief Add the alpha part to a valid RGB color code (#RGB, #RRGGBB, #RRGGBBAA)

    @param color_code The color code

    @return The color code in the form of #RRGGBBAA
    """

    if not color_code:
        return ""

    rgb = color_code[1:9]  # strip "#" and possible extra chars

    # RGB to RRGGBB
    if len(rgb) == 3:
        rgb = rgb[0] * 2 + rgb[1] * 2 + rgb[2] * 2

    return "#" + (rgb + "ff")[:8].lower()


@simple_decorator(add_alpha_to_rgb)
def color_code_to_rgba(color_code: str, region: sublime.Region = sublime.Region(0, 0)) -> str:
    """
    @brief Convert user settings color code into #RRGGBBAA form

    @param color_code The color code string from user settings
    @param region     The scope-related region

    @return The color code in the form of #RRGGBBAA
    """

    if not color_code:
        return ""

    view = sublime.active_window().active_view()

    # "color_code" is a scope?
    if not color_code.startswith("#"):
        if view and global_get("HAS_API_VIEW_STYLE_FOR_SCOPE"):
            # "color" is guaranteed to be #RRGGBB or #RRGGBBAA
            color = view.style_for_scope(view.scope_name(region.end() - 1)).get("foreground", "")

            if color_code == "@scope":
                return color

            if color_code == "@scope_inverted":
                # strip "#" and make color into RRGGBBAA int
                rgba_int = int((color + "ff")[1:9], 16)
                # invert RRGGBB, remain AA, strip "0x" prefix from hex and prepend 0s until 8 chars
                return "#" + hex((~rgba_int & 0xFFFFFF00) | (rgba_int & 0xFF))[2:].zfill(8)

        return ""

    # now color code must starts with "#"
    rgb = color_code[1:9]  # strip "#" and possible extra chars

    # RGB, RRGGBB, RRGGBBAA are legal
    if len(rgb) in [3, 6, 8] and re.match(r"[0-9a-fA-F]+$", rgb):
        return "#" + rgb

    return ""
