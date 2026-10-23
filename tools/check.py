"""Check that translated chunks keep the exact markup of the English source.

usage: python3 tools/check.py <lang> [chunk ...]
Compares the tag sequence (names + non-translatable attributes) of src/<lang>/NN.html against src/en/NN.html.
"""
import os, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_ATTRS = {"alt", "aria-label", "title", "placeholder", "data-title", "data-crumb"}


class Skel(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_starttag(self, tag, attrs):
        self.out.append("<%s %s>" % (tag, " ".join("%s=%s" % (k, v) for k, v in attrs if k not in TEXT_ATTRS)))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.out.append("</%s>" % tag)

    def handle_comment(self, data):
        self.out.append("<!--%s-->" % data)


def skel(path):
    p = Skel()
    p.feed(open(path, encoding="utf-8").read())
    return p.out


lang = sys.argv[1]
names = sys.argv[2:] or sorted(n[:2] for n in os.listdir(os.path.join(ROOT, "src", "en")))
bad = 0
for n in names:
    n = n[:2]
    src = os.path.join(ROOT, "src", "en", n + ".html")
    dst = os.path.join(ROOT, "src", lang, n + ".html")
    if not os.path.exists(dst):
        print(n, "MISSING"); bad += 1; continue
    a, b = skel(src), skel(dst)
    if a == b:
        print(n, "ok")
        continue
    bad += 1
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            print(n, "DIFF at tag #%d:\n  en: %s\n  %s: %s" % (i, x, lang, y)); break
    else:
        print(n, "DIFF: tag count %d vs %d" % (len(a), len(b)))
sys.exit(1 if bad else 0)
