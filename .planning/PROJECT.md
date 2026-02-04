# Personal-Claw

## What This Is

Personal-Claw is an anxiety-reduction system that sits between Jason and financial information sources (accountant, bank, tax office, etc.). It intercepts financial emails, provides neutral defused summaries via Discord, and enforces human-in-the-loop approval for all replies. The goal is to break the catastrophizing → avoidance → anxiety → sleep disruption cycle by removing emotional charge from financial communications.

## Core Value

Financial emails can be read and processed without triggering anxiety spirals. The system must never auto-send replies — human approval is mandatory.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Monitor Gmail inbox for emails from allowlisted financial contacts
- [ ] Batch non-urgent financial emails for scheduled delivery (default)
- [ ] Immediately deliver summaries for urgent/time-sensitive emails
- [ ] Send neutral, defused summaries to Discord using supportive/coaching tone
- [ ] Strip emotional/threatening language from email content
- [ ] Accept Discord input from single allowlisted user ID only (Jason)
- [ ] Support both text and voice input (voice transcribed to text)
- [ ] Allow free-form conversation for drafting replies (no rigid commands)
- [ ] Show draft reply in Discord for review/editing
- [ ] Require explicit "send this" phrase to trigger send flow
- [ ] Require confirmation ("confirm send to [name]?") before actually sending
- [ ] Never auto-send under any circumstances
- [ ] Gently surface avoidance after 24hrs ("Want to deal with it or snooze it?")
- [ ] Support vague deferral ("later" → ask when, or default sensibly)
- [ ] Voice input subject to same safety rules as text (no bypass)

### Out of Scope

- Spending tracking — Phase 2 (after email workflow proven)
- Savings goal monitoring — Phase 2
- Investment suggestions — Phase 2
- Multi-user support — Jason only
- Public channels/servers — DM or single private channel only
- Autonomous decision-making — Human approval required for all actions
- Real-time notifications for every email — Batching is default behavior

## Context

**The Problem:**
Jason experiences financial anxiety that manifests as:
1. Catastrophizing email content before reading ("I'm in trouble")
2. Avoidance/procrastination (defensive behavior)
3. Increased anxiety from not knowing + feeling behind
4. Sleep disruption
5. Cycle repeats

**Root Cause:**
Brain "hallucinates loaded language" — threat perception that isn't actually in the email content.

**The Solution Pattern:**
Create an emotional buffer between Jason and financial information:
- Neutral third-party reads the email first
- Strips threatening language
- Presents facts in supportive/coaching tone
- Removes urgency framing ("when ready" vs "immediately")
- Enforces deliberate action (approval gates prevent impulsive sends)

**Technical Environment:**
- Email: Gmail API
- Interface: Discord (text + voice via Discord voice messages)
- Deployment: N100 box (n100alerts) running OpenCode server
- Control: Tailscale SSH access

**Future Vision:**
Personal-Claw is the first module of a broader financial anxiety management system:
- Phase 1: Email (accountant, bank, tax office)
- Phase 2: Spending tracking with gentle coaching
- Phase 3: Savings goal monitoring
- Phase 4: Investment suggestions based on market trends

The email workflow establishes the pattern: **neutral buffering + supportive coaching + mandatory approval gates**.

## Constraints

- **Security**: Single allowlisted Discord user ID only — no multi-user support
- **Privacy**: Financial emails never logged or stored beyond operational needs
- **Safety**: NO auto-send under any circumstances — explicit approval required
- **Interface**: Discord only — no web UI, no email client, no other surfaces
- **Voice**: Must support voice input as first-class (Jason often drives/walks when checking)
- **Deployment**: Runs on N100 box — must survive reboots, run as system service
- **Email sources**: Allowlisted senders only (accountant, bank, tax office, etc.)
- **Tone**: Supportive/coaching, nurturing, more feminine than masculine (not clinical, not patronizing)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Discord as sole interface | Jason already uses Discord daily; supports text + voice naturally; familiar environment reduces friction | — Pending |
| Batched delivery by default | Reduces notification anxiety; prevents "oh god what now" feeling on every email | — Pending |
| Urgent emails break through batching | Critical/time-sensitive items can't wait; prevents real issues from being missed | — Pending |
| Two-step approval (send → confirm) | Prevents accidental sends; gives Jason time to reconsider; supports voice input safely | — Pending |
| Neutral tone without explicit defusing | Rewrite facts neutrally rather than calling out scary language; avoids patronizing "don't worry" framing | — Pending |
| Feminine, nurturing voice | Personal AI voice should feel more feminine and nurturing while staying calm and respectful | — Pending |
| Voice = text (same safety rules) | Prevents voice from bypassing safety gates; keeps mental model simple; no special privileges | — Pending |
| Gentle avoidance surfacing (24hr) | Supports Jason's awareness without being pushy; acknowledges procrastination without judgment | — Pending |
| Vague snooze timing allowed | Reduces decision fatigue; OpenClaw can ask for specifics or default sensibly; matches conversational style | — Pending |
| Email only for Phase 1 | Prove the anxiety-reduction pattern works before expanding to spending/savings/investing | — Pending |

---
*Last updated: 2025-02-02 after initialization*
