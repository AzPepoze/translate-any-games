# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
# Run with: uv run skills/image-text/overlay.py config.json
"""Clean regions of game images and draw translated text into them, from a JSON config."""

import json
import logging
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

EXIT_OK = 0
EXIT_CONFIG_ERROR = 1
EXIT_TEXT_NO_FIT = 2
DEFAULT_MIN_SIZE = 8
OPAQUE = 255

LOG = logging.getLogger("image-text")


class ConfigError(Exception):
    """A bad config value or a missing file. Exit code 1."""


class FitError(Exception):
    """Text does not fit its box at any allowed size. Exit code 2."""


def load_config(path):
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ConfigError(f"cannot read config {path}: {error}") from error
    if not isinstance(config.get("images"), list):
        raise ConfigError(f"{path}: config needs an 'images' list")
    return config


def require(item, key, label):
    if key not in item:
        raise ConfigError(f"{label}: missing '{key}'")
    return item[key]


def parse_color(value, label):
    digits = value.lstrip("#")
    if len(digits) not in (6, 8):
        raise ConfigError(f"{label}: colour '{value}' must be #rrggbb or #rrggbbaa")
    try:
        channels = tuple(int(digits[i : i + 2], 16) for i in range(0, len(digits), 2))
    except ValueError as error:
        raise ConfigError(f"{label}: colour '{value}' is not hex") from error
    if len(channels) == 3:
        return channels + (OPAQUE,)
    return channels


def parse_box(value, image_size, label):
    if not isinstance(value, list) or len(value) != 4:
        raise ConfigError(f"{label}: box must be [x, y, w, h]")
    x, y, width, height = value
    if width <= 0 or height <= 0:
        raise ConfigError(f"{label}: box width and height must be above 0")
    if x < 0 or y < 0 or x + width > image_size[0] or y + height > image_size[1]:
        raise ConfigError(f"{label}: box {value} is outside the image {image_size}")
    return x, y, width, height


def resolve_file(base, value, label):
    path = (base / value).resolve()
    if not path.is_file():
        raise ConfigError(f"{label}: file not found: {path}")
    return path


def open_image(path):
    try:
        return Image.open(path).convert("RGBA")
    except OSError as error:
        raise ConfigError(f"cannot open image {path}: {error}") from error


def fill_box(image, box, color):
    x, y, width, height = box
    image.paste(color, (x, y, x + width, y + height))


def edge_color(image, box):
    x, y, width, height = box
    left, top, right, bottom = x - 1, y - 1, x + width, y + height
    border = []
    for px in range(left, right + 1):
        border.extend(sample(image, px, top))
        border.extend(sample(image, px, bottom))
    for py in range(top + 1, bottom):
        border.extend(sample(image, left, py))
        border.extend(sample(image, right, py))
    if not border:
        raise ConfigError("edge clean: no pixels around the box")
    return tuple(int(statistics.median(channel)) for channel in zip(*border))


def sample(image, x, y):
    if 0 <= x < image.width and 0 <= y < image.height:
        return [image.getpixel((x, y))]
    return []


def clean_region(image, item, label):
    mode = require(item, "mode", label)
    box = parse_box(require(item, "box", label), image.size, label)
    if mode == "transparent":
        fill_box(image, box, (0, 0, 0, 0))
    elif mode == "fill":
        fill_box(image, box, parse_color(require(item, "color", label), label))
    elif mode == "edge":
        fill_box(image, box, edge_color(image, box))
    else:
        raise ConfigError(f"{label}: unknown clean mode '{mode}'")


def load_font(font_path, size, label):
    if font_path is None:
        return ImageFont.load_default(size=size)
    try:
        return ImageFont.truetype(str(font_path), size)
    except OSError as error:
        raise ConfigError(f"{label}: cannot load font {font_path}: {error}") from error


def text_width(font, text):
    return font.getlength(text)


def line_height(font):
    ascent, descent = font.getmetrics()
    return ascent + descent


