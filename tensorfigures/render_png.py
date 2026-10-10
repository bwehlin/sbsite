"""Render every SVG in figures/ to a 3x-resolution PNG with a transparent background.

Uses headless Chrome or Chromium. Set CHROME=/path/to/chrome if it isn't found.
The SVGs use CSS colour-mix(), so render with a current browser, not an SVG library.
"""
import os, re, glob, shutil, subprocess, tempfile, pathlib

CANDIDATES = [os.environ.get("CHROME"), "google-chrome", "chromium", "chromium-browser", "chrome",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
chrome = next((c for c in CANDIDATES if c and (shutil.which(c) or os.path.exists(c))), None)
if not chrome:
    raise SystemExit("Chrome/Chromium not found; set CHROME=/path/to/chrome")

for svg in sorted(glob.glob("figures/*.svg")):
    text = open(svg).read()
    w = int(float(re.search(r'width="([\d.]+)"', text).group(1)))
    h = int(float(re.search(r'height="([\d.]+)"', text).group(1)))
    uri = pathlib.Path(svg).resolve().as_uri()
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(f"<html style='color-scheme:light'><body style='margin:0;background:transparent'>"
                f"<img src='{uri}' style='width:{w}px;display:block'></body></html>")
        page = f.name
    png = svg[:-4] + ".png"
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--default-background-color=00000000",
                    "--force-device-scale-factor=3", f"--window-size={w},{h}",
                    f"--screenshot={os.path.abspath(png)}", pathlib.Path(page).as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(page)
    print("wrote", png)
