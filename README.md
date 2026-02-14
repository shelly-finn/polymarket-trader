# Revenue Generation System

This workspace is set up for autonomous revenue development. Every 30 minutes, the heartbeat triggers a revenue loop.

## Folder Structure

- **`scripts/`** - Automation scripts (heartbeat-monitor, gmail-monitor, idea-generator, etc.)
- **`databases/`** - JSON databases tracking opportunities, leads, completed tasks
- **`projects/`** - Active revenue projects (e.g., product MVP, service offering, automation)
- **`drafts/`** - Email templates, pitch decks, service descriptions (not sent without approval)
- **`research/`** - Market research, competitor analysis, pricing benchmarks
- **`assets/`** - Images, videos, templates, media for projects

## How It Works

### Heartbeat Loop (Every 30 minutes)

1. **Gmail Monitor** - Scans for incoming leads/opportunities matching keywords
   - Keywords: interested, opportunity, collaboration, partnership, budget, rate, availability
   - Results logged to `databases/opportunities.json`

2. **Status Check** - Reviews active opportunities and ideas
   - Shows count of active ideas, leads, and completed tasks
   - Identifies bottlenecks or stalled projects

3. **Idea Generation** - If no new leads found
   - Generates 1 new micro-revenue idea based on current capabilities
   - Logs to `databases/opportunities.json` with next steps

4. **Action Creation** - For each opportunity
   - Creates drafts, research docs, or task descriptions
   - Never sends emails or publishes without explicit approval

### Output

Each heartbeat produces:
- Summary of findings (leads found, ideas generated, progress made)
- Links to any new drafts or documents created
- Next concrete steps

## Tools Available

- **gog** - Gmail, Calendar, Drive, Contacts, Sheets, Docs
- **web_search** - Market research, competitor analysis
- **gemini** - Complex reasoning (used sparingly)
- **exec/scripts** - Automation, setup, deployment
- **bash** - System commands (full root access)

## Revenue Ideas & Tracking

All opportunities tracked in `databases/opportunities.json`:
- **Service offerings** - Consulting, setup, automation
- **Product ideas** - Software, templates, courses
- **Partnerships** - Integrations, referrals, collaborations
- **Automation** - Build tools to sell or license

Each idea has:
- Status: idea → in_progress → completed
- Effort: low/medium/high
- Revenue potential: low/medium/high
- Next steps (actionable tasks)
- Notes & research links

## Git & Version Control

Committed files:
- scripts/ and projects/ (version controlled)
- HEARTBEAT.md, revenue-ideas.md, strategic docs

Not committed:
- databases/ (active data)
- drafts/ (work in progress)
- research/ (raw research)
- assets/ (large files)

Use `git status` to see uncommitted changes. Commit regularly with meaningful messages.

## Safety & Autonomy

- ✅ Create drafts, documents, research, ideas
- ✅ Scan emails and calendar
- ✅ Run scripts and automation
- ✅ Organize files and projects
- ✅ Generate code and templates
- ❌ Send emails without explicit approval
- ❌ Publish or deploy without confirmation
- ❌ Destructive system changes without clear intent

## Next Steps

1. First heartbeat runs automatically in ~30 minutes
2. Monitor `HEARTBEAT.md` for checklist updates
3. Review generated ideas in `databases/opportunities.json`
4. Pick one to develop further and commit to `projects/`
5. Iterate: each heartbeat advances the most promising idea

---

**Goal: Make money autonomously, one heartbeat at a time.**
