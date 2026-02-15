# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Configured Tools

### GitHub
- **Account:** shelly-finn
- **Auth:** Google OAuth via gh CLI
- **Active Repos:**
  - openclaw-automation-consulting (https://github.com/shelly-finn/openclaw-automation-consulting)
  - heartbeat-automation (https://github.com/shelly-finn/heartbeat-automation)
  - openclaw-tools (https://github.com/shelly-finn/openclaw-tools)
- **Capabilities:** Push code, manage issues/PRs, workflows, public lead discovery

### Google Workspace (gog)
- **Account:** shellyfinn9@gmail.com
- **Auth:** GOG_KEYRING_PASSWORD="openclaw-test" (in .bashrc)
- **Services:** Gmail, Calendar, Drive, Contacts, Sheets, Docs
- **Use:** Email automation, outreach, document creation, spreadsheet tracking

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

