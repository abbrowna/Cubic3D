"""
Minify CSS source files into their .min.css counterparts.
Run directly:   python minify_css.py
Run via VS Code: wired as a preLaunchTask in .vscode/tasks.json
"""
import os
import rcssmin

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    # (source, output)
    ("app/static/app/content/sitev2.css",     "app/static/app/content/sitev2.min.css"),
    ("app/static/app/content/responsive.css", "app/static/app/content/responsive.css"),  # already plain
]

for src_rel, out_rel in FILES:
    src = os.path.join(BASE, src_rel)
    out = os.path.join(BASE, out_rel)
    if not os.path.exists(src):
        print(f"  SKIP  {src_rel} (not found)")
        continue
    with open(src, "r", encoding="utf-8") as f:
        css = f.read()
    
    # Preserve spaces in URLs by encoding them as %20 before minification
    import re
    css_encoded = re.sub(r"url\('([^']*\s[^']*)'\)", lambda m: f"url('{m.group(1).replace(' ', '%20')}')", css)
    css_encoded = re.sub(r'url\("([^"]*\s[^"]*)"\)', lambda m: f'url("{m.group(1).replace(" ", "%20")}")', css_encoded)
    
    minified = rcssmin.cssmin(css_encoded)
    
    # Restore readable spaces from %20 encoding (optional, but makes debugging easier)
    minified = minified.replace("%20", " ")
    
    with open(out, "w", encoding="utf-8") as f:
        f.write(minified)
    src_kb = os.path.getsize(src) / 1024
    out_kb = os.path.getsize(out) / 1024
    saving = 100 * (1 - out_kb / src_kb)
    print(f"  OK    {src_rel} → {out_rel}  ({src_kb:.1f} KB → {out_kb:.1f} KB, -{saving:.0f}%)")

print("Done.")
