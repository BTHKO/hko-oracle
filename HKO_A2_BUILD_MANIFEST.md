# HKO ESL Generator 2030 — A2 HR English
# BUILD MANIFEST v2.0 — Based on GEN_A2_L01_V3 Standard

---

## 1. SERIES OVERVIEW

| Property | Value |
|---|---|
| Course | A2 HR English — MineSafe Santiago |
| Lessons | L01–L12 + Quiz 1 (after L06) + Quiz 2 (after L12) |
| Format | Single-file HTML5 · SCORM 1.2 · Self-contained |
| Viewport | 960px max-width · Full-height chrome |
| Font stack | DM Sans + Syne (Google Fonts) |
| TTS engine | Piper TTS (local) · Female: en_US-lessac-medium · Male: en_US-ryan-medium |
| Audio format | WAV → base64 embedded in HTML |
| Standard | GEN_A2_L01_V3 is the canonical reference |

---

## 2. COLOUR SYSTEM (fixed across all lessons)

```css
--vocab:   #6b7c3a   /* olive-green  — Word Builder topbar + headers */
--gram:    #2e6b6b   /* teal         — Useful Language topbar + headers */
--fire:    #d46a1f   /* orange       — XP, alerts, quiz banner */
--ok:      #2e8b57   /* green        — correct answers */
--err:     #c0392b   /* red          — wrong answers */
--surface: #ffffff
--bg:      #f4f7fb
```

---

## 3. CHROME STRUCTURE (identical every lesson)

```
┌─────────────────────────────────────────────┐
│ TOPBAR (56px) — solid colour, changes per   │
│ section: olive vocab / teal grammar         │
│ [progress bar 14px] [Stage X/14] [XP badge] │
├─────────────────────────────────────────────┤
│ SECTION TABS (48px)                         │
│ [Part 1 · Word Builder] [Part 2 · UL 🎁]   │
│                              [Stage X / 14] │
├─────────────────────────────────────────────┤
│ STAGE HEADER (44px)                         │
│ [Stage tag]  [Title]   [Part 1] [Part 2 🎁] │
├─────────────────────────────────────────────┤
│ CONTENT ZONE (flex:1, scrollable)           │
│ Activity injected here by JS renderer       │
├─────────────────────────────────────────────┤
│ ACTION BAR (58px)                           │
│ [‹ BACK] [CHECK] [↩ RETRY] [pips] [NEXT ›] │
│                             [NEXT STAGE →]  │
└─────────────────────────────────────────────┘
```

### Overlays (z-index stacking)
- `#landing` — full-screen landing page (z:200), fades out on START
- `.gate-modal` — stage complete modal (z:999), confetti, XP display
- `.badge-toast` — badge notification (z:1000), bottom-centre

---

## 4. STAGE STRUCTURE (14 per lesson)

### Section A — Word Builder (V1–V7)
| Stage | ID | Activity | Part 2 (Bonus) | Gate |
|---|---|---|---|---|
| V1 | v1 | Scene Entry — 4 MCQ image observation | María story listen + 4 MCQ | Part 1 ≥70% |
| V2 | v2 | Vocab Cards (8 words, TTS each) | Word Match (6 pairs) | Part 1 ≥70% |
| V3 | v3 | Memory Game (8 pairs) + Type-in | Hangman / Word Detective | Part 1 ≥70% |
| V4 | v4 | Pronunciation Sort (-ed endings, 10 words) | Story Cloze (5 gap-fill) | Part 1 ≥70% |
| V5 | v5 | Dialogue MCQ (4Q) | Vocab Shoot game | Part 1 ≥70% |
| V6 | v6 | Gap Fill — type in (6 sentences) | Sentence Builder (3 sentences) | Part 1 ≥70% |
| V7 | v7 | Speaking task (record + rubric) | — | auto-pass |

### Section B — Useful Language (G1–G7)
| Stage | ID | Activity | Part 2 (Bonus) | Gate |
|---|---|---|---|---|
| G1 | g1 | Grammar Discovery (click highlight) | Grammar MCQ (4Q) | Part 1 auto |
| G2 | g2 | Grammar Sort (9 sentences, 3 columns) | Form Finder MCQ (4Q) | Part 1 ≥70% |
| G3 | g3 | Grammar Frame Fill (5 slots) | Dialogue Rebuild (3 sentences) | Part 1 ≥70% |
| G4 | g4 | Error Spotter (8 sentences) | Story Grammar MCQ (4Q) | Part 1 ≥70% |
| G5 | g5 | Sentence Repair MCQ (4Q) | Grammar Builder (3 sentences) | Part 1 ≥70% |
| G6 | g6 | Free Write (min 25 words) | Grammar Gap Fill (4 slots) | Part 1 ≥70% |
| G7 | g7 | Professional Email (min 40 words) | Can-Do Checklist | auto-pass |

