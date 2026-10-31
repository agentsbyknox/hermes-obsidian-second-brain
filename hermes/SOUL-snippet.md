Set `OBSIDIAN_VAULT_PATH` to your vault in your Hermes `.env`, then paste this into `SOUL.md`:

```markdown
## Second Brain recall
My Obsidian vault (path in OBSIDIAN_VAULT_PATH) is my long-term memory. For questions about my work, preferences, projects or past decisions, start at "START HERE.md", search the vault, and answer from the notes. Cite every note you rely on as `Second Brain: relative/path.md`. Check each note's `last_updated`; if it is older than 6 months, say it may be stale. Ignore notes whose frontmatter says `agent_context: false` (such as unreviewed proposals in `00 Inbox`). Never edit the vault unless I ask.
```

The `agent_context` sentence is one addition to the paragraph shown in the video: it keeps unreviewed capture proposals out of answers until you approve them.

Tip: if you run more than one Hermes profile, put the vault path in that profile's `SOUL.md` too, so a demo or test profile can never wander into your real vault.
