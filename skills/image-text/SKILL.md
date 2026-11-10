---
name: image-text
description: use when putting translated text into a game image using a per-game JSON config
---

# Image text

Use `overlay.py` to change text inside a game image. You write one JSON config per game. The script cleans old text out of the image and draws the new text in.

> [!NOTE]
> The script has no game data. Each game gets its own config file, kept in that game's project.

## Run

```bash
uv run skills/image-text/overlay.py /path/to/project/images.json
```

- `uv` reads the script's dependencies (Pillow) on its own. You do not need a venv.

To run the tests:

```bash
uv run --with pytest --with pillow pytest skills/image-text
```
- Paths in the config are relative to the config file's folder.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | All images written |
| 1 | Config or file error. The message names the problem. |
| 2 | Text does not fit its box, even at the smallest size |

## Config format

```json
{
  "images": [
    {
      "source": "original/title.png",
      "output": "../assets/images/title_EN.png",
      "clean": [
        { "mode": "transparent", "box": [10, 20, 80, 30] }
      ],
      "text": [
        {
          "text": "Start",
          "box": [10, 20, 80, 30],
          "font": "fonts/Example.ttf",
          "size": 24,
          "min_size": 12,
          "fill": "#ffffff",
          "outline": "#000000",
          "outline_width": 2,
          "glow": "#00e5ff",
          "glow_radius": 4,
          "align": "center",
          "rotate": 0,
          "stack": false
        }
      ]
    }
  ]
}
```

### Image entry

| Key | Required | Meaning |
|---|---|---|
| `source` | yes | Original image. Keep it in `original/`. |
| `output` | yes | Where the new PNG goes. The folder is created if missing. |
| `clean` | no | List of regions to clear before drawing. |
| `text` | no | List of text items to draw. |

### Clean item

| Key | Required | Meaning |
|---|---|---|
| `mode` | yes | `transparent`, `fill` or `edge` (see below) |
| `box` | yes | `[x, y, w, h]` in pixels |
| `color` | for `fill` | Hex colour, `#rrggbb` or `#rrggbbaa` |

| Mode | Result inside the box |
|---|---|
| `transparent` | Alpha set to 0 |
| `fill` | Filled with `color` |
| `edge` | Filled with the median colour of the 1-pixel border around the box |

### Text item

| Key | Default | Meaning |
|---|---|---|
| `text` | required | Text to draw. Use `\n` for a forced line break. |
| `box` | required | `[x, y, w, h]`. The text is drawn inside it. |
| `font` | Pillow default | Path to a `.ttf` or `.otf` file |
| `size` | required | Starting font size |
| `min_size` | 8 | Smallest size the script tries before it fails |
| `fill` | `#ffffff` | Text colour |
| `outline` | none | Outline colour |
| `outline_width` | 0 | Outline thickness in pixels |
| `glow` | none | Colour of a soft glow under the text |
| `glow_radius` | 4 | Blur radius of the glow |
| `align` | `left` | `left`, `center` or `right` |
| `rotate` | 0 | Degrees. Applied to the text only. |
| `stack` | false | `true` draws one character per line, top to bottom |

> [!TIP]
> Text that does not fit shrinks one size at a time until `min_size`. If it still does not fit, the script exits with code 2. Shorten the translation or enlarge the box.

## Checks the script makes

- The source image exists.
- Each font file exists.
- Each box is inside the image.
- Each colour is valid hex.

## Output

- PNG, RGBA.
- Same width and height as the source.
- Text is centred vertically in its box.