---

## 5. ACTIVITY RANDOMISATION RULES

Every activity MUST shuffle on each load. Rules per type:

| Activity Type | Shuffle Rule |
|---|---|
| MCQ options | `opts.sort(() => Math.random() - 0.5)` per question |
| MCQ questions | Paginated; always Q1 first, rest randomised |
| Word match | Both columns independently shuffled |
| Memory game | Full card array shuffled |
| Sentence builder tiles | Tile order shuffled |
| Grammar sort chips | Bank shuffled before render |
| Pron sort chips | Bank shuffled before render |
| Fill-select option pills | Shuffled per row |
| Error spotter items | Array shuffled each render |
| Hangman words | Array shuffled; new word each NEXT WORD |
| Gap fill hints | Pills per row shuffled |

**Recycling rule:** `STAGES` array is fixed but within each activity renderer, data arrays (`MEM_PAIRS`, `PRON_DATA`, `GSORT`, `ERR_ITEMS`, `HG_WORDS`, etc.) are shuffled each time `render*()` is called.

**New activity variants** to add per lesson cycle (rotate through):
- MCQ: "Which sentence is grammatically correct?" → replace with image-based MCQ where applicable
- Dialogue: swap characters (Carlos/María → other lesson characters)
- Error spotter: different sentence types per lesson
- Vocab sort: add category sort (people / things / actions) as V2 variant

---

## 6. PART 2 — BONUS ROUND POLICY

- **ALL `a2` activities are `bonus: true`**
- Part 2 tab always shows `🎁 BONUS` label
- `NEXT STAGE →` unlocks when Part 1 ≥70% — bonus never blocks
- Gate modal fires on Part 1 pass only
- CHECK button reads `CHECK (BONUS)` on bonus acts
- Retry always available; never counts against progression

---

## 7. AUDIO SPECIFICATION

### TTS Generation (Piper local)

```python
# Female voice (María, all narration)
MODEL_F = "en_US-lessac-medium.onnx"
# Male voice (Carlos, interviewer dialogue)  
MODEL_M = "en_US-ryan-medium.onnx"

# Story settings (slow, clear)
VOICE_SETTINGS_STORY = {
    "stability": 0.60,
    "similarity_boost": 0.82,
    "style": 0.15,
    "use_speaker_boost": True
}

# Per-word pronunciation settings (very stable, clear)
VOICE_SETTINGS_WORD = {
    "stability": 0.70,
    "similarity_boost": 0.80
}
```

### Story text format (sentence-per-line with `...` pauses)
```
Hello. My name is [character]. [pause]
I work in [department]. [pause]
[Short sentences. One idea per line.]
```

### Default playback speeds
- Story audio: **0.5×** (default), 0.75×, 1× buttons
- Pronunciation words: **0.5×** (default), 0.75×, 1× buttons
- Speed applies immediately to live audio via `audio.playbackRate`
- Re-record button (`↺`) busts cache, re-fetches from ElevenLabs OR reloads local WAV

### Audio file naming convention
```
{lesson_id}_story_{character}.wav          # e.g. l01_story_maria.wav
{lesson_id}_word_{word}.wav               # e.g. l01_word_started.wav
{lesson_id}_ctx_{word}.wav                # e.g. l01_ctx_started.wav
{lesson_id}_dlg_{speaker}{n}.wav          # e.g. l01_dlg_carlos1.wav
```

### Embedding strategy
- All WAVs embedded as `data:audio/wav;base64,...` in a `const AUDIO = {}` object at top of script
- Playback: `new Audio(AUDIO['key'])` — no external requests
- ElevenLabs fallback: if `AUDIO[key]` undefined, call ElevenLabs API (online mode)

---

## 8. IMAGE ASSIGNMENT — ALL LESSONS

### Global images (reused across lessons)
| Key | File | Used in |
|---|---|---|
| `success` | GEN_A2_GLB_IMG_SUCCESS_01_V1.png | Gate modal (all lessons) |
| `highfive` | GEN_A2_GLB_IMG_SUCCESS_01_V1.png | Lesson complete screen |

