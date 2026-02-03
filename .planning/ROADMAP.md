# Roadmap: Personal-Claw

## Overview

Personal-Claw breaks the financial anxiety cycle by intercepting Gmail, delivering neutral summaries via Discord, and enforcing mandatory approval for replies. This roadmap delivers the core anxiety-reduction pattern: monitor allowlisted financial contacts → defuse threatening language → support conversational drafting with voice → enforce two-step approval gates → gently surface avoidance after 24 hours.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation & Security** - Discord bot + Gmail API + single-user access control
- [ ] **Phase 2: Email Monitoring** - Watch inbox, filter by allowlist, track email state
- [ ] **Phase 3: Smart Contact Detection** - Manage allowlist, detect people vs spam, prompt for new contacts
- [ ] **Phase 4: Batching & Urgency** - Schedule non-urgent emails, deliver urgent summaries immediately
- [ ] **Phase 5: Neutral Summarization** - Defuse triggering language, supportive coaching tone
- [ ] **Phase 6: Reply Drafting & Voice** - Conversational drafting with voice transcription
- [ ] **Phase 7: Send Approval Gates** - Two-step approval ("send this" → confirm) with no bypass
- [ ] **Phase 8: Avoidance Support** - Track 24hr delays, gentle nudges, vague snooze timing

## Phase Details

### Phase 1: Foundation & Security
**Goal**: Discord bot connected to Gmail API with single-user access control
**Depends on**: Nothing (first phase)
**Requirements**: DISC-02
**Success Criteria** (what must be TRUE):
  1. Discord bot responds to messages from Jason's allowlisted Discord user ID only
  2. Discord bot rejects commands from any other Discord user with clear message
  3. Bot connects to Gmail API successfully and can read inbox
  4. Bot runs as system service on N100 box and survives reboots
**Plans**: 4 plans

 Plans:
- [x] 01-01-PLAN.md — Project foundation with dependencies and config ✓ 2026-02-03
- [x] 01-02-PLAN.md — Discord bot with user allowlist enforcement ✓ 2026-02-03
- [x] 01-03-PLAN.md — Gmail API integration with OAuth token management ✓ 2026-02-03
- [x] 01-04-PLAN.md — Integration, systemd service, and deployment ✓ 2026-02-03

### Phase 2: Email Monitoring
**Goal**: System watches Gmail inbox and filters by allowlisted senders
**Depends on**: Phase 1
**Requirements**: EMAIL-01, EMAIL-02, EMAIL-03, EMAIL-06
**Success Criteria** (what must be TRUE):
  1. System detects new emails from Gmail inbox within 5 minutes of arrival
  2. System processes only emails from allowlisted sender addresses/domains
  3. System ignores all non-allowlisted emails without action or notification
  4. System tracks email state (new, summarized, drafted, awaiting_approval, sent, snoozed)
**Plans**: TBD

Plans:
- [ ] 02-01: TBD during phase planning

### Phase 3: Smart Contact Detection
**Goal**: User manages allowlist and system detects new people vs spam
**Depends on**: Phase 2
**Requirements**: EMAIL-07, EMAIL-08, EMAIL-09, EMAIL-10, EMAIL-11, EMAIL-12
**Success Criteria** (what must be TRUE):
  1. User can add allowlisted senders via Discord command ("add [email] to allowed list")
  2. User can remove allowlisted senders via Discord command ("remove [email] from allowed list")
  3. System automatically ignores spam and mailing lists without prompting user
  4. System detects emails from actual people (personalized greeting, real sender, shared context)
  5. System immediately prompts Jason when detecting potential new contact ("Add [name] to allowed list?")
  6. User can see summary for detected person but cannot reply until approved
  7. User can decline detected person ("No, this is spam") or manually add later
**Plans**: TBD

Plans:
- [ ] 03-01: TBD during phase planning

