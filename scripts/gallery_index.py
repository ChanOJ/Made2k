#!/usr/bin/env python3
"""Write site/gallery/index.html: a plain listing of the gallery files.

The original gallery was a bare directory listing, which bunny.net does not serve.
Run it after any change of site/gallery/, then run scripts/seo.py (deterministic).

Usage: python3 -I scripts/gallery_index.py
"""
from html import escape
from pathlib import Path
from urllib.parse import quote

GALLERY = Path(__file__).resolve().parent.parent / "site" / "gallery"
SKIP = {"index.html", ".picasa.ini", ".DS_Store"}


def listing(folder):
    rel = folder.relative_to(GALLERY).as_posix()
    items = []
    for p in sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        if p.name in SKIP:
            continue
        url = quote(p.name) + ("/" if p.is_dir() else "")
        items.append((p.is_dir(), url, p.name + ("/" if p.is_dir() else "")))
    return rel, items


def page(folder):
    rel, items = listing(folder)
    title = "gallery" + ("/" + rel if rel != "." else "")
    up = '<A href="../">../</A><BR>\n' if rel != "." else '<A href="../files/">&lt; back to files</A><BR>\n'
    rows = "".join('<A href="%s">%s</A><BR>\n' % (u, escape(n)) for _, u, n in items)
    return (
        '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n'
        "<title>måde's home [%s]</title>\n</head>\n"
        '<BODY bgcolor="#DFF4F6" text="#696A6A" link="#696A6A" vlink="#696A6A" alink="#696A6A">\n'
        '<font size="3" face="Verdana, Arial, Helvetica, sans-serif">\n<B>%s</B><BR><BR>\n%s%s</font>\n</body>\n</html>\n'
        % (escape(title), escape(title), up, rows)
    )


def main():
    for folder in [GALLERY] + sorted(p for p in GALLERY.rglob("*") if p.is_dir()):
        (folder / "index.html").write_bytes(page(folder).encode("utf-8"))


if __name__ == "__main__":
    main()
