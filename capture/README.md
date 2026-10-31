# Capture loop

`capture_feed.py` prints a bounded, redacted digest of the last ~26 hours of your Hermes chats. It opens the profile's `state.db` **read-only** and never writes anything. A cron job runs it first and hands the output to the agent, which writes proposals to your Inbox.

## Set up

1. Copy `capture_feed.py` somewhere permanent (e.g. `~/.hermes/scripts/`).
2. Copy `capture_feed.sh` into your profile's `scripts/` folder, edit the two paths at the top, and make it executable (`chmod +x`).
3. Create the cron job with the Step 4 prompt, telling Hermes to use `capture_feed.sh` as the job's pre-run script.

## Environment

| Variable | Meaning |
|---|---|
| `CAPTURE_HERMES_HOME` | Your Hermes profile folder (the one containing `state.db`). Required. |
| `CAPTURE_VAULT` | Your vault root. Required; used only to list existing Inbox proposals. |
| `CAPTURE_HOURS` | Look-back window in hours (default 26). |
| `CAPTURE_MAX_CHARS` | Total digest cap (default 60000). |

Redaction covers emails, common API key and token formats, long hex strings, `password=`/`token=` pairs and Australian mobile numbers. Add patterns for anything else you don't want a model to see.
