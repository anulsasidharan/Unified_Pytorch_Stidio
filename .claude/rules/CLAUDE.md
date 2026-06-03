# PyTorch Learning Studio — CLAUDE.md

> **Architecture Origin**: Forked and adapted from Unified DSA Studio.  
> All backend infrastructure, spaced repetition engine, daily tracker, auth, and DB patterns are reused.  
> Domain content, topic taxonomy, question schema extensions, and AI tutor persona are PyTorch-specific.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Technology Stack](#3-technology-stack)
4. [Project Directory Structure](#4-project-directory-structure)
5. [Database Schema](#5-database-schema)
6. [Topic Hierarchy](#6-topic-hierarchy)
7. [Feature Specifications](#7-feature-specifications)
8. [REST API Endpoints](#8-rest-api-endpoints)
9. [AI Tutor — System Prompt & Configuration](#9-ai-tutor--system-prompt--configuration)
10. [Question Format Specification](#10-question-format-specification)
11. [UI Wireframes & Page Specs](#11-ui-wireframes--page-specs)
12. [Spaced Repetition Engine](#12-spaced-repetition-engine)
13. [Daily Tracker & Analytics](#13-daily-tracker--analytics)
14. [Notebook Integration (Colab / Jupyter)](#14-notebook-integration-colab--jupyter)
15. [External Question Import](#15-external-question-import)
16. [Implementation Roadmap](#16-implementation-roadmap)
17. [Environment Variables](#17-environment-variables)
18. [Development Commands](#18-development-commands)
19. [Future Enhancements (V2 / V3)](#19-future-enhancements-v2--v3)

---

## 1. Project Overview

**PyTorch Learning Studio** is a full-stack, AI-powered interactive learning platform for mastering PyTorch from foundational tensor operations to production model deployment. It mirrors the pedagogical structure of Unified DSA Studio — topic taxonomy, three-tier difficulty, spaced repetition, daily streaks, external import, and AI chatbot — but is fully domain-adapted for deep learning practitioners.

### Goals

- Provide structured PyTorch exercises across 13 modules × 3 difficulty levels
- Store all exercises, solutions, and user progress in a persistent PostgreSQL database
- Support runnable Colab notebook challenges embedded inside exercises
- Surface a PyTorch-expert AI tutor that debugs code, explains autograd, and reviews model architectures
- Track daily learning via streaks, heatmaps, and spaced repetition scheduling
- Allow users to import custom exercises (manual, CSV, JSON, notebook URL)

### Target Users

- ML engineers transitioning from TensorFlow or NumPy
- Data scientists learning deep learning fundamentals
- Students working through fast.ai, deeplearning.ai, or university courses
- Engineers preparing for ML engineering interviews

### Key Differentiators vs Generic Courses

| Feature | Generic Platforms | PyTorch Learning Studio |
|---|---|---|
| Exercise persistence & revision | ❌ | ✅ PostgreSQL-backed |
| Custom question import | ❌ | ✅ CSV / JSON / Notebook URL |
| Spaced repetition scheduling | ❌ | ✅ SM-2 algorithm |
| Colab notebook integration | ❌ | ✅ One-click launch |
| AI tutor with code debugging | Limited | ✅ PyTorch-specialist prompt |
| Daily tracker & streak | ❌ | ✅ GitHub-style heatmap |
| Shape / dtype assertion validation | ❌ | ✅ Built-in |

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│  Next.js 14 (App Router) + TypeScript + Tailwind CSS           │
│  Monaco Editor │ MathJax │ Recharts │ react-codemirror          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS / REST
┌──────────────────────────▼──────────────────────────────────────┐
│                         API LAYER                               │
│  FastAPI (Python 3.11) + Uvicorn + Pydantic v2                  │
│  JWT Auth │ Rate Limiting │ Background Tasks (Celery)            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼───────┐  ┌──────▼────────────┐
│  PostgreSQL  │  │     Redis      │  │  Anthropic API    │
│  (Primary DB)│  │ (Cache/Sessions│  │  claude-sonnet-4  │
│              │  │  Celery Broker)│  │  AI Tutor         │
└──────────────┘  └────────────────┘  └───────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│  Google Colab API │ nbviewer │ GitHub Gists │ AWS S3 (assets)   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. User authenticates → JWT issued, stored in Redis
2. User selects module → frontend fetches topic + question list from FastAPI
3. User submits code answer → stored in `user_attempts`; spaced repetition queue updated
4. Colab launch → backend generates signed notebook URL → redirects to Colab
5. AI Tutor request → FastAPI proxies to Anthropic API with PyTorch system prompt
6. Daily tracker → Celery cron aggregates activity into `daily_activity` table nightly

---

## 3. Technology Stack

### Frontend

| Technology | Version | Purpose |
|---|---|---|
| Next.js | 14.x (App Router) | Framework |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 3.x | Styling |
| shadcn/ui | latest | Component library |
| Monaco Editor | 0.44.x | Code editor with Python syntax |
| Recharts | 2.x | Analytics charts |
| MathJax | 3.x | LaTeX math rendering |
| react-syntax-highlighter | 15.x | Solution display |
| Zustand | 4.x | Client state management |

### Backend

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Runtime |
| FastAPI | 0.111.x | API framework |
| SQLAlchemy | 2.x | ORM |
| Alembic | 1.13.x | DB migrations |
| Pydantic | v2 | Data validation |
| Celery | 5.x | Background tasks & cron |
| python-jose | 3.x | JWT tokens |
| passlib | 1.7.x | Password hashing |
| httpx | 0.27.x | Async HTTP (Anthropic, Colab) |
| uv | latest | Package manager (preferred) |

### Infrastructure

| Technology | Purpose |
|---|---|
| PostgreSQL 16 | Primary database |
| Redis 7 | Cache, sessions, Celery broker |
| Docker Compose | Local development |
| AWS ECS Fargate | Production deployment |
| AWS S3 | Notebook assets, uploads |
| CloudFront | CDN for static assets |
| GitHub Actions | CI/CD pipeline |

---

## 4. Project Directory Structure

```
pytorch-learning-studio/
├── .claude/
│   ├── CLAUDE.md              # This file (authoritative spec)
│   ├── MEMORY.md              # Runtime memory for Claude Code
│   ├── PLAN.md                # Active sprint plan
│   └── TASKS.md               # Current task checklist
│
├── frontend/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── dashboard/page.tsx
│   │   ├── modules/
│   │   │   ├── page.tsx                  # Module browser
│   │   │   └── [slug]/
│   │   │       ├── page.tsx              # Module overview
│   │   │       └── [questionId]/page.tsx # Exercise page
│   │   ├── tracker/page.tsx              # Daily tracker
│   │   ├── revision/page.tsx             # Spaced repetition queue
│   │   ├── import/page.tsx               # External import
│   │   ├── tutor/page.tsx                # AI tutor chat
│   │   └── profile/page.tsx
│   ├── components/
│   │   ├── editor/
│   │   │   ├── CodeEditor.tsx            # Monaco with PyTorch snippets
│   │   │   ├── OutputPanel.tsx
│   │   │   └── ShapeValidator.tsx        # Tensor shape checker
│   │   ├── question/
│   │   │   ├── QuestionCard.tsx
│   │   │   ├── SolutionViewer.tsx
│   │   │   ├── HintDrawer.tsx
│   │   │   ├── ColabLauncher.tsx
│   │   │   └── DifficultyBadge.tsx
│   │   ├── tracker/
│   │   │   ├── StreakCounter.tsx
│   │   │   ├── HeatmapCalendar.tsx
│   │   │   ├── ProgressRing.tsx
│   │   │   └── WeeklyChart.tsx
│   │   ├── tutor/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── CodeSuggestion.tsx
│   │   └── ui/                           # shadcn components
│   ├── lib/
│   │   ├── api.ts                        # API client
│   │   ├── auth.ts
│   │   └── utils.ts
│   └── store/
│       ├── useUserStore.ts
│       ├── useProgressStore.ts
│       └── useTutorStore.ts
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── topic.py
│   │   │   ├── question.py
│   │   │   ├── attempt.py
│   │   │   ├── progress.py
│   │   │   ├── revision.py
│   │   │   └── daily_activity.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── topics.py
│   │   │   ├── questions.py
│   │   │   ├── attempts.py
│   │   │   ├── progress.py
│   │   │   ├── tracker.py
│   │   │   ├── revision.py
│   │   │   ├── import_.py
│   │   │   ├── tutor.py
│   │   │   └── colab.py
│   │   ├── services/
│   │   │   ├── spaced_repetition.py      # SM-2 algorithm
│   │   │   ├── tutor_service.py          # Anthropic API wrapper
│   │   │   ├── colab_service.py          # Colab URL generation
│   │   │   ├── import_service.py         # CSV/JSON/URL import
│   │   │   └── analytics_service.py      # Tracker aggregations
│   │   └── tasks/
│   │       ├── celery_app.py
│   │       ├── nightly_aggregation.py    # Daily activity cron
│   │       └── revision_scheduler.py    # SR queue refresh
│   ├── alembic/
│   │   └── versions/
│   ├── seeds/
│   │   ├── topics.py                     # 13 PyTorch modules seed
│   │   ├── questions_tensors.py
│   │   ├── questions_autograd.py
│   │   ├── questions_nn_module.py
│   │   └── ... (one file per module)
│   └── tests/
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── README.md
```

---

## 5. Database Schema

### 5.1 `users`

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    username        VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255),
    avatar_url      VARCHAR(500),
    pytorch_level   VARCHAR(20) DEFAULT 'beginner',  -- beginner|intermediate|advanced
    daily_goal      INTEGER DEFAULT 5,               -- exercises per day
    streak_count    INTEGER DEFAULT 0,
    longest_streak  INTEGER DEFAULT 0,
    last_active_date DATE,
    total_xp        INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.2 `topics`

```sql
CREATE TABLE topics (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    description     TEXT,
    icon            VARCHAR(100),               -- emoji or icon name
    color           VARCHAR(20),                -- hex color for UI
    order_index     INTEGER NOT NULL,           -- display order
    module_number   INTEGER NOT NULL,           -- 1–13
    total_questions INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.3 `questions`

```sql
CREATE TABLE questions (
    id                    SERIAL PRIMARY KEY,
    topic_id              INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    title                 VARCHAR(500) NOT NULL,
    slug                  VARCHAR(500) UNIQUE NOT NULL,
    difficulty            VARCHAR(20) NOT NULL CHECK (difficulty IN ('basic', 'intermediate', 'advanced')),
    question_type         VARCHAR(50) NOT NULL,
    -- question_type options:
    -- code_completion    | fill in missing PyTorch code
    -- debug_model        | find and fix tensor/model bug
    -- conceptual_mcq     | multiple choice theory question
    -- build_from_scratch | implement a full component
    -- notebook_challenge | runnable Colab exercise
    -- shape_assertion    | predict output tensor shape
    problem_statement     TEXT NOT NULL,
    constraints           TEXT,                -- e.g., "Use only torch.nn.functional"
    starter_code          TEXT,                -- boilerplate code for editor
    expected_output       TEXT,               -- expected printed output or shape
    expected_output_shape VARCHAR(200),       -- e.g., "(32, 10)" for tensor shape
    pytorch_version       VARCHAR(20) DEFAULT '2.x',
    gpu_required          BOOLEAN DEFAULT FALSE,
    colab_link            VARCHAR(1000),       -- Google Colab notebook URL
    tags                  TEXT[],              -- e.g., ['autograd', 'backprop', 'loss']
    xp_reward             INTEGER DEFAULT 10,  -- XP points on completion
    time_estimate_mins    INTEGER DEFAULT 15,
    is_published          BOOLEAN DEFAULT TRUE,
    source                VARCHAR(100) DEFAULT 'internal',  -- internal|imported|user
    source_url            VARCHAR(500),
    created_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_questions_topic_difficulty ON questions(topic_id, difficulty);
CREATE INDEX idx_questions_tags ON questions USING GIN(tags);
```

### 5.4 `solutions`

```sql
CREATE TABLE solutions (
    id              SERIAL PRIMARY KEY,
    question_id     INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    title           VARCHAR(200) NOT NULL,    -- e.g., "Clean Solution", "Memory-Efficient"
    code            TEXT NOT NULL,
    language        VARCHAR(20) DEFAULT 'python',
    explanation     TEXT,
    time_complexity VARCHAR(100),
    space_complexity VARCHAR(100),
    is_optimal      BOOLEAN DEFAULT FALSE,
    order_index     INTEGER DEFAULT 1,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.5 `test_cases`

```sql
CREATE TABLE test_cases (
    id              SERIAL PRIMARY KEY,
    question_id     INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    input_data      JSONB NOT NULL,           -- {"x": [[1,2],[3,4]], "shape": [2,2]}
    expected_output JSONB NOT NULL,           -- {"shape": [2,2], "dtype": "float32"}
    explanation     TEXT,
    is_hidden       BOOLEAN DEFAULT FALSE,    -- hidden test cases not shown to user
    order_index     INTEGER DEFAULT 1
);
```

### 5.6 `user_attempts`

```sql
CREATE TABLE user_attempts (
    id              SERIAL PRIMARY KEY,
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id     INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    submitted_code  TEXT,
    result          VARCHAR(20) CHECK (result IN ('correct', 'incorrect', 'partial', 'skipped')),
    runtime_ms      INTEGER,
    error_message   TEXT,
    hints_used      INTEGER DEFAULT 0,
    time_spent_secs INTEGER DEFAULT 0,
    attempt_number  INTEGER DEFAULT 1,
    attempted_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_attempts_user_question ON user_attempts(user_id, question_id);
CREATE INDEX idx_attempts_user_date ON user_attempts(user_id, attempted_at);
```

### 5.7 `user_progress`

```sql
CREATE TABLE user_progress (
    id                   SERIAL PRIMARY KEY,
    user_id              UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id             INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    questions_attempted  INTEGER DEFAULT 0,
    questions_solved     INTEGER DEFAULT 0,
    basic_solved         INTEGER DEFAULT 0,
    intermediate_solved  INTEGER DEFAULT 0,
    advanced_solved      INTEGER DEFAULT 0,
    total_time_spent_secs INTEGER DEFAULT 0,
    completion_pct       DECIMAL(5,2) DEFAULT 0.00,
    last_attempted_at    TIMESTAMP WITH TIME ZONE,
    UNIQUE (user_id, topic_id)
);
```

### 5.8 `daily_activity`

```sql
CREATE TABLE daily_activity (
    id               SERIAL PRIMARY KEY,
    user_id          UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_date    DATE NOT NULL,
    exercises_done   INTEGER DEFAULT 0,
    exercises_correct INTEGER DEFAULT 0,
    time_spent_secs  INTEGER DEFAULT 0,
    xp_earned        INTEGER DEFAULT 0,
    modules_touched  TEXT[],                  -- slugs of modules worked on
    streak_day       INTEGER DEFAULT 0,
    goal_met         BOOLEAN DEFAULT FALSE,
    UNIQUE (user_id, activity_date)
);

CREATE INDEX idx_daily_activity_user_date ON daily_activity(user_id, activity_date DESC);
```

### 5.9 `revision_queue`

```sql
CREATE TABLE revision_queue (
    id                   SERIAL PRIMARY KEY,
    user_id              UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id          INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    ease_factor          DECIMAL(4,2) DEFAULT 2.5,  -- SM-2 ease factor
    interval_days        INTEGER DEFAULT 1,
    repetition_count     INTEGER DEFAULT 0,
    next_review_date     DATE NOT NULL,
    last_reviewed_at     TIMESTAMP WITH TIME ZONE,
    last_result          VARCHAR(20),
    UNIQUE (user_id, question_id)
);

CREATE INDEX idx_revision_due ON revision_queue(user_id, next_review_date);
```

### 5.10 `user_notes`

```sql
CREATE TABLE user_notes (
    id              SERIAL PRIMARY KEY,
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id     INTEGER REFERENCES questions(id),
    topic_id        INTEGER REFERENCES topics(id),
    content         TEXT NOT NULL,
    note_type       VARCHAR(20) DEFAULT 'personal',  -- personal|insight|gotcha
    tags            TEXT[],
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.11 `custom_questions`

```sql
CREATE TABLE custom_questions (
    id              SERIAL PRIMARY KEY,
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id        INTEGER REFERENCES topics(id),
    title           VARCHAR(500) NOT NULL,
    difficulty      VARCHAR(20),
    problem_statement TEXT NOT NULL,
    solution_code   TEXT,
    colab_link      VARCHAR(1000),
    tags            TEXT[],
    is_shared       BOOLEAN DEFAULT FALSE,   -- share with community
    import_source   VARCHAR(200),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 6. Topic Hierarchy

PyTorch Learning Studio contains **13 modules**, each with Basic, Intermediate, and Advanced sub-tracks.  
Target: **500–650 total exercises** across all modules.

```
Module 01 — Tensors & Operations           (40 exercises)
Module 02 — Autograd & Backpropagation     (45 exercises)
Module 03 — Neural Network Basics          (50 exercises)
Module 04 — Training Loops & Optimization  (45 exercises)
Module 05 — Loss Functions & Metrics       (35 exercises)
Module 06 — Datasets & DataLoaders         (40 exercises)
Module 07 — CNNs & Computer Vision         (55 exercises)
Module 08 — RNNs, LSTMs & Sequences        (50 exercises)
Module 09 — Transformers & Attention       (55 exercises)
Module 10 — Transfer Learning & Fine-tuning(40 exercises)
Module 11 — Model Saving & Deployment      (35 exercises)
Module 12 — GPU / CUDA & Performance       (35 exercises)
Module 13 — PyTorch Lightning & Best Practices (35 exercises)
```

### Detailed Subtopics per Module

#### Module 01 — Tensors & Operations

| Level | Subtopics |
|---|---|
| Basic | Creating tensors (zeros, ones, rand, arange), tensor dtype & device, indexing & slicing, reshaping (view, reshape, squeeze, unsqueeze) |
| Intermediate | Broadcasting rules, in-place operations, tensor math (matmul, einsum), cloning vs views, contiguous memory |
| Advanced | Custom CUDA kernels via torch.utils.cpp_extension, memory layout optimization, sparse tensors, quantized tensors |

#### Module 02 — Autograd & Backpropagation

| Level | Subtopics |
|---|---|
| Basic | requires_grad, .backward(), .grad attribute, computation graph concept |
| Intermediate | grad_fn chains, detach(), no_grad context, gradient accumulation |
| Advanced | Custom autograd Functions (forward/backward), higher-order gradients, gradient checkpointing, hooks |

#### Module 03 — Neural Network Basics

| Level | Subtopics |
|---|---|
| Basic | nn.Module subclassing, __init__ & forward(), Linear layers, activation functions |
| Intermediate | Sequential containers, ModuleList/ModuleDict, parameter vs buffer, weight initialization |
| Advanced | Custom layers, parameter sharing, model surgery, dynamic computation graphs |

#### Module 04 — Training Loops & Optimization

| Level | Subtopics |
|---|---|
| Basic | Zero grad → forward → loss → backward → step pattern, SGD, Adam |
| Intermediate | Learning rate schedulers, gradient clipping, mixed precision (autocast, GradScaler) |
| Advanced | Custom optimizers, lookahead, SAM, learning rate finding, optimizer state management |

#### Module 05 — Loss Functions & Metrics

| Level | Subtopics |
|---|---|
| Basic | MSELoss, CrossEntropyLoss, BCELoss, NLLLoss |
| Intermediate | Custom loss functions, focal loss, label smoothing, multi-task loss weighting |
| Advanced | Contrastive loss, triplet loss, perceptual loss, differentiable metrics |

#### Module 06 — Datasets & DataLoaders

| Level | Subtopics |
|---|---|
| Basic | Dataset class (__len__, __getitem__), DataLoader, batch_size, shuffle |
| Intermediate | Custom collate_fn, weighted sampler, transforms pipeline (torchvision), num_workers |
| Advanced | IterableDataset, WebDataset, memory-mapped datasets, distributed sampler |

#### Module 07 — CNNs & Computer Vision

| Level | Subtopics |
|---|---|
| Basic | Conv2d, MaxPool2d, BatchNorm2d, building LeNet/AlexNet |
| Intermediate | ResNet skip connections, depthwise separable convolutions, feature map visualization |
| Advanced | U-Net, FPN, dilated convolutions, deformable convolutions, ViT patch embedding |

#### Module 08 — RNNs, LSTMs & Sequences

| Level | Subtopics |
|---|---|
| Basic | RNN cell, nn.RNN, sequence packing with pack_padded_sequence |
| Intermediate | LSTM, GRU, bidirectional RNNs, hidden state management |
| Advanced | Seq2Seq with attention, CTC loss, TCN, WaveNet-style architectures |

#### Module 09 — Transformers & Attention

| Level | Subtopics |
|---|---|
| Basic | Scaled dot-product attention, MultiheadAttention, positional encoding |
| Intermediate | Transformer encoder/decoder blocks, causal masking, padding mask |
| Advanced | Flash attention, grouped query attention, RoPE, KV-cache implementation |

#### Module 10 — Transfer Learning & Fine-tuning

| Level | Subtopics |
|---|---|
| Basic | Loading pretrained models (torchvision.models), freezing layers, replacing head |
| Intermediate | Layer-wise learning rates, feature extraction vs full fine-tuning |
| Advanced | LoRA, QLoRA, PEFT adapters, knowledge distillation |

#### Module 11 — Model Saving & Deployment

| Level | Subtopics |
|---|---|
| Basic | state_dict save/load, full model save, checkpoint resume |
| Intermediate | TorchScript (trace vs script), ONNX export, model versioning |
| Advanced | TensorRT optimization, torch.compile, mobile deployment (torchscript mobile) |

#### Module 12 — GPU / CUDA & Performance

| Level | Subtopics |
|---|---|
| Basic | .to(device), torch.cuda.is_available(), memory management basics |
| Intermediate | Profiling (torch.profiler), memory pinning, async data loading |
| Advanced | Multi-GPU (DataParallel, DistributedDataParallel), FSDP, gradient checkpointing |

#### Module 13 — PyTorch Lightning & Best Practices

| Level | Subtopics |
|---|---|
| Basic | LightningModule, training_step, Trainer, callbacks |
| Intermediate | LightningDataModule, logging (TensorBoard, W&B), checkpointing |
| Advanced | Custom strategies, fabric API, production-grade experiment management |

---

## 7. Feature Specifications

### Feature 1: Module & Exercise Browser

**Description**: Main learning interface displaying the 13 PyTorch modules, each expandable to show subtopics and exercises organized by difficulty.

**Acceptance Criteria**:
- Module grid shows name, icon, progress ring (% completed), and question count
- Clicking a module shows exercise list filterable by: difficulty, type, GPU required, completed/not completed
- Each exercise card shows: title, difficulty badge, type badge, XP reward, estimated time, Colab indicator
- Users can bookmark exercises for later
- Search bar filters exercises by title, tags, or keywords

**UI Components**:
```
/modules
├── ModuleGrid (13 cards with progress rings)
└── /modules/[slug]
    ├── ModuleHeader (name, description, your progress)
    ├── DifficultyTabs (All | Basic | Intermediate | Advanced)
    ├── FilterBar (type, GPU, completed)
    └── ExerciseList (cards with metadata)
```

---

### Feature 2: Exercise Page & Code Editor

**Description**: Full-screen exercise environment with problem statement, Monaco code editor, hints, solution viewer, and Colab launcher.

**Acceptance Criteria**:
- Problem statement rendered with Markdown + MathJax support
- Monaco editor pre-loaded with starter code and Python syntax highlighting
- PyTorch-specific autocomplete snippets (e.g., `nn.Linear`, `F.relu`)
- Hint system: hints revealed one at a time (each hint costs −2 XP)
- "Check Shape" button: validates expected_output_shape against user's code output
- Solution drawer shows optimal solution with explanation (locked until 1 attempt made)
- "Open in Colab" button launches colab_link in new tab (or generates one if blank)
- After correct submission: shows XP earned, adds to revision queue, suggests next exercise

**Exercise Types handled**:

| Type | Editor Behavior |
|---|---|
| `code_completion` | Pre-filled code with `# YOUR CODE HERE` gaps |
| `debug_model` | Pre-filled buggy code, user must identify and fix |
| `conceptual_mcq` | Multiple choice radio buttons, no code editor |
| `build_from_scratch` | Empty editor with imports only |
| `notebook_challenge` | Description + Colab launch button, no local editor |
| `shape_assertion` | Code editor + expected shape input field |

---

### Feature 3: AI Tutor (PyTorch Expert)

**Description**: Conversational AI assistant powered by Anthropic claude-sonnet-4, specialized in PyTorch debugging, conceptual explanations, and architecture reviews.

**Capabilities**:
- Debug runtime errors (shape mismatches, device mismatches, NaN loss)
- Explain autograd computation graphs
- Compare architectural choices (LSTM vs Transformer for task X)
- Review user-submitted model code and suggest improvements
- Explain paper implementations in PyTorch
- Generate minimal reproducible examples (MREs)

**Context injection**: When user opens tutor from an exercise page, the current question + user's submitted code is auto-injected as context.

**Rate limiting**: 20 tutor messages per day (free tier), unlimited (pro tier).

See Section 9 for full system prompt.

---

### Feature 4: Daily Tracker & Analytics Dashboard

**Description**: Tracks all learning activity, visualizes progress, and enforces daily goals.

**Dashboard Components**:

1. **Today's Summary Card** — exercises done / goal, XP earned today, time spent
2. **Streak Banner** — current streak 🔥, best streak, last active date
3. **Heatmap Calendar** — GitHub-style 52-week grid, color intensity = exercises done
4. **Weekly Bar Chart** — exercises per day for the past 7 days
5. **Module Progress Bars** — % completion per module across all 13
6. **Difficulty Breakdown Donut** — Basic / Intermediate / Advanced solved ratio
7. **XP Timeline** — cumulative XP over time (line chart)

**Auto-tracking**: Every exercise attempt is automatically logged. No manual entry required.

**Daily Goal Logic**:
```python
if exercises_done >= daily_goal:
    streak_count += 1
    goal_met = True
else:
    if yesterday_goal_met == False:
        streak_count = 0   # streak broken
```

---

### Feature 5: Spaced Repetition & Revision Queue

**Description**: After solving an exercise, it is added to the revision queue using the SM-2 algorithm. Users have a dedicated "Revision" page showing all due reviews.

**SM-2 Parameters**:
- `ease_factor`: starts at 2.5, adjusted based on rating
- `interval_days`: starts at 1, grows exponentially
- `repetition_count`: tracks how many times reviewed

**Rating Options** (shown post-answer):
- 😵 Blackout (0) — complete blank, interval → 1 day
- 😕 Hard (3) — remembered with difficulty
- 🙂 Good (4) — remembered with effort
- 😊 Easy (5) — perfect recall, ease_factor +0.1

**Revision Page**:
- Shows exercises due today (sorted by overdue days)
- Quick-answer mode: question → answer → rate recall
- Progress bar: X of Y due today completed

---

### Feature 6: External Question Import

**Description**: Users can import their own PyTorch exercises from multiple sources.

**Import Methods**:

| Method | Format | Notes |
|---|---|---|
| Manual Entry | Web form | Single question, all fields |
| CSV Bulk Import | `.csv` file | Up to 50 questions per upload |
| JSON Import | `.json` file | Structured format (see Section 15) |
| Notebook URL | Colab/nbviewer URL | Imports notebook as notebook_challenge type |
| GitHub Gist | Gist URL | Imports `.ipynb` or `.py` file |

All imported questions go into `custom_questions` table and can optionally be shared with the community (`is_shared = true`).

---

## 8. REST API Endpoints

**Base URL**: `/api/v1`

### Authentication

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/auth/logout` | Invalidate session |
| POST | `/auth/refresh` | Refresh JWT token |
| GET | `/auth/me` | Get current user profile |
| PUT | `/auth/me` | Update profile (name, daily_goal, level) |

### Topics & Modules

| Method | Path | Description |
|---|---|---|
| GET | `/topics` | List all 13 modules with user progress |
| GET | `/topics/{slug}` | Get module detail + exercise list |
| GET | `/topics/{slug}/progress` | Get user's progress for this module |

### Questions

| Method | Path | Description |
|---|---|---|
| GET | `/questions` | List questions (filters: topic, difficulty, type, tags) |
| GET | `/questions/{id}` | Get question detail (statement, starter_code, hints) |
| GET | `/questions/{id}/solution` | Get solution (requires 1 attempt first) |
| GET | `/questions/{id}/test-cases` | Get visible test cases |
| POST | `/questions/{id}/bookmark` | Toggle bookmark |
| GET | `/questions/bookmarked` | Get all bookmarked questions |

### Attempts & Submissions

| Method | Path | Description |
|---|---|---|
| POST | `/attempts` | Submit answer `{question_id, code, result, time_spent_secs}` |
| GET | `/attempts` | Get user's attempt history (paginated) |
| GET | `/attempts/question/{id}` | Get all attempts for a specific question |

### Progress & Tracker

| Method | Path | Description |
|---|---|---|
| GET | `/progress` | Full progress summary across all modules |
| GET | `/progress/topic/{slug}` | Progress for specific module |
| GET | `/tracker/dashboard` | Dashboard stats (streak, today's summary, weekly) |
| GET | `/tracker/heatmap` | 52-week heatmap data |
| GET | `/tracker/history` | Daily activity log (paginated) |
| GET | `/tracker/streak` | Streak data (current, longest, last_active) |

### Revision Queue

| Method | Path | Description |
|---|---|---|
| GET | `/revision/due` | Questions due for review today |
| POST | `/revision/review` | Submit review rating `{question_id, rating: 0-5}` |
| GET | `/revision/stats` | Queue size, due today, overdue |
| DELETE | `/revision/{question_id}` | Remove from queue |

### AI Tutor

| Method | Path | Description |
|---|---|---|
| POST | `/tutor/chat` | Send message to AI tutor |
| GET | `/tutor/history` | Get chat history (last 50 messages) |
| DELETE | `/tutor/history` | Clear chat history |
| GET | `/tutor/usage` | Get daily message count vs limit |

### Colab Integration

| Method | Path | Description |
|---|---|---|
| GET | `/colab/{question_id}` | Get or generate Colab URL for question |
| POST | `/colab/import` | Import notebook from Colab URL |

### Import

| Method | Path | Description |
|---|---|---|
| POST | `/import/manual` | Create custom question manually |
| POST | `/import/csv` | Bulk import from CSV file |
| POST | `/import/json` | Import from JSON payload |
| POST | `/import/notebook` | Import from notebook URL |
| GET | `/import/history` | Get import history |
| GET | `/custom-questions` | List user's custom questions |
| PUT | `/custom-questions/{id}` | Update custom question |
| DELETE | `/custom-questions/{id}` | Delete custom question |

---

## 9. AI Tutor — System Prompt & Configuration

**Model**: `claude-sonnet-4-20250514`  
**Max tokens**: 2048  
**Temperature**: 0.3 (deterministic, technical)

```python
PYTORCH_TUTOR_SYSTEM_PROMPT = """
You are an expert PyTorch engineer and educator with deep knowledge of:
- PyTorch internals (autograd engine, dispatcher, CUDA integration)
- Deep learning theory (optimization, regularization, architectures)
- Computer vision, NLP, and sequence modeling with PyTorch
- Production deployment (TorchScript, ONNX, torch.compile)
- Best practices for training stability, debugging, and performance

## Your Role
You help learners working through the PyTorch Learning Studio platform.
You answer questions about PyTorch concepts, debug their code, and guide
them through building models. You are patient, precise, and educational.

## Communication Style
- Always provide runnable PyTorch code examples (use PyTorch 2.x syntax)
- When debugging, identify the root cause, not just the symptom
- Explain WHY something works, not just HOW
- Use analogies when explaining abstract concepts (e.g., autograd as a tape recorder)
- For shape errors, always show the full shape trace

## Formatting
- Use Markdown for all responses
- Wrap ALL code in ```python code blocks
- Use bullet points for lists of issues or steps
- Bold key terms on first mention

## PyTorch-Specific Rules
- Always mention the PyTorch version when behavior differs across versions
- Prefer torch.nn.functional over deprecated patterns
- For GPU code, always show both CPU and GPU versions
- When showing training loops, always include: zero_grad, forward, loss, backward, step
- Recommend torch.compile for performance-sensitive code (PyTorch 2.0+)

## Limitations
- Do not generate training data or full datasets
- Do not debug non-PyTorch frameworks unless comparing to PyTorch
- Keep responses focused on the user's actual question

## Context
When the user provides code or an exercise context, focus your response on
that specific code. Do not give generic answers when specific ones are possible.
"""
```

**Context injection template** (when opened from exercise page):

```python
EXERCISE_CONTEXT_TEMPLATE = """
## Current Exercise Context

**Module**: {module_name}
**Exercise**: {question_title}
**Difficulty**: {difficulty}
**Type**: {question_type}

**Problem Statement**:
{problem_statement}

**User's Current Code**:
```python
{user_code}
```

**Error / Issue** (if any):
{error_message}

Please help the user with this specific exercise.
"""
```

---

## 10. Question Format Specification

### Example: Module 02 — Intermediate

```json
{
  "id": 47,
  "topic_id": 2,
  "title": "Implement Gradient Accumulation for Large Batch Training",
  "slug": "gradient-accumulation-large-batch",
  "difficulty": "intermediate",
  "question_type": "build_from_scratch",
  "problem_statement": "## Problem\n\nYou are training a model on a GPU with limited memory. Instead of using a batch size of 64, you can only fit 16 samples per forward pass.\n\nImplement **gradient accumulation** to simulate a batch size of 64 by accumulating gradients over 4 mini-batches before calling `optimizer.step()`.\n\n## Requirements\n- Use `accumulation_steps = 4`\n- Only call `optimizer.step()` and `optimizer.zero_grad()` every 4 steps\n- Normalize the loss appropriately\n- The final model weights must be mathematically equivalent to training with batch_size=64",
  "constraints": "Do not use any external library. Only torch, torch.nn, and torch.optim.",
  "starter_code": "import torch\nimport torch.nn as nn\nimport torch.optim as optim\n\n# Simple model\nmodel = nn.Linear(10, 1)\noptimizer = optim.SGD(model.parameters(), lr=0.01)\ncriterion = nn.MSELoss()\n\n# Simulated dataloader (16 batches of size 16 = 256 total samples)\nbatches = [(torch.randn(16, 10), torch.randn(16, 1)) for _ in range(16)]\n\naccumulation_steps = 4\n\n# YOUR CODE HERE\n# Implement the training loop with gradient accumulation\n",
  "expected_output": "Training loop completes without error. optimizer.step() called exactly 4 times.",
  "expected_output_shape": null,
  "pytorch_version": "2.x",
  "gpu_required": false,
  "colab_link": "https://colab.research.google.com/drive/example-gradient-accumulation",
  "tags": ["autograd", "optimization", "training-loop", "memory-efficiency"],
  "xp_reward": 20,
  "time_estimate_mins": 20
}
```

### Corresponding Solution

```json
{
  "question_id": 47,
  "title": "Gradient Accumulation Solution",
  "code": "import torch\nimport torch.nn as nn\nimport torch.optim as optim\n\nmodel = nn.Linear(10, 1)\noptimizer = optim.SGD(model.parameters(), lr=0.01)\ncriterion = nn.MSELoss()\n\nbatches = [(torch.randn(16, 10), torch.randn(16, 1)) for _ in range(16)]\naccumulation_steps = 4\n\noptimizer.zero_grad()\n\nfor i, (inputs, targets) in enumerate(batches):\n    outputs = model(inputs)\n    # Normalize loss by accumulation steps to match full-batch gradient scale\n    loss = criterion(outputs, targets) / accumulation_steps\n    loss.backward()\n\n    if (i + 1) % accumulation_steps == 0:\n        optimizer.step()\n        optimizer.zero_grad()\n        print(f'Step {(i+1)//accumulation_steps}: optimizer.step() called')\n\nprint('Training complete')",
  "explanation": "The key insight is dividing the loss by `accumulation_steps` before calling `.backward()`. This normalizes the gradients so they are mathematically equivalent to computing the gradient on the full batch. Without this normalization, gradients would be 4× larger than expected.",
  "time_complexity": "O(n) — same as standard training",
  "space_complexity": "O(1) extra — no additional memory beyond single mini-batch",
  "is_optimal": true
}
```

---

## 11. UI Wireframes & Page Specs

### Page 1: Dashboard (`/dashboard`)

```
┌─────────────────────────────────────────────────────────┐
│ PyTorch Learning Studio          [🔔] [Profile Avatar]   │
├─────────────────────────────────────────────────────────┤
│ Good morning, Anu 👋                                     │
│                                                         │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐  │
│ │ Today's Goal │ │ 🔥 Streak    │ │ XP This Week     │  │
│ │  3 / 5 done  │ │   12 days    │ │   340 XP         │  │
│ │  ████████░░  │ │   Best: 21   │ │   ▁▃▅▇▄▆▇       │  │
│ └──────────────┘ └──────────────┘ └──────────────────┘  │
│                                                         │
│ 📅 Revision Due Today: 7 exercises  [Start Revision →]  │
│                                                         │
│ Your Progress                                           │
│ Tensors          ████████████░░░░  75%                  │
│ Autograd         ██████░░░░░░░░░░  38%                  │
│ nn.Module        ████░░░░░░░░░░░░  22%                  │
│ Training Loops   ██░░░░░░░░░░░░░░  10%                  │
│ ...                                                     │
│                                                         │
│ 52-Week Heatmap                                         │
│ [GitHub-style calendar grid — colour = exercises done]  │
└─────────────────────────────────────────────────────────┘
```

### Page 2: Exercise Page (`/modules/[slug]/[id]`)

```
┌──────────────────────────────────────────────────────────┐
│ ← Autograd   |  Gradient Accumulation   [⭐ Bookmark]    │
│ 🟡 Intermediate  |  🔧 Build from Scratch  |  20 XP  20min│
├────────────────────────┬─────────────────────────────────┤
│  PROBLEM               │  CODE EDITOR                    │
│                        │                                 │
│  [Markdown + MathJax]  │  [Monaco Editor]                │
│                        │  Python syntax + PyTorch hints  │
│  ## Problem            │                                 │
│  Implement gradient    │  import torch                   │
│  accumulation...       │  import torch.nn as nn         │
│                        │  # YOUR CODE HERE               │
│  Test Cases:           │                                 │
│  ✅ Case 1 (visible)   ├─────────────────────────────────┤
│  🔒 Case 2 (hidden)    │  OUTPUT                         │
│                        │  [Console output panel]         │
│  [💡 Hint 1]           ├─────────────────────────────────┤
│  [💡 Hint 2 (−2 XP)]   │  [✅ Submit]  [🧪 Check Shape]  │
│                        │  [📓 Open in Colab]             │
│  [🤖 Ask AI Tutor]     │  [👁 View Solution]             │
└────────────────────────┴─────────────────────────────────┘
```

### Page 3: AI Tutor (`/tutor`)

```
┌─────────────────────────────────────────────────────────┐
│ 🤖 PyTorch AI Tutor          [📎 Attach Exercise] [⚙️]  │
│ Powered by Claude                    Usage: 8/20 today  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 🤖 Ask me anything about PyTorch! I can:        │    │
│  │  • Debug your code & shape errors               │    │
│  │  • Explain autograd and backprop                │    │
│  │  • Review your model architecture               │    │
│  │  • Compare training strategies                  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  [User message bubble]                                  │
│  [AI response with code block]                          │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  [Type your question... ]              [Attach code] [→] │
└─────────────────────────────────────────────────────────┘
```

### Page 4: Revision Queue (`/revision`)

```
┌─────────────────────────────────────────────────────────┐
│ 📚 Today's Revision Queue                               │
│ 7 due today  •  3 overdue  •  42 total in queue         │
├─────────────────────────────────────────────────────────┤
│ [Start Review Session →]                                │
│                                                         │
│ OVERDUE                                                 │
│ ┌────────────────────────────────────────┐              │
│ │ 🔴 Tensor Broadcasting Rules     +3d   │              │
│ │    Module 01 · Basic              [→]  │              │
│ └────────────────────────────────────────┘              │
│                                                         │
│ DUE TODAY                                               │
│ ┌────────────────────────────────────────┐              │
│ │ 🟡 Custom Autograd Function      Today │              │
│ │    Module 02 · Advanced           [→]  │              │
│ └────────────────────────────────────────┘              │
│  ... (5 more)                                           │
│                                                         │
│ [Rating reminder: 😵 Blackout | 😕 Hard | 🙂 Good | 😊 Easy] │
└─────────────────────────────────────────────────────────┘
```

### Page 5: Import (`/import`)

```
┌─────────────────────────────────────────────────────────┐
│ ➕ Import Custom Exercises                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ ✏️ Manual │ │ 📄 CSV   │ │ {} JSON  │ │ 📓 Colab │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                         │
│  [Import form based on selected tab]                    │
│                                                         │
│  ─────── Import History ────────                        │
│  2026-06-01  CSV import  12 questions  ✅ Success       │
│  2026-05-28  Manual      1 question    ✅ Success       │
└─────────────────────────────────────────────────────────┘
```

---

## 12. Spaced Repetition Engine

**Algorithm**: SuperMemo 2 (SM-2)

**File**: `backend/app/services/spaced_repetition.py`

```python
from datetime import date, timedelta
from dataclasses import dataclass

@dataclass
class ReviewResult:
    next_review_date: date
    new_interval: int
    new_ease_factor: float
    new_repetition_count: int


def calculate_next_review(
    rating: int,          # 0=blackout, 3=hard, 4=good, 5=easy
    ease_factor: float,   # current ease factor (default 2.5)
    interval_days: int,   # current interval in days
    repetition_count: int # how many times reviewed
) -> ReviewResult:
    """
    SM-2 algorithm implementation.
    rating < 3: treat as blackout — reset to day 1
    """
    if rating < 3:
        # Failed recall — reset
        new_interval = 1
        new_repetition_count = 0
        new_ease_factor = max(1.3, ease_factor - 0.2)
    else:
        new_repetition_count = repetition_count + 1
        new_ease_factor = ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
        new_ease_factor = max(1.3, new_ease_factor)

        if new_repetition_count == 1:
            new_interval = 1
        elif new_repetition_count == 2:
            new_interval = 6
        else:
            new_interval = round(interval_days * new_ease_factor)

    next_review = date.today() + timedelta(days=new_interval)

    return ReviewResult(
        next_review_date=next_review,
        new_interval=new_interval,
        new_ease_factor=round(new_ease_factor, 2),
        new_repetition_count=new_repetition_count
    )
```

**Queue population logic**:
- Question added to queue on first correct submission
- Questions with `result = 'incorrect'` reset interval to 1 day
- Daily Celery task at 00:05 UTC refreshes the "due today" view

---

## 13. Daily Tracker & Analytics

### Nightly Aggregation Task

**File**: `backend/app/tasks/nightly_aggregation.py`

```python
@celery_app.task
def aggregate_daily_activity():
    """Runs nightly at 00:05 UTC. Rolls up today's attempts into daily_activity."""
    yesterday = date.today() - timedelta(days=1)

    # For each user with activity yesterday
    # Aggregate: count attempts, correct, time_spent, XP
    # Update streak_count on users table
    # Set goal_met = (exercises_done >= daily_goal)
    pass
```

### XP System

| Action | XP Reward |
|---|---|
| First correct submission | +10 (Basic), +20 (Intermediate), +30 (Advanced) |
| Using a hint | −2 per hint |
| Completing daily goal | +25 bonus |
| Perfect revision session (all rated 4+) | +15 bonus |
| Completing a full module | +100 milestone XP |
| 7-day streak | +50 bonus |
| 30-day streak | +200 bonus |

---

## 14. Notebook Integration (Colab / Jupyter)

### Colab URL Generation

For exercises with `colab_link` already set, return the stored URL directly.

For exercises without a Colab link, generate a template notebook:

**File**: `backend/app/services/colab_service.py`

```python
import nbformat
import base64

def generate_notebook(question: Question) -> str:
    """Generates a Jupyter notebook from a question and returns a Colab URL."""
    nb = nbformat.v4.new_notebook()

    # Cell 1: Title and description
    nb.cells.append(nbformat.v4.new_markdown_cell(
        f"# {question.title}\n\n"
        f"**Module**: {question.topic.name}  \n"
        f"**Difficulty**: {question.difficulty}  \n\n"
        f"---\n\n"
        f"{question.problem_statement}"
    ))

    # Cell 2: Install PyTorch (if not in Colab already)
    nb.cells.append(nbformat.v4.new_code_cell(
        "# Install dependencies (skip if already installed)\n"
        "# !pip install torch torchvision"
    ))

    # Cell 3: Starter code
    nb.cells.append(nbformat.v4.new_code_cell(question.starter_code or "# Your code here"))

    # Encode as base64 for Colab open URL
    nb_str = nbformat.writes(nb)
    encoded = base64.urlsafe_b64encode(nb_str.encode()).decode()

    # Google Colab supports opening notebooks from base64-encoded content
    colab_url = f"https://colab.research.google.com/notebook#{encoded}"
    return colab_url
```

### Notebook Import

When a user provides a Colab/nbviewer/GitHub notebook URL:

1. Fetch the `.ipynb` JSON
2. Extract markdown cells → `problem_statement`
3. Extract first code cell → `starter_code`
4. Infer module from notebook filename or user-selected topic
5. Create entry in `custom_questions` with `source = 'notebook'`

---

## 15. External Question Import

### CSV Format

```csv
title,topic_slug,difficulty,question_type,problem_statement,starter_code,expected_output,tags,colab_link,time_estimate_mins
"Custom Tensor Norm","tensors","intermediate","code_completion","Implement L2 norm without torch.norm","import torch\nx = torch.randn(3, 4)\n# YOUR CODE HERE","tensor([[...]]shape=(3,4))","tensors,linear-algebra","","15"
```

### JSON Format

```json
{
  "questions": [
    {
      "title": "Implement Batch Normalization from Scratch",
      "topic_slug": "nn-module",
      "difficulty": "advanced",
      "question_type": "build_from_scratch",
      "problem_statement": "Implement BatchNorm1d from scratch using only basic tensor operations...",
      "starter_code": "import torch\nimport torch.nn as nn\n\nclass MyBatchNorm1d(nn.Module):\n    def __init__(self, num_features):\n        super().__init__()\n        # YOUR CODE HERE\n    \n    def forward(self, x):\n        # YOUR CODE HERE\n        pass",
      "expected_output_shape": "(batch_size, num_features)",
      "tags": ["batch-norm", "normalization", "custom-layer"],
      "colab_link": "",
      "gpu_required": false,
      "time_estimate_mins": 30
    }
  ]
}
```

---

## 16. Implementation Roadmap

### Phase 1 — Foundation (Weeks 1–4)

- [ ] Repository setup: fork from DSA Studio, rename, clean git history
- [ ] Update docker-compose.yml (no changes needed, reuse as-is)
- [ ] Run Alembic migration: add `colab_link`, `expected_output_shape`, `gpu_required`, `pytorch_version` columns to `questions`
- [ ] Seed 13 topics into `topics` table (topics.py)
- [ ] Seed 60 starter questions across Modules 01–03 (20 per module)
- [ ] Update FastAPI routers (rename topic references, add colab endpoint)
- [ ] Verify auth, daily tracker, spaced repetition work unchanged
- [ ] Basic frontend: module grid + exercise page (reuse DSA Studio components, retheme)

**Deliverable**: Functional app with 3 modules, 60 exercises, Colab links working

---

### Phase 2 — Content Expansion (Weeks 5–8)

- [ ] Seed Modules 04–07 (Training, Loss, DataLoaders, CNNs)
- [ ] Implement `ColabLauncher` component with notebook generation fallback
- [ ] Implement `ShapeValidator` component
- [ ] Monaco editor: add PyTorch autocomplete snippets
- [ ] Full AI Tutor implementation (Anthropic API integration + system prompt)
- [ ] Exercise context injection into tutor from exercise page

**Deliverable**: 7 modules live, AI tutor working, Colab integration complete

---

### Phase 3 — Analytics & Tracker (Weeks 9–12)

- [ ] Dashboard page: all 7 components (streak, heatmap, module progress, XP timeline)
- [ ] Recharts integration for analytics charts
- [ ] Nightly Celery aggregation task
- [ ] XP system: calculation, awards, milestone notifications
- [ ] Revision queue page with SM-2 review flow

**Deliverable**: Full tracker + revision system live

---

### Phase 4 — Import & Community (Weeks 13–16)

- [ ] Import page: manual entry form
- [ ] CSV bulk import with validation
- [ ] JSON import endpoint
- [ ] Notebook URL import (Colab/nbviewer)
- [ ] `is_shared` flag + community question browser
- [ ] User notes per exercise

**Deliverable**: Import system complete, community questions visible

---

### Phase 5 — Remaining Modules & Polish (Weeks 17–20)

- [ ] Seed Modules 08–13 (RNNs, Transformers, Transfer Learning, Deployment, GPU, Lightning)
- [ ] Reach 500+ total exercises
- [ ] Search & filter across all exercises
- [ ] Keyboard shortcuts in editor (Ctrl+Enter to run, Ctrl+H for hints)
- [ ] Mobile-responsive layout
- [ ] Dark mode

**Deliverable**: Full 13-module content library, polished UX

---

### Phase 6 — Production (Weeks 21–24)

- [ ] AWS ECS Fargate deployment (reuse VidShield AI Terraform config)
- [ ] CloudFront CDN for frontend
- [ ] GitHub Actions CI/CD pipeline
- [ ] Performance testing (k6 load tests)
- [ ] Security audit (OWASP top 10)
- [ ] Documentation: README, API docs (auto-generated from FastAPI /docs)

**Deliverable**: Production-ready deployment on AWS

---

## 17. Environment Variables

```env
# ── Application ──────────────────────────────────────────
APP_NAME=pytorch-learning-studio
APP_ENV=development                        # development|staging|production
APP_PORT=8000
FRONTEND_URL=http://localhost:3000
SECRET_KEY=your-jwt-secret-key-min-32-chars

# ── Database ─────────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/pytorch_studio
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# ── Redis ────────────────────────────────────────────────
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ── Anthropic ────────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-...
TUTOR_MODEL=claude-sonnet-4-20250514
TUTOR_MAX_TOKENS=2048
TUTOR_DAILY_LIMIT_FREE=20

# ── AWS (Production) ─────────────────────────────────────
AWS_REGION=ca-central-1
AWS_S3_BUCKET=pytorch-studio-assets
AWS_CLOUDFRONT_URL=https://cdn.pytorch-studio.example.com

# ── Colab Integration ────────────────────────────────────
COLAB_NOTEBOOK_BASE_URL=https://colab.research.google.com/notebook#
NBVIEWER_BASE_URL=https://nbviewer.org/url/

# ── JWT ──────────────────────────────────────────────────
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30
```

---

## 18. Development Commands

```bash
# ── Setup (using uv) ─────────────────────────────────────
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# ── Database ─────────────────────────────────────────────
alembic upgrade head                       # run all migrations
alembic revision --autogenerate -m "add colab fields"
python -m seeds.topics                     # seed 13 PyTorch modules
python -m seeds.questions_tensors          # seed Module 01 questions

# ── Run Backend ──────────────────────────────────────────
uvicorn app.main:app --reload --port 8000

# ── Run Celery ───────────────────────────────────────────
celery -A app.tasks.celery_app worker --loglevel=info
celery -A app.tasks.celery_app beat --loglevel=info   # cron scheduler

# ── Frontend ─────────────────────────────────────────────
cd frontend
npm install
npm run dev                                # starts on :3000

# ── Docker Compose (Full Stack) ──────────────────────────
docker-compose up -d                       # postgres + redis + backend + frontend
docker-compose logs -f backend

# ── Tests ────────────────────────────────────────────────
pytest backend/tests/ -v
cd frontend && npm run test

# ── Linting ──────────────────────────────────────────────
ruff check backend/                        # Python linting
ruff format backend/
cd frontend && npm run lint                # ESLint
```

---

## 19. Future Enhancements (V2 / V3)

### V2 (Months 6–9)

- **Live Code Execution**: Integrate with Judge0 or custom sandboxed executor to run PyTorch code in-browser without Colab
- **Video Explanations**: 2–5 minute video walkthroughs per module linked from exercise pages
- **Path Recommendations**: AI-powered learning path suggestions based on user's performance profile
- **Leaderboard**: Weekly XP rankings among users (opt-in)
- **Study Groups**: Shared revision queues and progress tracking for cohorts (e.g., Euron Super 30)

### V3 (Months 10–18)

- **Paper-to-Exercise Pipeline**: Given an arXiv paper URL, auto-generate implementation exercises using the AI pipeline
- **Interview Mode**: Timed ML engineering interview simulations (30-min coding challenges)
- **Certification**: Completion certificates for each module (PDF, shareable on LinkedIn)
- **Mobile App**: React Native companion app with offline exercise cache
- **Multi-Framework**: Extend the same architecture to JAX, TensorFlow 2.x as separate studio instances

---

## Document Metadata

| Field | Value |
|---|---|
| **Document Version** | 1.0 |
| **Created** | June 3, 2026 |
| **Author** | Anu (OrionVexa) |
| **Based On** | Unified DSA Studio CLAUDE.md v1.0 |
| **Status** | Ready for Implementation |
| **Next Review** | After Phase 1 completion |
| **Repo** | github.com/anulsasidharan/pytorch-learning-studio |
