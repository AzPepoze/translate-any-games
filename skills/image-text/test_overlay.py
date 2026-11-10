import json

from PIL import Image, ImageDraw

import overlay


def write_source(folder, image):
    path = folder / "source.png"
    image.save(path, format="PNG")
    return path


def write_config(folder, images):
    config = folder / "images.json"
    config.write_text(json.dumps({"images": images}), encoding="utf-8")
    return config


def solid(size, color):
    return Image.new("RGBA", size, color)


def run(config):
    return overlay.main(["overlay.py", str(config)])


def pixel(path, xy):
    with Image.open(path) as image:
        return image.convert("RGBA").getpixel(xy)


def test_missing_images_list_is_config_error(tmp_path):
    config = tmp_path / "images.json"
    config.write_text("{}", encoding="utf-8")

    assert run(config) == overlay.EXIT_CONFIG_ERROR


def test_box_outside_image_is_config_error(tmp_path):
    write_source(tmp_path, solid((20, 20), (255, 0, 0, 255)))
    config = write_config(tmp_path, [{
        "source": "source.png",
        "output": "out/result.png",
        "clean": [{"mode": "transparent", "box": [10, 10, 20, 20]}],
    }])

    assert run(config) == overlay.EXIT_CONFIG_ERROR
    assert not (tmp_path / "out" / "result.png").exists()


def test_bad_colour_is_config_error(tmp_path):
    write_source(tmp_path, solid((20, 20), (255, 0, 0, 255)))
    config = write_config(tmp_path, [{
        "source": "source.png",
        "output": "out/result.png",
        "clean": [{"mode": "fill", "box": [5, 5, 10, 10], "color": "#12345"}],
    }])

    assert run(config) == overlay.EXIT_CONFIG_ERROR


def test_text_that_cannot_fit_is_exit_2(tmp_path):
    write_source(tmp_path, solid((40, 30), (0, 0, 0, 0)))
    config = write_config(tmp_path, [{
        "source": "source.png",
        "output": "out/result.png",
        "text": [{"text": "Hello", "box": [0, 0, 5, 5], "size": 12}],
    }])

    assert run(config) == overlay.EXIT_TEXT_NO_FIT


def test_normal_run_keeps_source_size(tmp_path):
    write_source(tmp_path, solid((40, 30), (0, 0, 0, 0)))
    output = tmp_path / "out" / "result.png"
    config = write_config(tmp_path, [{
        "source": "source.png",
        "output": "out/result.png",
        "text": [{"text": "Hi", "box": [5, 5, 30, 20], "size": 12, "fill": "#ffffff"}],
    }])

    assert run(config) == overlay.EXIT_OK
    with Image.open(output) as image:
        assert image.size == (40, 30)
        assert image.mode == "RGBA"
        assert image.getextrema()[3][1] > 0


def test_transparent_clean_clears_alpha(tmp_path):
    write_source(tmp_path, solid((20, 20), (255, 0, 0, 255)))
    output = tmp_path / "out" / "result.png"
    config = write_config(tmp_path, [{
        "source": "source.png",
        "output": "out/result.png",
        "clean": [{"mode": "transparent", "box": [5, 5, 10, 10]}],
    }])

    assert run(config) == overlay.EXIT_OK
    assert pixel(output, (10, 10))[3] == 0
    assert pixel(output, (0, 0)) == (255, 0, 0, 255)


def test_fill_clean_uses_colour(tmp_path):
    write_source(tmp_path, solid((20, 20), (255, 0, 0, 255)))
    output = tmp_path / "out" / "result.png"
    config = write_config(tmp_path, [{
        "source": "source.png",
        "output": "out/result.png",
        "clean": [{"mode": "fill", "box": [5, 5, 10, 10], "color": "#00ff00"}],
    }])

    assert run(config) == overlay.EXIT_OK
    assert pixel(output, (10, 10)) == (0, 255, 0, 255)


def test_edge_clean_uses_border_colour(tmp_path):
    source = Image.new("RGBA", (20, 20), (0, 0, 255, 255))
    ImageDraw.Draw(source).rectangle((5, 5, 14, 14), fill=(0, 0, 0, 255))
    write_source(tmp_path, source)
    output = tmp_path / "out" / "result.png"
    config = write_config(tmp_path, [{
        "source": "source.png",
        "output": "out/result.png",
        "clean": [{"mode": "edge", "box": [5, 5, 10, 10]}],
    }])

    assert run(config) == overlay.EXIT_OK
    assert pixel(output, (10, 10)) == (0, 0, 255, 255)
