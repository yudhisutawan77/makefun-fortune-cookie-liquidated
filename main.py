"""Fortune Cookie for the Liquidated Trader.

Writes one original fortune-cookie line for a crypto trader who has
just been liquidated, to the entry output path. The kit harness
exports MAKEFUN_OUTPUT_DIR and reads ``$MAKEFUN_OUTPUT_DIR/entry.txt``
afterwards, so that directory is honoured right after ENTRY_OUT.
"""

import os
import sys


FORTUNE = "Your lucky numbers are 5, 25, and 100 — the leverage levels that liquidated you."


def resolve_output_path():
    """Return the entry.txt path from the environment or the default.

    The harness may hand the output location over as a file path or as
    a directory; both are supported, and /output/entry.txt is the
    fallback named in the competition rules. Priority: ENTRY_OUT,
    then the kit harness directory MAKEFUN_OUTPUT_DIR, then
    ENTRY_OUT_DIR / OUTPUT / OUTPUT_DIR, then the default.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        if os.path.isdir(entry_out) or entry_out.endswith(("/", os.sep)):
            return os.path.join(entry_out, "entry.txt")
        return entry_out
    makefun_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if makefun_dir:
        # MAKEFUN_OUTPUT_DIR always names a directory, even before it
        # exists (makedirs in main() creates it).
        return os.path.join(makefun_dir, "entry.txt")
    for name in ("ENTRY_OUT_DIR", "OUTPUT", "OUTPUT_DIR"):
        value = os.environ.get(name)
        if value:
            if os.path.isdir(value) or value.endswith(("/", os.sep)):
                return os.path.join(value, "entry.txt")
            return value
    return "/output/entry.txt"


def main():
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(FORTUNE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
