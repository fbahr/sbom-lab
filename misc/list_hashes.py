#!/usr/bin/python3

import sys
import json

from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cdxfile = Path(sys.argv[1])
        if cdxfile.is_file():
            cdxreport = json.loads(cdxfile.read_text())
            report = { "components": {} }
            for c in cdxreport.get("components",[]):
                if c.get("purl"):
                    purl   = c["purl"].removeprefix("pkg:maven/").removesuffix("?type=jar")
                    hashes = c["hashes"] if c.get("hashes") else c["externalReferences"][0]["hashes"]
                    if hashes:
                        hash = [h["content"] for h in hashes if h["alg"] == "SHA-1"][0]
                        report["components"][hash] = purl
                    else:
                        print(f"Component {purl} misses a SHA-1 hash!", file=sys.stderr)
            for k in sorted(report["components"].keys()):
                print(f"{k} {report['components'][k]} ")
        else:
            print("Usage: ./list_hashes.py <filename.json>", file=sys.stderr)
            print(f"`{cdxfile}` not found!", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: ./list_hashes.py <filename.json>", file=sys.stderr)
        sys.exit(255)
