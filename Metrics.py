import os
import io
import re

repo_dir = r"C:\" # Main directory

exclude = [r""] # Excluded subdirectories

# Regex searches
patterns = [
    r"[};]", r"//(.*);",
    r"#define", r"#ifdef", r"#ifndef",
    r"malloc", r"=[^\S\r\n]*new", r"NULL", r"void[^\S\r\n]*\*",
    r"inline", r"virtual", r"volatile", r"\n[^\S\r\n/]*register ", r"goto[^\S\r\n]+",
    r"friend[^\S\r\n]+class",
    r"const_cast", r"dynamic_cast", r"static_cast", r"reinterpret_cast",

    r"#pragma once"
    r"const[^\S\r\n]+", r"noexcept", r"throw", r"override", r"explicit", r"enum class",
    r"=[^\S\r\n]*delete", r"=[^\S\r\n]*default",
    r"constexpr", r"static_assert",
    r"auto", r"nullptr",
    r"unique_ptr", r"shared_ptr", r"make_unique", r"make_shared",
    r"begin\(\)", r"end\(\)",
    r"std::", r"std::move", r"std::find", r"std::sort", r"std::transform",  r"std::function",
    r"std::vector", r"std::map", r"std::set", r"std::array", r"std::pair", r"std::tuple",
    r"int[\d]+_t", r"double", r"float", r"bool", r"void",
    r"_v<"
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
            matches[i] += len(re.findall(p, data))

print("Searched in " + str(len(all_files)) + " files.")
print(str(sum(matches)) + " matches total.\n")
for m, p in zip(matches, patterns):
    print(str(m) + ": " + str(p))
