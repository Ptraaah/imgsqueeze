# imgsqueeze

Batch-compress images for the web without the tears. Point it at a folder and it resizes, converts, and re-encodes every image into a web-ready output folder, then tells you exactly how much weight you saved.

## Usage

```bash
pip install Pillow
python3 imgsqueeze.py ./raw-photos
python3 imgsqueeze.py ./raw --out ./web --max-width 1600 --format webp --quality 80
python3 imgsqueeze.py ./raw --format jpeg     # keep JPEG, just squeeze it
```

Real run:

```
OK    foto-besar.jpg: 173 KB -> 13 KB

imgsqueeze: 1 converted, 0 kept/skipped, 173 KB -> 13 KB (92% saved)
```

- Defaults are sane for the web: max width 1920, WebP at quality 82
- Never upscales, respects EXIF orientation, preserves folder structure
- If squeezing would make a file bigger, the original is kept and reported instead of silently bloating your site
- Handles JPG, PNG, WebP, BMP, TIFF, and GIF sources

## Indonesian summary

Kompres gambar massal untuk web: ubah ukuran, konversi ke WebP/JPEG/PNG, dan lihat total penghematannya. File yang hasil kompresnya malah lebih besar akan dipertahankan versi aslinya.

## License

MIT. By ptraaa.

## Support

If this project helped you, you can support its development on Trakteer: https://trakteer.id/adel_putra2

Kalau proyek ini membantu Anda, Anda bisa mendukung pengembangannya lewat Trakteer: https://trakteer.id/adel_putra2
