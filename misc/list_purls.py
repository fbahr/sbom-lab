#!/usr/bin/python3

import sys
import json

from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cdxfile = Path(sys.argv[1])
        if cdxfile.is_file():
            cdxreport = json.loads(cdxfile.read_text())

            purls = set()
            for c in cdxreport.get("components",[]):
                if c.get("purl"):
                    purls.add(c["purl"].removeprefix("pkg:maven/").removesuffix("?type=jar").removesuffix("?type=war"))
                else:
                    print(f"Component {c['name']} misses a PURL value!", file=sys.stderr)

            for c in cdxreport.get("dependencies",[]):
                ref = c["ref"].removeprefix("pkg:maven/").removesuffix("?type=jar").removesuffix("?type=war")
                if ":" in ref:
                    tokens = ref.rsplit(":",1)
                    tokens[0] = tokens[0].replace(":","/")
                    ref = "@".join(tokens)
                purls.add(ref)

                for d in c["dependsOn"]:
                    dep = d.removeprefix("pkg:maven/").removesuffix("?type=jar").removesuffix("?type=war")
                    if ":" in dep:
                        tokens = dep.rsplit(":",1)
                        tokens[0] = tokens[0].replace(":","/")
                        if "$" in tokens[1]:
                            # Hot-fix (for jbom SBOMs)
                            tokens[1] = "null"
                        dep = "@".join(tokens)
                    purls.add(dep)

            purls_dict = {}
            for purl in purls:
                tokens = purl.rsplit("@",1)
                if len(tokens) == 2:
                    pkg, version = tokens[0], tokens[1]
                else:
                    print(f"PURL with invalid pkg/ver scheme: {purl}!", file=sys.stderr)
                    pkg, version = tokens[0], "null"
                if purls_dict.get(pkg):
                    purls_dict[pkg].add(version)
                else:
                    purls_dict[pkg] = set([version])

            for pkg in sorted(purls_dict.keys()):
                # if pkg.startswith("null") or pkg.startswith("$"): #< hot-fix!
                #     continue
                if len(purls_dict[pkg]) > 1:
                    purls_dict[pkg] = purls_dict[pkg] - set(["null"])
                for version in purls_dict[pkg]:
                    print(f"{pkg}@{version}")
        else:
            print("Usage: ./list_purls.py <filename.json>", file=sys.stderr)
            print(f"`{cdxfile}` not found!", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: ./list_purls.py <filename.json>", file=sys.stderr)
        sys.exit(255)
