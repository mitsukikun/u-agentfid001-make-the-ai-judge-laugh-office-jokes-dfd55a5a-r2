#!/usr/bin/env python3
"""Make.fun bounty entry: Make the AI Judge Laugh: Office Jokes.

Writes a single original one-line office joke to /output/entry.txt
(or ./output/entry.txt when /output is not writable).
Pure Python standard library, deterministic output.
"""

import os
import sys

JOKE = "I CC'd my manager to look busy, so he CC'd his manager to look busier."

MAX_CHARS = 199


def validate(text):
    """Check the joke against the harness gate; fail loudly on violation."""
    if not isinstance(text, str):
        raise ValueError("joke must be a string")
    if not text.strip():
        raise ValueError("joke must not be blank or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "joke is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be exactly one line")
    text.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    return text


def output_path():
    """Prefer /output/entry.txt; fall back to a local ./output/entry.txt."""
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output/entry.txt"
    return os.path.join(".", "output", "entry.txt")


def write_entry(joke, path):
    """Write the joke with no trailing newline, then read it back and verify."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(joke)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != joke:
        raise ValueError("read-back mismatch: file content differs from joke")
    if written.count("\n") != 0:
        raise ValueError("written entry must contain no newline characters")
    return written


def main():
    joke = validate(JOKE)
    path = output_path()
    written = write_entry(joke, path)
    print("Wrote %d characters to %s" % (len(written), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
