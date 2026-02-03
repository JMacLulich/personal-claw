# Requirements: Personal-Claw

**Defined:** 2025-02-02
**Core Value:** Financial emails can be read and processed without triggering anxiety spirals. The system must never auto-send replies — human approval is mandatory.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Email Interception

- [x] **EMAIL-01**: System monitors Gmail inbox for new emails via Gmail API
- [ ] **EMAIL-02**: System filters emails by allowlisted sender addresses/domains only
- [ ] **EMAIL-03**: System ignores all emails from non-allowlisted senders (security)
- [ ] **EMAIL-04**: System batches non-urgent emails for scheduled delivery (default behavior)
- [ ] **EMAIL-05**: System immediately delivers summaries for urgent/time-sensitive emails
- [ ] **EMAIL-06**: System tracks email status (new, summarized, drafted, awaiting_approval, sent, snoozed)
- [x] **EMAIL-07**: User can add/remove allowlisted senders via Discord commands
- [x] **EMAIL-08**: System automatically ignores spam and mailing list emails (common patterns detected)
- [x] **EMAIL-09**: System detects emails from actual people (criteria: personalized greeting with Jason's name, email structure, sender history, reply-to address is real person, message references shared context)
- [x] **EMAIL-10**: System prompts user immediately when detecting potential new contact ("We've identified [name] as someone you know — add to allowed list?")
- [x] **EMAIL-11**: System shows summary for potential new contact but blocks reply capability until user approves
- [x] **EMAIL-12**: User can decline to add detected person ("No, this is spam") or later add via command ("add [name] to allowed list")

### Neutral Summarization

- [ ] **SUMM-01**: System generates calm, factual summaries with no alarming language
- [ ] **SUMM-02**: System extracts key information (sender, subject, action needed, deadline if stated)
- [ ] **SUMM-03**: System sends summary to Discord in clear formatted message
- [ ] **SUMM-04**: System defuses triggering language (rewrites "urgent" as "routine", removes panic framing)
- [ ] **SUMM-05**: System uses supportive/coaching tone ("you've done well before" framing, not clinical)
- [ ] **SUMM-06**: System provides context-aware framing ("this was a big expense month" context when relevant)

### Reply Drafting & Approval

- [ ] **DRAFT-01**: User can draft replies via free-form conversational text input in Discord
- [ ] **DRAFT-02**: System displays full draft for review before any sending action
- [ ] **DRAFT-03**: System requires explicit "send this" phrase to initiate send flow (rejects "ok", "sure", "thanks")
- [ ] **DRAFT-04**: System requires confirmation ("Confirm send to [recipient name]?") after "send this"
- [ ] **DRAFT-05**: System never auto-sends under any circumstances (all send paths blocked without approval)
- [ ] **DRAFT-06**: User can edit draft via free-form conversation ("make it shorter", "add X", "change tone")
- [ ] **DRAFT-07**: User can draft replies via Discord voice messages (transcribed to text)
- [ ] **DRAFT-08**: System displays transcribed text back to user for visual confirmation before using

### Discord Interface

- [ ] **DISC-01**: System responds to text messages in Discord DM or configured private channel
- [ ] **DISC-02**: System accepts commands only from allowlisted Discord user ID (Jason's ID)
- [ ] **DISC-03**: System formats summaries and drafts clearly in Discord messages
- [ ] **DISC-04**: System accepts and transcribes Discord voice messages
- [ ] **DISC-05**: System supports free natural language input (minimal slash commands, conversational style)
- [ ] **DISC-06**: System enforces same safety rules for voice and text input (no approval bypass via voice)

### Avoidance Support

- [ ] **AVOID-01**: System tracks when summaries remain unresponded for 24 hours
- [ ] **AVOID-02**: System gently surfaces avoidance ("I sent a summary yesterday — want to deal with it or snooze it?")
- [ ] **AVOID-03**: System supports vague snooze timing ("later" → bot asks when, or defaults sensibly)

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Financial Tracking

- **TRACK-01**: System monitors bank account transactions
- **TRACK-02**: System tracks spending vs budget targets
- **TRACK-03**: System notifies when spending approaches target limits
- **TRACK-04**: System provides supportive coaching on spending patterns

### Savings Goals

- **SAVE-01**: System tracks savings goals with target amounts and deadlines
- **SAVE-02**: System calculates required savings per paycheck
- **SAVE-03**: System notifies when savings trajectory is off-target

### Investment Suggestions

- **INVEST-01**: System monitors market trends
- **INVEST-02**: System suggests investment opportunities based on risk profile
- **INVEST-03**: System explains investment suggestions in accessible language

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Multi-user support | Single-user anxiety-reduction tool for Jason only; complexity not justified |
| Web interface | Discord is the familiar safe space; adding web UI increases surface area |
| Auto-send based on confidence | Violates core value of mandatory human approval; catastrophic if wrong |
| Real-time notification for every email | Creates notification anxiety; batching is default to reduce stress |
| Inbox zero metrics | Productivity framing recreates anxiety; this is mental health tool, not productivity tool |
| Email thread management | Scope limited to individual emails; threading adds complexity without anxiety benefit |
| Calendar integration | Phase 1 is email only; calendar is future enhancement |
| Spending tracking in v1 | Prove email anxiety-reduction pattern works before expanding to spending |
| OAuth for multiple Gmail accounts | Single-user, single-account only |
| Public Discord servers/channels | Security risk; DM or single private channel only |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| EMAIL-01 | Phase 2 | Pending |
| EMAIL-02 | Phase 2 | Pending |
| EMAIL-03 | Phase 2 | Pending |
| EMAIL-04 | Phase 4 | Pending |
| EMAIL-05 | Phase 4 | Pending |
| EMAIL-06 | Phase 2 | Pending |
| EMAIL-07 | Phase 3 | Pending |
| EMAIL-08 | Phase 3 | Pending |
| EMAIL-09 | Phase 3 | Pending |
| EMAIL-10 | Phase 3 | Pending |
| EMAIL-11 | Phase 3 | Pending |
| EMAIL-12 | Phase 3 | Pending |
| SUMM-01 | Phase 5 | Pending |
| SUMM-02 | Phase 5 | Pending |
| SUMM-03 | Phase 5 | Pending |
| SUMM-04 | Phase 5 | Pending |
| SUMM-05 | Phase 5 | Pending |
| SUMM-06 | Phase 5 | Pending |
| DRAFT-01 | Phase 6 | Pending |
| DRAFT-02 | Phase 6 | Pending |
| DRAFT-03 | Phase 7 | Pending |
| DRAFT-04 | Phase 7 | Pending |
| DRAFT-05 | Phase 7 | Pending |
| DRAFT-06 | Phase 6 | Pending |
| DRAFT-07 | Phase 6 | Pending |
| DRAFT-08 | Phase 6 | Pending |
 | DISC-01 | Phase 6 | Pending |
 | DISC-02 | Phase 1 | Complete |
| DISC-03 | Phase 5 | Pending |
| DISC-04 | Phase 6 | Pending |
| DISC-05 | Phase 6 | Pending |
| DISC-06 | Phase 6 | Pending |
| AVOID-01 | Phase 8 | Pending |
| AVOID-02 | Phase 8 | Pending |
| AVOID-03 | Phase 8 | Pending |

**Coverage:**
- v1 requirements: 35 total
- Mapped to phases: 35 ✓
- Unmapped: 0 ✓

---
*Requirements defined: 2025-02-02*
*Last updated: 2025-02-02 after initial definition*
