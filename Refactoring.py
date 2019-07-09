import os
import io
import re

repo_dir = r"C:\" # Main directory
exclude = [r""] # Excluded subdirectories

# Regex [search, replace] patterns
patterns = [
    #[r"#ifndef(.*)_h\r?\n#define\1_h(?s)(.*)#endif[^\r\n]*\r?\n?", r"#pragma once\2"],
    #[r"NULL", r"nullptr"]
    ]

def is_excluded(root):
    for ex in exclude:
        if root.startswith(repo_dir + "\\" + ex):
            return True
    return False

def has_correct_file_ending(file):
    file = file.lower()
    return file.endswith(".cpp") or file.endswith(".h") or file.endswith(".inl")

def AllFiles():
    for root, dir, files in os.walk(repo_dir):
        if not is_excluded(root):
            for file in files:
                os.path.join(root, file)
                if has_correct_file_ending(file):
                   yield os.path.join(root, file)

matches = [0] * len(patterns)
all_files = list(AllFiles())

for file in all_files:
    print(file)
    with io.open(file, 'r', newline='') as open_file:
        data = open_file.read()
        for i, p in enumerate(patterns):
            data, count = re.subn(p[0], p[1], data)
            matches[i] += count
    with io.open(file, 'w', newline='') as open_file:
        open_file.write(data)

print("Searched in " + str(len(all_files)) + " files.")
print(str(sum(matches)) + " matches total.\n")
for m, p in zip(matches, patterns):
    print(str(m) + ": " + str(p))
