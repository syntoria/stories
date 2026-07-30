"""Generate the site's icon set from the Syntoria brand mark.

Source is assets/logo-mark-white.png from the Syntoria Design System — the
rising-sun mark in white with transparency. The mark is not centred in its own
canvas, so it is re-cropped to its opaque bounds and re-centred here before
being placed on the brand navy tile.

    python3 make_favicon.py

Writes favicon.ico, favicon-16/32/48.png, apple-touch-icon.png, and
icon-192/512.png at the repository root.
"""

from PIL import Image, ImageDraw

SOURCE = "brand/logo-mark-white.png"
NAVY = (0x0A, 0x25, 0x40, 255)  # --navy-800, the brand's primary dark ground

# Share of the tile the mark occupies, at normal sizes. The mark is a dense set
# of concentric arcs; much above this and it crowds the corners.
MARK_SCALE = 0.72

# At 16px the arcs land on single pixels and merge into a blob. Filling more of
# the tile, and dropping the rounding that eats the corner pixels, is what keeps
# the three rings and the dome distinguishable. Optical correction at small
# sizes is normal icon practice; nobody sees 16 and 32 side by side.
SMALL_SIZE = 16
SMALL_MARK_SCALE = 0.92

# Corner radius as a share of tile width.
CORNER_RADIUS = 0.18


def build_tile(size, rounded=True):
    """Return the mark centred on a navy tile at the given pixel size."""
    scale = SMALL_MARK_SCALE if size <= SMALL_SIZE else MARK_SCALE
    rounded = rounded and size > SMALL_SIZE

    tile = Image.new("RGBA", (size, size), NAVY)

    if rounded:
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [(0, 0), (size - 1, size - 1)],
            radius=int(size * CORNER_RADIUS),
            fill=255,
        )
        tile.putalpha(mask)

    mark = Image.open(SOURCE).convert("RGBA")
    mark = mark.crop(mark.split()[3].getbbox())  # trim to the mark itself

    target = int(size * scale)
    mark.thumbnail((target, target), Image.LANCZOS)

    tile.alpha_composite(
        mark,
        ((size - mark.width) // 2, (size - mark.height) // 2),
    )
    return tile


def main():
    # Browser tab icons.
    for size in (16, 32, 48):
        build_tile(size).save(f"favicon-{size}.png")

    # Multi-resolution .ico for older browsers and Windows.
    build_tile(48).save(
        "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)]
    )

    # iOS home screen. Square: iOS applies its own corner mask, so rounding
    # here would show up as a double-rounded edge.
    build_tile(180, rounded=False).convert("RGB").save("apple-touch-icon.png")

    # Android home screen / PWA.
    for size in (192, 512):
        build_tile(size).save(f"icon-{size}.png")

    print("wrote favicon.ico, favicon-16/32/48.png, apple-touch-icon.png, icon-192/512.png")


if __name__ == "__main__":
    main()
