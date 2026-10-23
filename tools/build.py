"""Assemble the published pages from src/: index.html (en), vi.html, es.html, ja.html.

usage: python3 tools/build.py   (BUILD_LANGS=en,vi to build only some pages)
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGS = [
    # code, output file, label in the switcher, "No result for", video iframe title
    ("en", "index.html", "English", "No result for", "GenFarmer video tutorial"),
    ("vi", "vi.html", "Tiếng Việt", "Không có kết quả cho", "Video hướng dẫn GenFarmer"),
    ("es", "es.html", "Español", "No hay resultados para", "Videotutorial de GenFarmer"),
    ("ja", "ja.html", "日本語", "検索結果がありません:", "GenFarmer 動画チュートリアル"),
]

SWITCH_CSS = """
/* ---------- chon ngon ngu: nhan hien thi + select trong suot de dung menu goc cua he dieu hanh ---------- */
.langsw{
  position:relative;height:36px;display:inline-flex;align-items:center;flex-shrink:0;
  padding:0 28px 0 10px;border:1px solid var(--line);border-radius:var(--r);
  background:var(--surface) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%2398a0ad' stroke-width='3' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 10px center;
  color:var(--text);font-size:14px;font-weight:500;white-space:nowrap;
}
.langsw:hover{border-color:var(--line-strong)}
.langsw:focus-within{outline:2px solid var(--blue);outline-offset:1px}
.langsw select{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;font-size:16px}
.langsw .code{display:none}
@media (max-width:560px){
  .langsw{padding:0 22px 0 8px;font-size:13px;background-position:right 7px center}
  .langsw .full{display:none}
  .langsw .code{display:inline}
}
"""

JA_CSS = """
:root{--font:Inter,"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
"""

SWITCH_JS = """
<script>
(function(){
  /* doi ngon ngu nhung giu nguyen trang dang xem */
  var sel = document.getElementById("langSel");
  sel.addEventListener("change", function(){ location.href = sel.value + location.hash; });
})();
</script>
"""


def read(*p):
    return open(os.path.join(ROOT, *p), encoding="utf-8").read()


def main():
    head, tail = read("src", "head.html"), read("src", "tail.html")
    chunks = sorted(os.listdir(os.path.join(ROOT, "src", "en")))
    alternates = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (c, f) for c, f, *_ in LANGS)
    only = os.environ.get("BUILD_LANGS")
    for code, out, _label, noresult, vtitle in LANGS:
        if only and code not in only.split(","):
            continue
        body = "".join(read("src", code, n) for n in chunks)
        options = "".join(
            '<option value="%s"%s>%s</option>' % (f, " selected" if c == code else "", lbl) for c, f, lbl, *_ in LANGS
        )
        switch = (
            '<label class="langsw"><span class="full">%s</span><span class="code">%s</span>'
            '<select id="langSel" aria-label="Language">%s</select></label>\n    ' % (_label, code.upper(), options)
        )
        anchor = '<button class="iconbtn" id="themeBtn"'
        assert body.count(anchor) == 1, (code, "theme button anchor")
        body = body.replace(anchor, switch + anchor)

        h = head.replace('<html lang="en"', '<html lang="%s"' % code)
        extra_css = SWITCH_CSS + (JA_CSS if code == "ja" else "")
        h = h.replace("</style>", extra_css + "</style>", 1)
        fonts = "family=Inter:wght@400;500;600;700;800"
        if code == "ja":
            h = h.replace(fonts, fonts + "&family=Noto+Sans+JP:wght@400;500;700")
        h = h.replace("</head>", alternates + "</head>", 1)

        t = tail.replace("No result for &ldquo;", noresult + " &ldquo;")
        t = t.replace('title="GenFarmer video tutorial"', 'title="%s"' % vtitle)
        t = t.replace("</body>", SWITCH_JS + "</body>", 1)

        with open(os.path.join(ROOT, out), "w", encoding="utf-8") as f:
            f.write(h + body + t)
        print(out, len(h + body + t))


main()
