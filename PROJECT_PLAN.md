# Burton → Urdu Narration + Farsi Digressions: Project Plan

Goal: Build a repeatable, cost-conscious pipeline that converts a Burton “Arabian Nights” passage (English) into performable Urdu narration with embedded Persian digressions, plus TTS output and episode packaging.

Audience: Urdu speakers learning Farsi (bilingual storytelling, not classroom tone).

Operating stance (stealth + cost-conscious):
- Minimize paid API calls by caching intermediate artifacts and reusing prompts.
- Keep outputs modular to allow A/B testing and fast iteration with small passages first.
- Prefer open-source TTS (XTTSv2) during R&D; switch to paid engines only if quality requires.

---

## A) Roadmap (Phases)

1) **Foundation & Style Spec**
   - Define narration register, Burton vibe mapping, and oral pacing rules.
   - Decide on Persian digression density and rotation logic by difficulty.

2) **Prompt & Rewrite Pipeline**
   - Create LLM prompts for Urdu narration, Persian insertion, and QA passes.
   - Draft reusable prompt templates and parameterize episode metadata.

3) **Formatting & Digression Insertion**
   - Implement performance formatting (breath units, stage directions).
   - Insert Persian digressions with mode rotation and density guardrails.

4) **Packaging Outputs**
   - Generate clean text, SSML (or pause-marked text), phrase list, glossary, recap.
   - Assemble metadata and QA report.

5) **Audio & QA**
   - Run TTS with optional cadence reference.
   - Validate metrics and quality gates; iterate.

6) **Scale Plan (10 Episodes)**
   - Define incremental Persian density and teaching progression.
   - Establish batch workflow and cost controls.

---

## B) Task Table

| Task ID | Title | Description | Inputs | Outputs | Acceptance Criteria | Dependencies |
|---|---|---|---|---|---|---|
| T1 | Define episode style spec | Define Urdu register, Burton vibe, oral pacing, stage directions, and glossary tone. | style assumptions; sample Burton passage | Style spec doc | Spec covers pacing rules, register choices, and stage direction tokens; approved by narrator lead. | None |
| T2 | Create translation + rewriting prompts | Draft LLM prompts for Urdu narration + tone, and for Farsi digressions, plus glossary/recap prompts. | style spec, audience profile, difficulty | Prompt templates | Prompts are parameterized; produce consistent output with no violations on 2 sample passages. | T1 |
| T3 | Build performance formatting step | Define breath units, pause markers, and line breaks; create converter from clean text to performable script. | Urdu narration draft | performance script | Performance output has short breath units; no run-on lines > 15–20 words. | T2 |
| T4 | Build Persian digression inserter | Insert digressions using Mode A/B/C rotation, density limits, glossing rules. | Urdu narration draft, difficulty, density rules | Urdu narration with digressions | No more than 5 insertions per 500 Urdu words (early episodes); modes rotate without repeats; gloss applied per difficulty. | T2 |
| T5 | Generate phrase list + glossary + recap | Extract Farsi phrases; create glossary of 10–20 hard terms; write recap (≤5 phrases). | digressed narration | CSV + glossary + recap | Phrase list matches inserts; glossary has 10–20 items; recap ≤5 phrases. | T4 |
| T6 | Generate SSML or pause-marked text | Build SSML when engine supports; fallback plain text with pause markers. | performance script, TTS engine | SSML or pause-marked text | Valid XML if SSML; fallback includes pause tokens; aligns with narration. | T3 |
| T7 | Generate TTS audio | Run TTS engine with optional cadence reference; output audio file. | SSML or pause-marked text; cadence ref | audio output | Audio generated; sample passes clarity and cadence check. | T6 |
| T8 | Run QA checks | Compute metrics: word counts, Farsi density, mode sequence, readability flags, overlap rates. | narration + phrase list + recap | QA report + meta.json | All metrics computed; violations listed with fixes; gates passed or flagged. | T4, T5 |
| T9 | Package outputs + metadata JSON | Consolidate outputs into structured folder, include provenance. | all prior outputs | final files set | All required files present; metadata includes required metrics. | T5, T6, T7, T8 |
| T10 | Create scale plan for 10 episodes | Define progression of Persian density, difficulty, and recap format. | metrics baseline + episode specs | scale plan | Clear progression across 10 episodes; no density spikes; cost plan included. | T1, T8 |

---

## C) Next Actions Checklist for Episode 1 (E01)

1) **Confirm Style Spec**
   - Draft 1-page style spec with: register, Burton vibe mapping, oral cadence rules.
2) **Run Base Urdu Narration Prompt**
   - Translate + adapt passage to oral Urdu (no Persian yet).
3) **Insert Persian Digressions (Beginner Mode)**
   - Apply Mode rotation: A → B → C; max 5 per 500 words; gloss immediately.
4) **Format for Performance**
   - Insert line breaks for breath; add stage directions (e.g., [وقفہ], [آہستہ]).
5) **Generate Phrase List + Glossary + Recap**
   - Extract phrases, add transliteration in CSV only; glossary 10–20 terms.
6) **Build SSML or Pause-Marked Text**
   - If engine supports SSML, generate; else add pause markers.
7) **Run TTS**
   - Use XTTSv2 for cost control; apply cadence reference if provided.
8) **QA Gate**
   - Compute metrics and verify density, mode rotation, readability.
9) **Package Files**
   - Save outputs to output_dir with E01 naming convention.

---

## D) Future Automation (CLI + Batch Generation)

### CLI design (minimal, cost-conscious)
Command:
```
burton2urdu \
  --episode-id E01 \
  --input english.txt \
  --difficulty Beginner \
  --tts-engine XTTSv2 \
  --cadence-ref optional.wav \
  --output-dir outputs/
```

### Pipeline modules
1) `ingest`: validate input, sanitize text.
2) `rewrite`: run Urdu narration prompt.
3) `digress`: insert Persian digressions with mode rotation.
4) `format`: generate performance script.
5) `pack`: generate clean text, SSML/pause, phrase list, glossary, recap.
6) `qa`: compute metrics + QA report.
7) `tts`: optional audio generation.

### Batch runner
```
burton2urdu batch --episodes spec.json --output-dir outputs/
```

### Cost controls
- Cache all LLM outputs by episode + prompt hash.
- Use a “dry-run” mode to output only text for review.
- Run TTS only after QA gates pass.

---

## Quality Gates (must pass before shipping)

1) **Density Gate**: max 5 Persian insertions per 500 Urdu words for early episodes.
2) **Mode Rotation Gate**: no immediate repetition of A/B/C.
3) **Glossing Gate**: Beginner = immediate gloss; Intermediate = echo; Advanced = delayed gloss by 1–2 sentences.
4) **Oral Readability Gate**: no line > 20 words; flag tongue-twisters.
5) **Recap Overlap Gate**: recap phrases overlap with phrase list but do not exceed 5 items.
6) **Copyright Gate**: no long verbatim blocks; only modest excerpts.

---

## Suggestions & Augmentations (for a stealthy, cost-conscious startup)

- **Pilot with 3-minute episodes** to validate cadence and listener retention.
- **Use a fixed narrator voice** for brand continuity; avoid frequent voice swaps.
- **A/B test Persian density** on small cohorts; track retention vs. comprehension.
- **Set up a “storyteller review pass”** to keep performance natural.
- **Add a fallback “no-digression” mode** for users who want pure Urdu narrative.

