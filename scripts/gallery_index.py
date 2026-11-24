#!/usr/bin/env python3
"""Write site/gallery/index.html: directory listings of the gallery, in the style of the original Apache server's `Index of /gallery`.

The original gallery was a bare directory listing, which bunny.net does not serve.
Run it after any change of site/gallery/, then run scripts/seo.py (deterministic).

Usage: python3 -I scripts/gallery_index.py
"""
from html import escape
from pathlib import Path
from urllib.parse import quote

GALLERY = Path(__file__).resolve().parent.parent / "site" / "gallery"
SKIP = {"index.html", ".picasa.ini", ".DS_Store"}


def size(p):
    if p.is_dir():
        return "-"
    n = p.stat().st_size
    return "%dK" % max(1, round(n / 1024)) if n < 1024 * 1024 else "%.1fM" % (n / 1024 / 1024)


def page(folder):
    """Classic Apache 1.3 "Index of /dir" page (name and size columns, no icons or dates)."""
    rel = folder.relative_to(GALLERY).as_posix()
    path = "/gallery" + ("" if rel == "." else "/" + rel)
    entries = [p for p in sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())) if p.name not in SKIP]
    width = max([len(p.name) + (1 if p.is_dir() else 0) for p in entries] + [16]) + 1
    rows = ""
    for p in entries:
        name = p.name + ("/" if p.is_dir() else "")
        link = '<A HREF="%s">%s</A>' % (quote(p.name) + ("/" if p.is_dir() else ""), escape(name))
        rows += "%s%s%6s\n" % (link, " " * (width - len(name)), size(p))
    head = "Name" + " " * (width - 4) + "  Size\n"
    return (
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<HTML>\n<HEAD>\n'
        '<META CHARSET="utf-8">\n<TITLE>Index of %s</TITLE>\n</HEAD><BODY>\n<H1>Index of %s</H1>\n<PRE>\n'
        '%s<HR>\n<A HREF="../">Parent Directory</A>\n%s<HR>\n</PRE>\n</BODY></HTML>\n'
        % (escape(path), escape(path), head, rows)
    )


def main():
    for folder in [GALLERY] + sorted(p for p in GALLERY.rglob("*") if p.is_dir()):
        (folder / "index.html").write_bytes(page(folder).encode("utf-8"))


if __name__ == "__main__":
    main()
