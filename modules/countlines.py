import os
from fnmatch import fnmatch

def countlines(directory, pattern="*.py"):
    lines = 0
    chars = 0
    chars_w_spaces = 0
    for path, _, files in os.walk(directory):
        for name in files:
            if fnmatch(name, pattern):
                with open(os.path.join(path, name), "r") as fp:
                    for _ in fp:
                        if 1: #len(_.strip()) != 0:
                            lines += 1
                            chars += len(_.strip())
                            chars_w_spaces += len(_)
    return lines, chars, chars_w_spaces