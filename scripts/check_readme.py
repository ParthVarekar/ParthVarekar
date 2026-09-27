#!/usr/bin/env python3
"""Check that every image and link in README.md actually works.

Images must return HTTP 200 with an image content type (a broken image is an error).
Links must return a non-error status (a dead link is reported as a warning, since some
sites refuse automated requests).

    python scripts/check_readme.py README.md
"""
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (X11; Linux x86_64) profile-readme-check"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*,text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read(4096)
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), b""
    except Exception as e:  # DNS, TLS, timeout
        return 0, type(e).__name__, b""


def main(readme):
    text = Path(readme).read_text()
    base = Path(readme).parent
    images = sorted(set(re.findall(r'(?:src|srcset)="([^"]+)"', text)))
    links = sorted(set(re.findall(r'href="([^"]+)"', text) + re.findall(r"\]\((https?://[^)\s]+)\)", text)))

    errors = 0
    print("IMAGES")
    for url in images:
        if not url.startswith("http"):
            ok = (base / url.split("?")[0]).is_file()
            print(f"  {'ok ' if ok else 'ERR'}  file  {url}")
            errors += not ok
            continue
        # retry: freshly published files can take a moment to reach GitHub's raw file CDN
        for attempt in range(4):
            status, ctype, head = get(url)
            ok = status == 200 and ("image" in ctype or head.lstrip().startswith((b"<svg", b"<?xml")))
            if ok or attempt == 3:
                break
            time.sleep(20)
        print(f"  {'ok ' if ok else 'ERR'}  {status}  {ctype[:28]:<28}  {url}")
        if not ok:
            errors += 1
            print(f"::error title=Broken README image::{url} returned {status} {ctype}")

    print("LINKS")
    for url in links:
        if not url.startswith("http"):
            continue
        status, _, _ = get(url)
        ok = 200 <= status < 400
        print(f"  {'ok ' if ok else 'WRN'}  {status}  {url}")
        if not ok:
            print(f"::warning title=README link failed::{url} returned {status}")

    print(f"\n{len(images)} images checked, {errors} broken; {len(links)} links checked")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "README.md"))
