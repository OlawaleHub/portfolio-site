"""Regenerate the abstract SVG artwork used by the site.

Writes 2:1 thumbnails to assets/img/work/ and 4:1 banners to
assets/img/banners/. The CSS applies grayscale and multiply blending, so these
read as editorial texture rather than as decoration.

These are placeholders for real screenshots. To use a real image, drop a JPG or
PNG of the same aspect ratio into the folder and point the page's <img src> at
it — no other change is needed.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORK = ROOT / "assets" / "img" / "work"
BANNERS = ROOT / "assets" / "img" / "banners"

PAPER = "#f0f0f0"
INK = "#14130f"
ACCENT = {"green": "#3f6b46", "carmine": "#8f0a30", "ochre": "#7a5e02"}

# name -> (accent, secondary)
PALETTE = {
    "lagos-emergency": ("carmine", "green"),
    "ifeoluwa-medical": ("green", "ochre"),
    "token-gated-voting": ("ochre", "carmine"),
    "refcrypt-labs": ("ochre", "green"),
    "portfolio-builds": ("green", "ochre"),
    "mobile-flutter": ("carmine", "ochre"),
}


def art(width: int, height: int, a: str, b: str) -> str:
    """Abstract banner: grid, rule-lines, circles, squares and a top bar."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="4" cy="4" r="1.2" fill="{INK}" opacity="0.5"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="{PAPER}"/>
  <rect width="{width}" height="{height}" fill="url(#dots)"/>
  <circle cx="{int(width * 0.8)}" cy="70" r="{int(height * 0.48)}" fill="{a}" opacity="0.16"/>
  <circle cx="{int(width * 0.15)}" cy="{int(height * 0.85)}" r="{int(height * 0.55)}" fill="{b}" opacity="0.13"/>
  <path d="M0 {int(height * 0.8)} L{width} {int(height * 0.3)}" stroke="{a}" stroke-width="2" opacity="0.45"/>
  <path d="M0 {int(height * 0.9)} L{width} {int(height * 0.4)}" stroke="{b}" stroke-width="1" opacity="0.38"/>
  <path d="M{int(width * 0.56)} {height} L{int(width * 0.68)} 0" stroke="{a}" stroke-width="1" opacity="0.30"/>
  <path d="M{int(width * 0.74)} {height} L{int(width * 0.85)} 0" stroke="{b}" stroke-width="1" opacity="0.28"/>
  <rect x="{int(width * 0.84)}" y="{int(height * 0.6)}" width="{int(height * 0.38)}" height="{int(height * 0.38)}"
        fill="none" stroke="{INK}" stroke-width="1.5" opacity="0.4"/>
  <circle cx="{int(width * 0.075)}" cy="{int(height * 0.2)}" r="{int(height * 0.1)}"
          fill="none" stroke="{b}" stroke-width="1.5" opacity="0.55"/>
  <circle cx="{int(width * 0.075)}" cy="{int(height * 0.2)}" r="{int(height * 0.045)}" fill="{a}" opacity="0.32"/>
  <g stroke="{INK}" stroke-width="1" opacity="0.22">
    <line x1="{int(width * 0.25)}" y1="0" x2="{int(width * 0.25)}" y2="{height}"/>
    <line x1="{int(width * 0.5)}" y1="0" x2="{int(width * 0.5)}" y2="{height}"/>
    <line x1="{int(width * 0.75)}" y1="0" x2="{int(width * 0.75)}" y2="{height}"/>
  </g>
  <rect x="0" y="0" width="{width}" height="6" fill="{a}" opacity="0.85"/>
</svg>
"""


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    BANNERS.mkdir(parents=True, exist_ok=True)

    for name, (a, b) in PALETTE.items():
        thumb = WORK / f"{name}.svg"
        thumb.write_text(art(800, 400, ACCENT[a], ACCENT[b]), encoding="utf-8")
        print(f"thumb  {thumb.relative_to(ROOT)}  {thumb.stat().st_size} bytes")

        banner = BANNERS / f"{name}.svg"
        banner.write_text(art(1600, 400, ACCENT[a], ACCENT[b]), encoding="utf-8")
        print(f"banner {banner.relative_to(ROOT)}  {banner.stat().st_size} bytes")


if __name__ == "__main__":
    main()