### L01 — "I Started in HR Five Years Ago"
| Stage | Image file | Description |
|---|---|---|
| Landing hero | GEN_A2_L01_PPT_HERO_01_V1.png | HR office scene |
| V1A1 scene | GEN_A2_L01_IMG_SCENE_01_V2.png | Office observation |
| V1A2 story | GEN_A2_L01_IMG_MATCH_01_V2.png | María portrait |
| G1 discovery | GEN_A2_L01_IMG_LABEL_01_V1.png | Grammar scene |
| G5 listening | GEN_A2_L01_IMG_LABEL_01_V1.png | Listening scene |

### L02–L12 — Scene images
| Lesson | File |
|---|---|
| L02 | GEN_A2_L02_IMG_MATCH_01_V2.png |
| L03 | GEN_A2_L03_IMG_MATCH_01_V1.png |
| L04 | GEN_A2_L04_IMG_SCENE_0.png |
| L05 | GEN_A2_L05_IMG_SCENE_01_V1.png |
| L06 | GEN_A2_L06_IMG_SCENE_01_V1.png |
| L07 | EN_A2_L07_IMG_SCENE_01_V1.png |
| L08 | GEN_A2_L08_IMG_SCENE_01_V1.png |
| L09–L12 | Use general pool (see §9) |

### General image pool (assign by visual match to lesson topic)
| File | Visual content | Best for |
|---|---|---|
| Img-01 (two at desk charts) | Two people reviewing data dashboard | L07 data/reporting |
| Img-02 (woman in office) | HR professional standing in open office | L03/L08 characters |
| Img-03 (team highfive) | 4-person team celebrating | L06 teamwork/success |
| Img-04 (man with headphones) | Employee working at dual monitors | L04 IT/operations |
| Img-05 (email inbox phone) | Person holding phone with email inbox | L09 email/comms |
| Img-06 (graduation) | Woman in graduation gown | L01/L02 education |
| Img-07 (man reading doc) | Man reviewing documents at table | L05 compliance/legal |
| Img-08 (woman café phone) | Person on phone in casual setting | L10 informal comms |
| Img-09 (woman writing CVs) | Person writing with CVs on desk | L02 recruitment |
| Img-10 (man presenting HKO) | Person presenting HKO slide | L11 presentations |
| Img-11 (handshake business) | Two people shaking hands, exchanging cards | L03 networking |
| Img-12 (woman smiling office) | Young professional portrait | L01 María character |
| Img-13 (woman entering office) | Professional woman entering building | L01/L08 first day |
| Img-14 (woman outdoors) | Young professional outdoors | L10/L11 |
| Img-15 (tablet shortlist) | HR shortlist on tablet | L05/L06 selection |
| Img-16 (analytics tablet) | Recruitment analytics dashboard | L07 data |
| Img-17 (two women talking HKO) | HR interview/1:1 conversation | L03/L08 |
| Img-18 (stickies planning) | Team planning with sticky notes | L11/L12 |
| Img-19 (man signing tablet) | Professional signing document on tablet | L09 contracts |
| Img-20 (woman presenting HKO) | Female presenter with HKO chart | L07/L11 |

---

## 9. LESSON TOPIC MAP — A2 HR English

| Lesson | Title | Grammar focus | Vocabulary focus |
|---|---|---|---|
| L01 | "I Started in HR Five Years Ago" | Past Simple — Regular Verbs | Career history verbs |
| L02 | "We Received 200 Applications" | Past Simple — Irregular Verbs | Recruitment verbs |
| L03 | "She Has Worked Here for 3 Years" | Present Perfect — Have/Has + PP | Employment duration |
| L04 | "The Interview Will Be on Monday" | Future — Will / Going To | Interview scheduling |
| L05 | "If You Apply Now, We'll Review It" | First Conditional | Application process |
| L06 | "He Was Promoted Last Quarter" | Passive Voice — Was/Were + PP | HR processes |
| **Quiz 1** | Lessons 1–6 Review | All above | All above |
| L07 | "We Need Someone Who Can Lead" | Relative Clauses — Who/Which | Job requirements |
| L08 | "She Should Have Sent the Report" | Modal Perfect — Should Have | Workplace feedback |
| L09 | "Please Find Attached My CV" | Formal Email Language | Professional writing |
| L10 | "The Meeting Has Been Cancelled" | Passive — Has Been + PP | Office comms |
| L11 | "I'd Like to Discuss Your Performance" | Would Like To / Could You | Performance reviews |
| L12 | "We've Been Working on This for Months" | Present Perfect Continuous | Project language |
| **Quiz 2** | Lessons 7–12 Review | All above | All above |

---

