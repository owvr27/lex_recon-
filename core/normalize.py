from __future__ import annotations
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

def normalize_url(u: str) -> str:
    u = u.strip()
    if not u:
        return ""
    # Ensure scheme for parsing
    if "://" not in u:
        u = "https://" + u
    parts = urlsplit(u)
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    path = parts.path or "/"
    # remove default ports
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    if scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]
    # normalize query ordering
    q = parse_qsl(parts.query, keep_blank_values=True)
    q.sort()
    query = urlencode(q, doseq=True)
    return urlunsplit((scheme, netloc, path, query, ""))  # drop fragment
