# Hermes + Obsidian Second Brain: starter kit

Give your [Hermes](https://hermes-agent.nousresearch.com/docs) agent a long-term memory that gets smarter every week, using a free Obsidian vault. Nothing becomes part of the memory until **you** approve it.

▶️ **Video walkthrough (9 min):** https://www.youtube.com/watch?v=v1Rgnc1mHYs
📘 **Step-by-step guide:** https://atlas-knox-guide.vercel.app/ep04/

## What's in here

| Path | What it is |
|---|---|
| `vault/` | A ready-made example vault (folders, `START HERE`, Memory Protocol, frontmatter schema, sample notes). Open it in Obsidian, then replace the notes in `10 Identity/` with your own. |
| `hermes/SOUL-snippet.md` | The paragraph that connects recall: answers come from your notes, with citations. |
| `prompts/` | The four prompts used in the video, in order. |
| `capture/` | The nightly capture loop: a read-only script that prints the day's chats, plus the cron job prompt that turns them into *proposals*. |

## The loop

```
Capture → Distil → Review → Promote → Recall → (better answers, new captures)
```

1. **Build the vault.** Copy `vault/` somewhere permanent and open it in Obsidian.
2. **Teach it who you are.** Edit `10 Identity/`, then run [`prompts/step2-teach-it-who-you-are.md`](prompts/step2-teach-it-who-you-are.md).
3. **Connect recall.** Set `OBSIDIAN_VAULT_PATH` in your Hermes `.env` and paste [`hermes/SOUL-snippet.md`](hermes/SOUL-snippet.md) into `SOUL.md`. Test it with [`prompts/step3-test-recall.md`](prompts/step3-test-recall.md).
4. **Automate capture.** Set up [`capture/`](capture/README.md) and run [`prompts/step4-nightly-capture.md`](prompts/step4-nightly-capture.md).
5. **Review and promote weekly.** Run [`prompts/step5-weekly-review.md`](prompts/step5-weekly-review.md).

## The promotion ladder

| Signal | Goes to |
|---|---|
| A stable fact or preference needed every session | Built-in memory (`USER.md` / `MEMORY.md`) |
| A reusable procedure | A skill |
| Durable knowledge or research | A vault note |
| A decision, and why | `60 Decisions/Decision Log.md` |
| One-off task progress | Let it die |

## Guardrails

- **The agent proposes, you approve.** The capture job writes only to `00 Inbox/`; it never edits notes, memory or skills.
- **Sources over vibes.** Every recalled fact cites `Second Brain: <path>`; `last_updated` decides freshness.
- **No secrets, no raw transcripts** in the vault. The capture script redacts emails, keys and tokens before the model sees anything.
- `40 Resources/Old camera settings.md` is deliberately out of date, so you can check that your agent flags stale notes.

## Cost

Nothing extra. Obsidian is free for personal use, Hermes is free and open source, and the model can run on a subscription you already pay for.

## Notes

- Tested with Hermes Agent on macOS. If anything here disagrees with the [Hermes docs](https://hermes-agent.nousresearch.com/docs), the docs win.
- Independent project; not affiliated with Nous Research or Obsidian.
- New Hermes episode weekly → https://www.youtube.com/@AgentsByKnox?sub_confirmation=1

MIT licensed. Made by [Atlas Knox](https://www.youtube.com/@AgentsByKnox).