## 10. QUIZ FORMAT (Quiz 1 after L06, Quiz 2 after L12)

### Structure
- 30 questions (5 per lesson covered)
- 3 activity types: MCQ (20q), Error Spot (6q), Gap Fill (4q)
- Timed: 30 minutes
- Pass: ≥70% = Certificate unlock
- SCORM reports: `cmi.core.lesson_status` = passed/failed

### Quiz HTML structure
Same chrome as lessons, but:
- No section tabs (single run-through)
- No Back button (forward only)
- Timer displayed in topbar
- Final score screen with certificate download link

---

## 11. RETRY / PROGRESSION RULES

| Situation | Behaviour |
|---|---|
| Part 1 score ≥70% | Gate fires, NEXT STAGE unlocks |
| Part 1 score <70% | Shake animation, Retry appears |
| Part 2 (bonus) any score | No gate, NEXT STAGE always available if P1 passed |
| RETRY clicked | All state cleared for current activity, fresh re-render |
| BACK clicked | Previous activity loaded, score NOT cleared |
| NEXT STAGE clicked | Stage++ , Act=0, loadActivity |
| Part 2 tab clicked | Free navigation, no gate |

---

## 12. SCORM 1.2 REPORTING

```javascript
api.LMSSetValue('cmi.core.lesson_status', pct >= 80 ? 'passed' : 'incomplete');
api.LMSSetValue('cmi.core.score.raw', String(XP));
api.LMSSetValue('cmi.core.score.min', '0');
api.LMSSetValue('cmi.core.score.max', '500');
// session time on beforeunload
```

---

## 13. FILE NAMING CONVENTION

```
GEN_A2_L01_COMPLETE.html     — Lesson 01 (canonical standard)
GEN_A2_L02_COMPLETE.html     — Lesson 02
...
GEN_A2_L12_COMPLETE.html     — Lesson 12
GEN_A2_QUIZ1_COMPLETE.html   — Quiz after L06
GEN_A2_QUIZ2_COMPLETE.html   — Quiz after L12

Audio files (embedded, not separate):
  l01_story_maria.wav
  l01_word_{word}.wav
  l01_ctx_{word}.wav
  l01_dlg_{speaker}{n}.wav

Images (embedded as base64 OR referenced via /assets/):
  GEN_A2_L01_IMG_SCENE_01_V2.png
  GEN_A2_L01_IMG_MATCH_01_V2.png
  etc.
```

---

## 14. LESSONS LEARNED — APPLIED TO STANDARD

| Issue found | Fix applied |
|---|---|
| Dark full-bleed backgrounds | All surfaces white/light, dark only in game canvas |
| Part 2 impossible to win | All Part 2 acts marked `bonus:true`, never block progression |
| Retry didn't clear state | `doRetry()` explicitly resets all module-level state vars |
| Part 2 tab locked | Removed gate from `goToAct()` |
| Progress bar invisible | 14px height, white fill on coloured topbar |
| HKO branding in lesson | Logo removed from lesson chrome (kept in Moodle shell) |
| Audio too fast for A2 | Default 0.5× playback, three speed buttons |
| Single-word pron only | Added `💬` context sentence button per chip |
| No Back button | `‹ BACK` in action bar, `doBack()` navigates correctly |
| No transcript for review | Collapsible transcript in V4A2 and story players |
| V4A2 showed `---` | Rewritten as complete natural sentences |
| Type-in not available | V3A1 split into memory game + type-in columns |
| Section dots tiny | Replaced with large Part 1 / Part 2 labelled tab buttons |
| Can-Do only in lesson | Added to landing page with ✓ badge icons |
| Speed 1.25× available | Removed, replaced with 0.5× as slowest option |
| Images missing from stages | All 14 stages now use uploaded images |
| Story one long blob | Rewritten sentence-per-line with `...` pause markers |

---

## 15. BUILD SEQUENCE

1. `GEN_A2_L01_COMPLETE.html` — Finalise from V3, embed audio + images
2. `HKO_A2_AUDIO_GEN.py` — Piper TTS script for all 12 lessons
3. `GEN_A2_L02_COMPLETE.html` through `L12` — Clone L01 shell, swap content arrays
4. `GEN_A2_QUIZ1_COMPLETE.html` — 30Q quiz, lessons 1–6
5. `GEN_A2_QUIZ2_COMPLETE.html` — 30Q quiz, lessons 7–12
6. SCORM package each file with `imsmanifest.xml`
7. Upload to Moodle CDO·HR course

---

*Manifest version 2.0 — April 2026 — HKO ESL Generator 2030*
