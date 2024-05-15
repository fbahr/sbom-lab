#!/usr/bin/python3

import sys
import json

from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cdxfile = Path(sys.argv[1])
        if cdxfile.is_file():
            cdxreport = json.loads(cdxfile.read_text())

            purls     = set()
            metadata  = {}
            for c in cdxreport.get("components",[]):
                if c.get("purl"):
                    purls.add(c["purl"].removeprefix("pkg:maven/").removesuffix("?type=jar"))
                else:
                    # print(f"Component {c['name']} misses a PURL value!", file=sys.stderr)
                    metadata[c["name"]] = c["version"]

            for c in cdxreport.get("dependencies",[]):
                ref = c["ref"].removeprefix("pkg:maven/").removesuffix("?type=jar")
                if ":" in ref:
                    tokens = ref.rsplit(":",1)
                    tokens[0] = tokens[0].replace(":","/")
                    ref = "@".join(tokens)
                purls.add(ref)
                for d in c["dependsOn"]:
                    dep = d.removeprefix("pkg:maven/").removesuffix("?type=jar")
                    if ":" in dep:
                        tokens = dep.rsplit(":",1)
                        tokens[0] = tokens[0].replace(":","/")
                        if "$" in tokens[1]:
                            lib = tokens[0].rsplit("/",1)[1]
                            tokens[1] = "null" if not metadata.get(lib) else metadata[lib]
                        dep = "@".join(tokens)
                    purls.add(dep)

            purls_dict = {}
            for purl in purls:
                pkg, version = purl.rsplit("@",1)
                if purls_dict.get(pkg):
                    purls_dict[pkg].add(version)
                else:
                    purls_dict[pkg] = set([version])

            # for k, v in metadata.items():
            #     print(k,v)

            for pkg in sorted(purls_dict.keys()):
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
