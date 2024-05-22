#!/usr/bin/python3

import sys
import os

from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file1 = Path(sys.argv[1])
        file2 = Path(sys.argv[2])
        if not (file1.is_file() and file2.is_file()):
            print("Usage: ./compare_purls.py <purl_list_1.txt> <purl_list_2.txt>", file=sys.stderr)
            if not file1.is_file():
                print(f"`{file1}` not found!", file=sys.stderr)
            if not file2.is_file():
                print(f"`{file2}` not found!", file=sys.stderr)
            sys.exit(1)

        purl_set1 = set(file1.read_text().splitlines())
        purl_set2 = set(file2.read_text().splitlines())

        file1_only = purl_set1 - purl_set2
        if file1_only:
            print(f"{os.linesep}PURLs only appearing in {file1}:")
            for purl in sorted(file1_only):
                if not (purl.startswith("null") or purl.startswith("$")):
                    print(purl)

        file2_only = purl_set2 - purl_set1
        if file2_only:
            print(f"{os.linesep}PURLs only appearing in {file2}:")
            for purl in sorted(file2_only):
                if not (purl.startswith("null") or purl.startswith("$")):
                    print(purl)

        intersect = purl_set1.intersection(purl_set2)
        if intersect:
            print(f"{os.linesep}PURLs appearing both in {file1} and {file2}:")
            for purl in sorted(intersect):
                if not (purl.startswith("null") or purl.startswith("$")):
                    print(purl)
        
        unresolved_file1 = sorted([purl for purl in file1_only if purl.startswith("$") or purl.startswith("null")])
        if unresolved_file1:
            print(f"{os.linesep}Unresolved PURLs appearing in {file1}:")
            for purl in sorted(unresolved_file1):
                print(purl)

        unresolved_file2 = sorted([purl for purl in file2_only if purl.startswith("$") or purl.startswith("null")])
        if unresolved_file2:
            print(f"{os.linesep}Unresolved PURLs appearing in {file2}:")
            for purl in sorted(unresolved_file2):
                print(purl)
    else:
        print("Usage: ./compare_purls.py <purl_list_1.txt> <purl_list_2.txt>", file=sys.stderr)
        sys.exit(255)