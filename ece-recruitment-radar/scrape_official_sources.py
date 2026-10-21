#!/usr/bin/env python3
"""Polite official-source link discovery. Does not verify live application status or eligibility."""
import hashlib, json, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urldefrag, urlparse
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
USER_AGENT = "ECE-Recruitment-Radar/1.0 (public official-notice discovery)"
TIMEOUT = (5, 10)
MAX_BYTES = 2_000_000
MAX_LINKS_PER_SOURCE = 40
RELEVANT = re.compile(r"recruit|career|vacanc|advertisement|notification|job opening|job opportunity|engineer trainee|graduate engineer|scientist|technical officer|technician|apprentice|executive trainee|junior engineer|assistant engineer|rrb|ssc je|engineering services|gate 2027|gate score|application form|apply online|corrigendum|addendum|admit card|call letter|exam date|answer key|result|shortlist|document verification|skill test|cbt|employment notice|walk.?in|project engineer|probationary engineer|management trainee|latest.?job|current opportunities|what.?s new|recruitment notice", re.I)
HIGH = re.compile(r"recruit|vacanc|advertisement|notification|engineer trainee|graduate engineer|scientist|technical officer|technician|apprentice|executive trainee|junior engineer|application form|apply online|employment notice|probationary engineer|project engineer|job opening|job opportunity", re.I)
DATE_RE = re.compile(r"\b(?:\d{1,2}[./-]\d{1,2}[./-](?:20)?\d{2}|\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+20\d{2}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+20\d{2})\b", re.I)

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def read_json(path, default):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return default

def make_id(url):
    return hashlib.sha256(urldefrag(url)[0].rstrip("/").encode()).hexdigest()[:16]

def extract(html, base, source):
    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript", "svg"]): node.decompose()
    found, seen = [], set()
    for a in soup.find_all("a", href=True):
        title = " ".join(a.get_text(" ", strip=True).split())
        href = a.get("href", "").strip()
        if len(title) < 4 or not href or href.startswith(("javascript:", "mailto:", "tel:", "#")): continue
        url = urldefrag(urljoin(base, href))[0]
        if urlparse(url).scheme not in ("http", "https") or url.rstrip("/") in seen: continue
        parent = a.parent
        context = " ".join(parent.get_text(" ", strip=True).split())[:500] if parent else title
        hay = title + " " + context
        if not RELEVANT.search(hay): continue
        seen.add(url.rstrip("/"))
        dt = DATE_RE.search(hay)
        found.append({"id":make_id(url),"title":title[:240],"url":url,"source_id":source["id"],"source_name":source["name"],"category":source["category"],"snippet":context,"date_text":dt.group(0) if dt else None,"first_seen":None,"last_seen":None,"is_new":False,"relevance":"high" if HIGH.search(title) else "normal","route_hint":"GATE mentioned; verify notice" if re.search(r"\bGATE\b",hay,re.I) else "Route not inferred; verify notice","verification":"Unverified link discovery"})
    found.sort(key=lambda n:(n["relevance"]=="high",bool(n["date_text"]),len(n["title"])),reverse=True)
    return found[:MAX_LINKS_PER_SOURCE]

def main():
    sources = read_json(DATA/"sources.json", [])
    old = read_json(DATA/"live-notices.json", {})
    old_items = old.get("notices", []) if isinstance(old, dict) else []
    old_by = {n.get("id"):n for n in old_items if n.get("id")}
    initial = not bool(old.get("generated_at"))
    session = requests.Session()
    session.headers.update({"User-Agent":USER_AGENT,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.7"})
    notices, results, errors = [], [], []
    for i, src in enumerate(sources):
        health = {"id":src["id"],"name":src["name"],"url":src["url"],"category":src["category"],"checked_at":now(),"ok":False,"status_code":None,"found_links":0,"error":None}
        try:
            with session.get(src["url"], timeout=TIMEOUT, allow_redirects=True, stream=True) as r:
                health["status_code"] = r.status_code
                r.raise_for_status()
                ctype = r.headers.get("Content-Type","").lower()
                if "html" not in ctype and "xml" not in ctype and ctype:
                    raise RuntimeError("Not an HTML/XML listing ("+ctype[:100]+")")
                chunks, total = [], 0
                for chunk in r.iter_content(65536):
                    total += len(chunk)
                    if total > MAX_BYTES: break
                    chunks.append(chunk)
                items = extract(b"".join(chunks), r.url, src)
            health["ok"] = True
            health["found_links"] = len(items)
            for n in items:
                prev = old_by.get(n["id"],{})
                n["first_seen"] = prev.get("first_seen") or now()
                n["last_seen"] = now()
                n["is_new"] = (not initial and n["id"] not in old_by)
                notices.append(n)
        except Exception as exc:
            health["error"] = str(exc)[:260]
            errors.append({"source_id":src["id"],"source_name":src["name"],"url":src["url"],"error":health["error"]})
            for old_n in old_items:
                if old_n.get("source_id")==src["id"]:
                    carried=dict(old_n); carried["is_new"]=False; carried["stale"]=True; notices.append(carried)
        results.append(health)
        print(("OK " if health["ok"] else "WARN ")+src["name"]+f": {health['found_links']} links"+(f" ({health['error']})" if health["error"] else ""))
        if i < len(sources)-1: time.sleep(0.35)
    unique = {}
    for n in notices: unique[n["id"]]=n
    all_notices=sorted(unique.values(),key=lambda n:(bool(n.get("is_new")),n.get("relevance")=="high",n.get("last_seen","")),reverse=True)
    feed={"schema_version":1,"generated_at":now(),"source_count":len(sources),"ok_source_count":sum(s["ok"] for s in results),"new_count":sum(n.get("is_new",False) for n in all_notices),"initial_run":initial,"sources":results,"errors":errors,"notices":all_notices}
    (DATA/"live-notices.json").write_text(json.dumps(feed,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"\nScanned {len(sources)} sources; {feed['ok_source_count']} responded; {len(all_notices)} links retained; {feed['new_count']} newly detected links; {len(errors)} fetch errors.")

if __name__ == "__main__":
    main()
