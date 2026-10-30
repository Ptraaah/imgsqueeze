#!/usr/bin/env python3
"""
imgsqueeze - batch-compress images for the web without the tears.

Point it at a folder and it resizes, converts, and re-encodes every image into
a web-ready output folder, printing how much weight you saved. Built on Pillow.

    python3 imgsqueeze.py ./raw-photos
    python3 imgsqueeze.py ./raw --out ./web --max-width 1600 --format webp --quality 80
    python3 imgsqueeze.py ./raw --format jpeg   # keep jpeg, just squeeze

Defaults: max width 1920, convert to WebP at quality 82, never upscale,
preserve folder structure, skip files already smaller than the result.

By ptraaa - MIT License
"""
import argparse, os, sys

try:
    from PIL import Image, ImageOps
except ImportError:
    print("imgsqueeze needs Pillow:  pip install Pillow", file=sys.stderr)
    sys.exit(2)

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".gif"}
FMT_EXT = {"webp": ".webp", "jpeg": ".jpg", "png": ".png"}


def squeeze(src, dst, max_width, fmt, quality):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.width > max_width:
            h = round(im.height * max_width / im.width)
            im = im.resize((max_width, h), Image.LANCZOS)
        if fmt == "webp":
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if "transparency" in im.info else "RGB")
            im.save(dst, "WEBP", quality=quality, method=6)
        elif fmt == "jpeg":
            im.convert("RGB").save(dst, "JPEG", quality=quality, optimize=True)
        else:
            im.save(dst, "PNG", optimize=True)
    return os.path.getsize(dst)


def main():
    ap = argparse.ArgumentParser(description="Batch image compressor for the web")
    ap.add_argument("folder", help="folder with source images")
    ap.add_argument("--out", default=None, help="output folder (default: <folder>-web)")
    ap.add_argument("--max-width", type=int, default=1920)
    ap.add_argument("--format", choices=["webp", "jpeg", "png"], default="webp")
    ap.add_argument("--quality", type=int, default=82)
    args = ap.parse_args()

    out_root = args.out or (args.folder.rstrip("/") + "-web")
    total_in = total_out = done = skipped = 0
    for base, _dirs, files in os.walk(args.folder):
        for f in files:
            if os.path.splitext(f)[1].lower() not in EXTS:
                continue
            src = os.path.join(base, f)
            rel = os.path.relpath(src, args.folder)
            dst = os.path.join(out_root, os.path.splitext(rel)[0] + FMT_EXT[args.format])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            size_in = os.path.getsize(src)
            try:
                size_out = squeeze(src, dst, args.max_width, args.format, args.quality)
            except Exception as e:
                print(f"SKIP  {rel}: {e}")
                skipped += 1
                continue
            total_in += size_in
            if size_out >= size_in and os.path.abspath(src) != os.path.abspath(dst):
                os.remove(dst)  # squeezing made it bigger: keep the original instead
                print(f"KEPT  {rel} (original already smaller)")
                total_out += size_in
                skipped += 1
                continue
            total_out += size_out
            done += 1
            print(f"OK    {rel}: {size_in//1024} KB -> {size_out//1024} KB")
    if total_in:
        saved = 100 * (1 - total_out / total_in)
        print(f"\nimgsqueeze: {done} converted, {skipped} kept/skipped, "
              f"{total_in//1024} KB -> {total_out//1024} KB ({saved:.0f}% saved) in {out_root}")
    else:
        print("no images found")


if __name__ == "__main__":
    main()
