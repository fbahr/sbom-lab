#!/usr/bin/python3

import sys
import json

from pathlib import Path
import requests
import json

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cdxfile = Path(sys.argv[1])
        if cdxfile.is_file():
            cdxreport = json.loads(cdxfile.read_text())
            report = { "components": {} }
            for c in cdxreport.get("components",[]):
                hashes = c["hashes"] if c.get("hashes") else None
                hashes = c["externalReferences"][0]["hashes"] if not hashes and c.get("externalReferences") and c["externalReferences"][0].get("hashes") else hashes
                if hashes:
                   hash = [h["content"] for h in hashes if h["alg"] == "SHA-1"][0]
                else:
                   print(f"Component {c['name']} misses a SHA-1 hash!", file=sys.stderr)
                   continue

                purl = None
                property = [p for p in c["properties"] if p.get("name") and p["name"] == "maven" and p.get("value") and p["value"].startswith("https://search.maven.org/search?")] if c.get("properties") else []
                if property:
                    # Hot-fix for jbom SBOMs...
                    response = requests.get(f"https://search.maven.org/solrsearch/select?q=1:{hash}&rows=1&wt=json")
                    response.close()
                    if response.status_code == 200:
                        rjson = response.json()
                        if rjson and rjson.get("response") and rjson["response"].get("docs"):
                           descr = rjson["response"]["docs"][0]
                           purl = f"{descr['g']}/{descr['a']}@{descr['v']}"
                    else:
                        print(f"{c['name']} > {response=}", file=sys.stderr)
                elif c.get("purl"):
                    purl = c["purl"].removeprefix("pkg:maven/").removesuffix("?type=jar")

                if not purl:
                    print(f"Component \"{c['name']}\" misses a valid PURL!", file=sys.stderr)
                    purl = c["name"]

                report["components"][hash] = purl
    
            for k in sorted(report["components"].keys()):
                print(f"{k} {report['components'][k]} ")
        else:
            print("Usage: ./list_hashes.py <filename.json>", file=sys.stderr)
            print(f"`{cdxfile}` not found!", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: ./list_hashes.py <filename.json>", file=sys.stderr)
        sys.exit(255)