def wrap_words(text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split():
            candidate = f"{current} {word}" if current else word
            if not current or text_width(font, candidate) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def layout_lines(text, font, max_width, stack):
    if stack:
        return [char for char in text if not char.isspace()]
    return wrap_words(text, font, max_width)


def block_fits(lines, font, max_width, max_height):
    if any(text_width(font, line) > max_width for line in lines):
        return False
    return len(lines) * line_height(font) <= max_height


def fit_text(item, inner_size, font_path, label):
    stroke = item.get("outline_width", 0)
    max_width = inner_size[0]
    max_height = inner_size[1]
    stack = item.get("stack", False)
    min_size = item.get("min_size", DEFAULT_MIN_SIZE)
    for size in range(item["size"], min_size - 1, -1):
        font = load_font(font_path, size, label)
        lines = layout_lines(item["text"], font, max_width, stack)
        if block_fits(lines, font, max_width, max_height):
            return font, lines
    raise FitError(f"{label}: text does not fit its box, even at size {min_size}")


def line_x(align, box_width, line_width):
    if align == "center":
        return (box_width - line_width) / 2
    if align == "right":
        return box_width - line_width
    return 0


def draw_lines(layer, lines, font, item, fill):
    stroke = item.get("outline_width", 0)
    outline = item.get("outline")
    align = item.get("align", "left")
    draw = ImageDraw.Draw(layer)
    step = line_height(font)
    top = (layer.height - len(lines) * step) / 2
    for index, line in enumerate(lines):
        x = line_x(align, layer.width, text_width(font, line))
        y = top + index * step
        draw.text(
            (x, y),
            line,
            font=font,
            fill=fill,
            stroke_width=stroke,
            stroke_fill=outline,
        )


def glow_layer(size, lines, font, item):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    glow = parse_color(item["glow"], "glow")
    draw_lines(layer, lines, font, item, glow)
    return layer.filter(ImageFilter.GaussianBlur(item.get("glow_radius", 4)))


def text_layer(size, lines, font, item):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    if "glow" in item:
        layer.alpha_composite(glow_layer(size, lines, font, item))
    fill = parse_color(item.get("fill", "#ffffff"), "fill")
    draw_lines(layer, lines, font, item, fill)
    angle = item.get("rotate", 0)
    if angle:
        layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    return layer


def composite_at(base, layer, x, y):
    left = max(0, -x)
    top = max(0, -y)
    right = min(layer.width, base.width - x)
    bottom = min(layer.height, base.height - y)
    if right <= left or bottom <= top:
        return
    visible = layer.crop((left, top, right, bottom))
    base.alpha_composite(visible, (x + left, y + top))


def draw_item(image, item, font_path, label):
    box = parse_box(require(item, "box", label), image.size, label)
    x, y, width, height = box
    stroke = item.get("outline_width", 0)
    inner = (width - 2 * stroke, height - 2 * stroke)
    font, lines = fit_text(item, inner, font_path, label)
    layer = text_layer((width, height), lines, font, item)
    center_x = x + width / 2 - layer.width / 2
    center_y = y + height / 2 - layer.height / 2
    composite_at(image, layer, round(center_x), round(center_y))


def text_label(source, index, item):
    snippet = str(item.get("text", ""))[:20]
    return f'{source.name}, text item {index} ("{snippet}")'


def render_image(entry, base):
    source_value = require(entry, "source", "image entry")
    output_value = require(entry, "output", "image entry")
    source = resolve_file(base, source_value, f"image '{source_value}'")
    output = (base / output_value).resolve()
    image = open_image(source)
    for clean in entry.get("clean", []):
        clean_region(image, clean, f"{source.name}, clean item")
    for index, item in enumerate(entry.get("text", []), start=1):
        label = text_label(source, index, item)
        font_path = None
        if "font" in item:
            font_path = resolve_file(base, item["font"], label)
        draw_item(image, item, font_path, label)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG")
    LOG.info("wrote %s", output)


def main(argv):
    if len(argv) != 2:
        LOG.error("usage: overlay.py config.json")
        return EXIT_CONFIG_ERROR
    config_path = Path(argv[1]).resolve()
    try:
        config = load_config(config_path)
        for entry in config["images"]:
            render_image(entry, config_path.parent)
    except ConfigError as error:
        LOG.error("%s", error)
        return EXIT_CONFIG_ERROR
    except FitError as error:
        LOG.error("%s", error)
        return EXIT_TEXT_NO_FIT
    LOG.info("done: %d image(s)", len(config["images"]))
    return EXIT_OK


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stderr)
    sys.exit(main(sys.argv))
