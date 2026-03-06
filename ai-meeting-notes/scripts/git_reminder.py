#!/usr/bin/env python
"""Utility script to remind developer to commit and push changes."""

import sys

if __name__ == "__main__":
    print("Don't forget to run: git add . && git commit -m \"your message\" && git push")
    sys.exit(0)
