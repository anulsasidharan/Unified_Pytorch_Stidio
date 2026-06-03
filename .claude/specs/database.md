# Database Schema — PyTorch Learning Studio

*Extracted from `.claude/rules/CLAUDE.md` §5 Database Schema*

PostgreSQL 16 with UUID primary keys for users (`gen_random_uuid()`). SQLAlchemy models should mirror these tables; Alembic manages migrations.

---

## Entity relationship (summary)

```text
users ──┬── user_attempts ── questions ── topics
        ├── user_progress ── topics
        ├── daily_activity
        ├── revision_queue ── questions
        ├── user_notes ── questions / topics
        └── custom_questions ── topics

questions ── test_cases
questions ── solutions
```

---

## Tables (11 core)

### `users`

Identity, PyTorch level, daily goal, streaks, XP.

| Column | Notes |
|--------|--------|
| `pytorch_level` | `beginner` \| `intermediate` \| `advanced` |
| `daily_goal` | Default 5 exercises/day |
| `streak_count`, `longest_streak` | Gamification |
| `total_xp` | Cumulative XP |
| `last_active_date` | For streak calculation |

### `topics`

13 PyTorch modules with display order and module number.

| Column | Notes |
|--------|--------|
| `module_number` | 1–13 |
| `order_index` | Display order |
| `icon`, `color` | UI metadata |
| `total_questions` | Denormalized count |

### `questions`

Core exercise bank with PyTorch-specific fields.

| Column | Notes |
|--------|--------|
| `question_type` | `code_completion` \| `debug_model` \| `conceptual_mcq` \| `build_from_scratch` \| `notebook_challenge` \| `shape_assertion` |
| `starter_code` | Boilerplate for Monaco editor |
| `expected_output` | Expected printed output or shape string |
| `expected_output_shape` | e.g. `"(32, 10)"` for tensor shape validation |
| `pytorch_version` | Default `2.x` |
| `gpu_required` | Boolean; Colab fallback for GPU exercises |
| `colab_link` | Google Colab notebook URL |
| `tags` | TEXT[] array |
| `xp_reward` | Default 10; overridden by difficulty |
| `time_estimate_mins` | Default 15 |
| `source` | `internal` \| `imported` \| `user` |

### `test_cases`

Per question; JSONB input/output for tensor data.

| Column | Notes |
|--------|--------|
| `input_data` | JSONB: `{"x": [[1,2]], "shape": [2,2]}` |
| `expected_output` | JSONB: `{"shape": [2,2], "dtype": "float32"}` |
| `is_hidden` | Hidden test cases not shown to user |

### `solutions`

Multiple per question; Python code with explanation.

| Column | Notes |
|--------|--------|
| `code` | Python solution |
| `explanation` | Markdown explanation |
| `is_optimal` | Mark best solution |

### `user_attempts`

Each submission with PyTorch-specific result tracking.

**Result enum:** `correct`, `incorrect`, `partial`, `skipped`

| Column | Notes |
|--------|--------|
| `submitted_code` | User's Python code |
| `hints_used` | Count for XP penalty (−2 each) |
| `time_spent_secs` | Time on exercise |
| `error_message` | Runtime/shape error captured |

### `user_progress`

One row per user+topic (module-level aggregation).

| Column | Notes |
|--------|--------|
| `basic_solved`, `intermediate_solved`, `advanced_solved` | Counts by difficulty |
| `completion_pct` | Percentage of module exercises solved |

### `daily_activity`

One row per user per `activity_date`.

| Column | Notes |
|--------|--------|
| `exercises_done`, `exercises_correct` | Daily counts |
| `xp_earned` | XP for the day |
| `modules_touched` | TEXT[] of module slugs |
| `goal_met` | `exercises_done >= daily_goal` |

### `revision_queue`

SM-2 spaced repetition scheduling.

| Column | Notes |
|--------|--------|
| `ease_factor` | SM-2 ease factor (default 2.5) |
| `interval_days` | Current interval in days |
| `repetition_count` | Times successfully reviewed |
| `next_review_date` | When due for review |
| `last_result` | Last review rating outcome |

### `user_notes`

Free-text notes per question or topic.

| Column | Notes |
|--------|--------|
| `note_type` | `personal` \| `insight` \| `gotcha` |
| `tags` | TEXT[] array |

### `custom_questions`

User-imported exercises with community sharing.

| Column | Notes |
|--------|--------|
| `is_shared` | Share with community |
| `import_source` | Origin (csv, json, notebook, manual) |
| `colab_link` | Optional Colab URL |

---

## Indexing recommendations

| Table | Index |
|-------|--------|
| `questions` | `(topic_id, difficulty)`, GIN on `tags` |
| `user_progress` | `(user_id, topic_id)` UNIQUE |
| `user_attempts` | `(user_id, question_id)`, `(user_id, attempted_at DESC)` |
| `revision_queue` | `(user_id, next_review_date)` |
| `daily_activity` | `(user_id, activity_date DESC)` UNIQUE |

---

## Migration policy

- Backward-compatible Alembic migrations only on main branch  
- Seed data: idempotent scripts in `backend/seeds/`  
- Soft-delete questions via `is_published` rather than hard delete when attempts exist  

---

## Full DDL reference

Canonical SQL definitions: **`.claude/rules/CLAUDE.md` §5 Database Schema** (sections 5.1–5.11).
