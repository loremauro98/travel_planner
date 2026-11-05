---
trigger: always_on
description: Monitor conversation depth and periodically report context usage milestones to the user.
---

# Context Health & Compaction Monitor

To prevent language server resource exhaustion and unexpected session drops:

1. **Milestone Reporting (Every ~10 Turns or at 10% Intervals):**
   - At conversational milestones (every ~10 user turns, or upon crossing estimated context thresholds like 100k, 150k, 200k tokens):
   - Check the recent token count in `.system_generated/logs/transcript.jsonl` or estimate from session depth.
   - Append a lightweight footer to your response:
     `> [Context Health: ~Xk / 1,000k (Y%) | Turn Z]`

2. **Compaction & Session Reset Alert:**
   - **Threshold Warning (>= 150k tokens or >= 40 turns):** Add a proactive recommendation warning:
     `> [!TIP] Context load is growing (>150k tokens). Consider running `/compact` or starting a fresh session for the next task to keep the backend responsive and prevent restarts.`
   - **Critical Warning (>= 200k tokens or >= 75 turns):** Strongly advise running `/compact` or starting a fresh session before executing heavy multi-file diffs.
