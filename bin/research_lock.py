#!/usr/bin/env python3
"""Encrypt a research entry's rendered body for the client-side password gate.

Same at-rest scheme as the poem page (assets/enc/poem7-24-26.json): PBKDF2-SHA256
(300k iterations) -> AES-256-GCM via WebCrypto-compatible primitives. The payload
is JSON {"html": <post body HTML>} with every local <img> inlined as a data URI,
so no plaintext content or image ever needs to exist in this public repo — only
the ciphertext under assets/enc/. Master sources live OUTSIDE the repo (see the
research_src README where they are kept).

Workflow to (re)publish an entry:
  1. put the plaintext post .md back into _research/ locally (from the masters),
  2. build/serve so _site/research/<slug>/index.html exists with real content,
  3. python3 bin/research_lock.py <slug> <password>
  4. restore the locked stub .md (layout: research_locked + enc_payload path),
  5. commit assets/enc/research-<slug>.json + the stub. Never commit plaintext.

Usage: python3 bin/research_lock.py <slug> <password>
"""

import base64
import json
import os
import re
import sys

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

slug, password = sys.argv[1], sys.argv[2]
site = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(f"{site}/_site/research/{slug}/index.html").read()
i = html.find('<article class="post-content">')
j = html.rfind("</article>")
assert i != -1 and j > i, "post-content article not found in built page"
body = html[i + len('<article class="post-content">') : j]

MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "svg": "image/svg+xml", "webp": "image/webp", "gif": "image/gif"}


def inline(m):
    src = m.group(1)
    if not src.startswith("/"):
        return m.group(0)
    path = f"{site}/_site{src}"
    if not os.path.isfile(path):
        return m.group(0)
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    mime = MIME.get(src.rsplit(".", 1)[-1].lower(), "application/octet-stream")
    return m.group(0).replace(src, f"data:{mime};base64,{b64}")


body = re.sub(r'<img[^>]+src="([^"]+)"', inline, body)

iters = 300000
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iters).derive(
    password.encode()
)
ct = AESGCM(key).encrypt(iv, json.dumps({"html": body}).encode(), None)
out = {
    "v": 1,
    "kdf": "PBKDF2-SHA256",
    "iter": iters,
    "salt": base64.b64encode(salt).decode(),
    "iv": base64.b64encode(iv).decode(),
    "ct": base64.b64encode(ct).decode(),
}
os.makedirs(f"{site}/assets/enc", exist_ok=True)
dest = f"{site}/assets/enc/research-{slug}.json"
json.dump(out, open(dest, "w"))
print(f"wrote {dest} ({len(ct)} ct bytes, body {len(body)} chars)")
