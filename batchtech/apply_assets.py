"""Write the brand files over Open WebUI's icons and splash images.

    python3 batchtech/apply_assets.py                                  the built-in BatchTechUI files
    python3 batchtech/apply_assets.py --main-logo LOGO --model-logo ICON

--main-logo   your logo for the login page, splash screen, browser tab icon and home-screen icon.
--model-logo  the default picture for models and assistants (chat answers, model lists). It is static/favicon.png.
Each is a PNG/JPG/WebP file path or an https:// URL. Square images look best. Leave an option off to keep the
built-in file for it. The installer in the ElderThings repo asks for these and then calls this script before
building the image.
"""

import argparse, base64, io, shutil, sys, urllib.request
from pathlib import Path

root = Path(__file__).resolve().parent.parent
brand = root / 'batchtech/assets/brand'
out = root / 'static/static'


def load(src):
    from PIL import Image

    if src.startswith(('http://', 'https://')):
        req = urllib.request.Request(src, headers={'User-Agent': 'batchtechui-installer'})
        data = urllib.request.urlopen(req, timeout=30).read()
        img = Image.open(io.BytesIO(data))
    else:
        img = Image.open(Path(src).expanduser())
    return img.convert('RGBA')


def square(img, size):
    """Fit the image inside a transparent square without stretching it."""
    from PIL import Image

    img = img.copy()
    img.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    canvas.paste(img, ((size - img.width) // 2, (size - img.height) // 2), img)
    return canvas


def save(img, path, size):
    square(img, size).save(path, 'PNG')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--main-logo')
    ap.add_argument('--model-logo')
    a = ap.parse_args()

    # 1. the built-in set
    for f in sorted(brand.iterdir()):
        shutil.copyfile(f, out / f.name)
    shutil.copyfile(brand / 'favicon.png', root / 'static/favicon.png')

    # 2. your main logo replaces everything the browser and the login page show
    if a.main_logo:
        img = load(a.main_logo)
        save(img, out / 'logo.png', 512)
        save(img, out / 'splash.png', 512)
        save(img, out / 'splash-dark.png', 512)
        save(img, out / 'web-app-manifest-512x512.png', 512)
        save(img, out / 'web-app-manifest-192x192.png', 192)
        save(img, out / 'apple-touch-icon.png', 180)
        save(img, out / 'favicon-96x96.png', 96)
        square(img, 256).save(out / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        buf = io.BytesIO()
        square(img, 256).save(buf, 'PNG')
        b64 = base64.b64encode(buf.getvalue()).decode()
        (out / 'favicon.svg').write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 256 256">'
            f'<image width="256" height="256" xlink:href="data:image/png;base64,{b64}"/></svg>\n'
        )
        # the main logo is also the default model picture unless a model logo is given
        if not a.model_logo:
            save(img, out / 'favicon.png', 512)
            save(img, root / 'static/favicon.png', 512)

    # 3. your model logo: the picture a model shows when it has none of its own
    if a.model_logo:
        img = load(a.model_logo)
        save(img, out / 'favicon.png', 512)
        save(img, root / 'static/favicon.png', 512)

    print('assets written' + (' (custom main logo)' if a.main_logo else '') + (' (custom model logo)' if a.model_logo else ''))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:  # a bad path or URL should stop the build, not ship the wrong logo
        sys.exit(f'apply_assets: {e}')
