#!/bin/bash
# Read-only digest of recent chat sessions, for the nightly capture job.
# Edit these two paths for your setup.
export CAPTURE_HERMES_HOME="$HOME/.hermes"            # your profile folder (contains state.db)
export CAPTURE_VAULT="$HOME/Documents/Second Brain"   # your Obsidian vault
unset PYTHONPATH
exec /usr/bin/env python3 -I "$HOME/.hermes/scripts/capture_feed.py"
