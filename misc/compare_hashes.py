#!/usr/bin/python3

import sys
import os

from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file1 = Path(sys.argv[1])
        file2 = Path(sys.argv[2])
        if not (file1.is_file() and file2.is_file()):
            print("Usage: ./fcomp.py <hash_list_1.txt> <hash_list_2.txt>", file=sys.stderr)
            if not file1.is_file():
                print(f"`{file1}` not found!", file=sys.stderr)
            if not file2.is_file():
                print(f"`{file2}` not found!", file=sys.stderr)
            sys.exit(1)  
        hash_list1 = file1.read_text().splitlines()
        hash_list2 = file2.read_text().splitlines()

        hash_set1 = set([line.split(" ",1)[0] for line in hash_list1])
        hash_set2 = set([line.split(" ",1)[0] for line in hash_list2])

        file1_only = hash_set1 - hash_set2
        if file1_only:
            print(f"{os.linesep}Hashes only appearing in {file1}:")
            for hash in file1_only:
                for line in hash_list1:
                    if line.startswith(hash):
                        print(line)
                        break

        file2_only = hash_set2 - hash_set1
        if file2_only:
            print(f"{os.linesep}Hashes only appearing in {file2}:")
            for hash in file2_only:
                for line in hash_list2:
                    if line.startswith(hash):
                        print(line)
                        break

        intersect = hash_set1.intersection(hash_set2)
        if intersect:
            print(f"{os.linesep}Hashes appearing both in {file1} and {file2}:")
            for hash in intersect:
                line1, line2 = "", ""
                for line in hash_list1:
                    if line.startswith(hash):
                        line1 = line
                        break
                for line in hash_list2:
                    if line.startswith(hash):
                        line2 = line
                        break
                cmp = "==" if line1 == line2 else "<>"
                print(f"{line1}{cmp} {line2.split(' ',1)[1]}")
    else:
        print("Usage: ./fcomp.py <hash_list_1.txt> <hash_list_2.txt>", file=sys.stderr)
        sys.exit(255)