### Phase 4: Batching & Urgency
**Goal**: Non-urgent emails batched for scheduled delivery, urgent emails delivered immediately
**Depends on**: Phase 3
**Requirements**: EMAIL-04, EMAIL-05
**Success Criteria** (what must be TRUE):
  1. System batches non-urgent emails and delivers summaries on schedule (default behavior)
  2. System detects urgent/time-sensitive keywords and delivers those summaries immediately
  3. User receives single batched Discord message with multiple non-urgent summaries
  4. User receives immediate separate Discord message for each urgent email
**Plans**: TBD

Plans:
- [ ] 04-01: TBD during phase planning

### Phase 5: Neutral Summarization
**Goal**: System generates calm, defused summaries with supportive coaching tone
**Depends on**: Phase 4
**Requirements**: SUMM-01, SUMM-02, SUMM-03, SUMM-04, SUMM-05, SUMM-06, DISC-03
**Success Criteria** (what must be TRUE):
  1. Summaries use calm, factual language with no alarming words
  2. Summaries extract key information (sender, subject, action needed, deadline)
  3. Summaries appear in Discord as clear formatted messages
  4. System rewrites "urgent" as "routine" and removes panic framing from original emails
  5. Summaries use supportive/coaching tone ("you've handled this before" framing)
  6. System provides context-aware framing when relevant ("big expense month" context)
**Plans**: TBD

Plans:
- [ ] 05-01: TBD during phase planning

### Phase 6: Reply Drafting & Voice
**Goal**: User drafts replies via free-form text or voice with natural conversation
**Depends on**: Phase 5
**Requirements**: DRAFT-01, DRAFT-02, DRAFT-06, DRAFT-07, DRAFT-08, DISC-01, DISC-04, DISC-05, DISC-06
**Success Criteria** (what must be TRUE):
  1. User writes free-form conversational text to draft reply ("Tell them I'll have it Friday")
  2. System displays full draft for review before any sending action
  3. User can edit draft via conversation ("make it shorter", "add X", "change tone")
  4. User sends Discord voice message to draft reply (while driving or walking)
  5. System transcribes voice message to text and displays for confirmation
  6. System applies same safety rules to voice input as text (no approval bypass)
  7. Bot supports natural language without rigid slash commands
**Plans**: TBD

Plans:
- [ ] 06-01: TBD during phase planning

### Phase 7: Send Approval Gates
**Goal**: Two-step approval required for all sends with no bypass possible
**Depends on**: Phase 6
**Requirements**: DRAFT-03, DRAFT-04, DRAFT-05
**Success Criteria** (what must be TRUE):
  1. System requires explicit "send this" phrase to initiate send flow
  2. System rejects vague approvals like "ok", "sure", "thanks" for sending
  3. System prompts for confirmation after "send this" ("Confirm send to [recipient name]?")
  4. System sends email only after user confirms (e.g., "yes", "confirm", "send it")
  5. No path exists to auto-send under any circumstances (code-level enforcement)
**Plans**: TBD

Plans:
- [ ] 07-01: TBD during phase planning

### Phase 8: Avoidance Support
**Goal**: Gentle 24hr nudges with vague snooze timing support
**Depends on**: Phase 7
**Requirements**: AVOID-01, AVOID-02, AVOID-03
**Success Criteria** (what must be TRUE):
  1. System tracks when summaries remain unresponded for 24 hours
  2. System sends gentle reminder ("I sent a summary yesterday — want to deal with it or snooze it?")
  3. User can respond with vague timing ("later") and system asks for specifics or defaults sensibly
  4. System does not nag repeatedly — one nudge per email, then respects snooze
**Plans**: TBD

Plans:
- [ ] 08-01: TBD during phase planning

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Security | 1/4 | In progress | - |
| 2. Email Monitoring | 0/TBD | Not started | - |
| 3. Smart Contact Detection | 0/TBD | Not started | - |
| 4. Batching & Urgency | 0/TBD | Not started | - |
| 5. Neutral Summarization | 0/TBD | Not started | - |
| 6. Reply Drafting & Voice | 0/TBD | Not started | - |
| 7. Send Approval Gates | 0/TBD | Not started | - |
| 8. Avoidance Support | 0/TBD | Not started | - |
