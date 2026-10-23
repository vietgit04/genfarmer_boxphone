"""Assemble index.html: one page holding all four languages, switched in place.

usage: python3 tools/build.py

- Pages of each language become <section id="p-<lang>-<page>" lang="<lang>">; other ids inside
  them get a "<lang>--" prefix so they stay unique.
- Header, sidebar, table-of-contents label and search box are shared: text that differs between
  languages becomes <span data-l="..."> siblings, attributes that differ are listed in ATTRS.
- vi.html / es.html / ja.html are kept as redirects to index.html#/<lang>/... for old links.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGS = [("en", "English"), ("vi", "Tiếng Việt"), ("es", "Español"), ("ja", "日本語")]
CODES = [c for c, _ in LANGS]

STR = {
    "site": {"en": "GenFarmer Support Center", "vi": "Trung tâm hỗ trợ GenFarmer",
             "es": "Centro de soporte GenFarmer", "ja": "GenFarmer サポートセンター"},
    "lang": {"en": "Language", "vi": "Ngôn ngữ", "es": "Idioma", "ja": "言語"},
    "totop": {"en": "Back to top", "vi": "Lên đầu trang", "es": "Volver arriba", "ja": "ページの先頭へ"},
    "no_result": {"en": "No result for", "vi": "Không có kết quả cho", "es": "No hay resultados para",
                  "ja": "検索結果がありません:"},
    "video": {"en": "GenFarmer video tutorial", "vi": "Video hướng dẫn GenFarmer",
              "es": "Videotutorial de GenFarmer", "ja": "GenFarmer 動画チュートリアル"},
}

MAIN_OPEN = '<main class="main" id="main">'
MAIN_CLOSE = "</main>"
TAG_SPLIT = re.compile(r"(<[^>]+>)")
ATTR_RE = re.compile(r'\s([a-zA-Z-]+)="([^"]*)"')


def read(*p):
    return open(os.path.join(ROOT, *p), encoding="utf-8").read()


def merge_shell(parts, attrs):
    """Merge the same shell markup in every language into one, tagging text/attrs that differ."""
    toks = {c: TAG_SPLIT.split(parts[c]) for c in CODES}
    n = len(toks["en"])
    assert all(len(t) == n for t in toks.values()), "shell token count differs"
    out = []
    for i in range(n):
        vals = {c: toks[c][i] for c in CODES}
        en = vals["en"]
        if i % 2:  # tag
            if len(set(vals.values())) == 1:
                out.append(en)
                continue
            per = {c: dict(ATTR_RE.findall(vals[c])) for c in CODES}
            diff = {a: {c: per[c].get(a, "") for c in CODES} for a in per["en"]
                    if len({per[c].get(a) for c in CODES}) > 1}
            key = str(len(attrs))
            attrs[key] = diff
            out.append(re.sub(r"\s*(/?>)$", ' data-i18n-attr="%s"\\1' % key, en, count=1))
        else:  # text
            if len(set(vals.values())) == 1 or not en.strip():
                out.append(en)
                continue
            lead = en[: len(en) - len(en.lstrip())]
            trail = en[len(en.rstrip()):]
            spans = "".join(
                '<span data-l="%s"%s>%s</span>' % (c, "" if c == "en" else " hidden", vals[c].strip()) for c in CODES
            )
            out.append(lead + spans + trail)
    return "".join(out)


def localise_pages(html, code):
    def ids(m):
        v = m.group(1)
        return ' id="p-%s-%s"' % (code, v[2:]) if v.startswith("p-") else ' id="%s--%s"' % (code, v)

    html = re.sub(r'\sid="([^"]+)"', ids, html)
    return html.replace('<section class="page" ', '<section class="page" lang="%s" ' % code)


def lang_menu():
    items = "".join(
        '<button type="button" role="menuitemradio" data-set-lang="%s" aria-checked="false">'
        '<span class="code">%s</span><span class="nm">%s</span>'
        '<svg class="tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></button>' % (c, c.upper(), name)
        for c, name in LANGS
    )
    return (
        '<div class="langwrap">\n'
        '      <button class="langbtn" id="langBtn" type="button" aria-haspopup="menu" aria-expanded="false" aria-label="Language">\n'
        '        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" '
        'stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/>'
        '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10Z"/></svg>\n'
        '        <span id="langCode">EN</span>\n'
        '        <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>\n'
        '      </button>\n'
        '      <div class="langmenu" id="langMenu" role="menu">%s</div>\n'
        '    </div>\n    ' % items
    )


def redirect(code):
    return (
        '<!doctype html>\n<html lang="%(c)s">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>GenFarmer Support Center</title>\n'
        '<meta http-equiv="refresh" content="0; url=./#/%(c)s/home">\n'
        '<script>location.replace("./#/%(c)s/" + (location.hash.replace(/^#\\/?/, "") || "home"));</script>\n'
        '</head>\n<body><a href="./#/%(c)s/home">GenFarmer Support Center</a></body>\n</html>\n' % {"c": code}
    )


def main():
    head, tail = read("src", "head.html"), read("src", "tail.html")
    chunks = sorted(os.listdir(os.path.join(ROOT, "src", "en")))
    pre, pages, post = {}, {}, {}
    for c in CODES:
        body = "".join(read("src", c, n) for n in chunks)
        a = body.index(MAIN_OPEN) + len(MAIN_OPEN)
        b = body.index(MAIN_CLOSE)
        pre[c], pages[c], post[c] = body[:a], body[a:b], body[b:]

    # tab cua tung trang lay tu nhom sidebar chua no
    tabof = {}
    for tab, grp in re.findall(r'<div class="side-grp" data-tab="([a-z]+)">(.*?)\n      </div>', pre["en"], re.S):
        for page in re.findall(r'data-nav="([a-z0-9-]+)"', grp):
            tabof[page] = tab
    page_ids = re.findall(r'<section class="page" id="p-([a-z0-9-]+)"', pages["en"])
    assert set(page_ids) == set(tabof), set(page_ids) ^ set(tabof)

    attrs = {}
    shell_pre = merge_shell(pre, attrs)
    shell_post = merge_shell(post, attrs)
    anchor = '<button class="iconbtn" id="themeBtn"'
    assert shell_pre.count(anchor) == 1
    shell_pre = shell_pre.replace(anchor, lang_menu() + anchor)

    data = "".join(
        "  var %s = %s;\n" % (k, json.dumps(v, ensure_ascii=False))
        for k, v in (("PAGES", page_ids), ("TABOF", tabof), ("LANGS", CODES), ("STR", STR), ("ATTRS", attrs))
    )
    marker = "  /* PAGES, TABOF, LANGS, STR, ATTRS are injected by tools/build.py */\n"
    assert tail.count(marker) == 1
    body = shell_pre + "".join(localise_pages(pages[c], c) for c in CODES) + shell_post
    html = head + body + tail.replace(marker, marker + data)

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html", len(html), "bytes,", len(page_ids), "pages x", len(CODES), "languages")
    for c in CODES[1:]:
        with open(os.path.join(ROOT, c + ".html"), "w", encoding="utf-8") as f:
            f.write(redirect(c))


main()
