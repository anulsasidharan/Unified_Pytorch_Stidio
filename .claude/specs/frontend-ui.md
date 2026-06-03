# Frontend UI — PyTorch Learning Studio

*Extracted from `.claude/rules/CLAUDE.md` §7 Feature Specifications & §11 UI Wireframes*

Stack: Next.js 14 (App Router), TypeScript, Tailwind, shadcn/ui, Monaco, Recharts, MathJax.

---

## Global navigation

```
[🏠 PyTorch Studio]  [📚 Modules]  [📊 Tracker]  [🔄 Revision]  [🤖 Tutor]  [📥 Import]
```

- **Modules** → Module browser and exercise list  
- **Tracker** → Analytics dashboard  
- **Revision** → SM-2 spaced repetition queue  
- **Tutor** → AI PyTorch tutor chat  
- **Import** → Custom exercise import  

---

## Page: Dashboard (`/dashboard`)

| Section | Content |
|---------|---------|
| Quick stats | Streak 🔥, total XP, modules completed, exercises solved |
| Today's summary | Exercises done / daily goal, XP earned today, time spent |
| Module progress | Progress rings for all 13 modules |
| Due for revision | Top N items due today + View All |
| Continue learning | Last exercise + CTA |

Wireframe reference: `rules/CLAUDE.md` §11 Dashboard Page.

---

## Page: Module browser (`/modules`)

| Section | Content |
|---------|---------|
| ModuleGrid | 13 cards with icon, name, progress ring (%), exercise count |
| Search bar | Filter by title, tags, keywords |

---

## Page: Module detail (`/modules/[slug]`)

| Section | Content |
|---------|---------|
| ModuleHeader | Name, description, your progress % |
| DifficultyTabs | All \| Basic \| Intermediate \| Advanced |
| FilterBar | Type, GPU required, completed/not completed |
| ExerciseList | Cards: title, difficulty badge, type badge, XP, time estimate, Colab indicator |

---

## Page: Exercise (`/modules/[slug]/[questionId]`)

**Layout:** Header (title, difficulty, type, tags, bookmark) · Problem statement · Editor zone · Side panel

| Zone | Components |
|------|------------|
| Statement | Markdown + MathJax rendered problem |
| Editor | Monaco with starter code; type-specific behavior (see below) |
| Actions | Run / Submit / Check Shape / Open in Colab / Show Hint |
| Side panel | Test results, XP earned, tutor chat panel |
| Footer | Personal notes, bookmark, difficulty rating |

**Exercise type behaviors:**

| Type | UI |
|------|-----|
| `code_completion` | Pre-filled code with `# YOUR CODE HERE` gaps |
| `debug_model` | Pre-filled buggy code to fix |
| `conceptual_mcq` | Multiple choice radio buttons, no editor |
| `build_from_scratch` | Empty editor with imports only |
| `notebook_challenge` | Description + Colab launch button, no local editor |
| `shape_assertion` | Code editor + ShapeValidator for expected shape |

**Interactions:**

- Submit → grade + update progress + award XP + add to revision queue on correct  
- Show Hint → progressive drawer (−2 XP per hint)  
- Check Shape → validate `expected_output_shape` against user code output  
- Open in Colab → launch `colab_link` or generate notebook  
- Solution drawer → locked until 1 attempt made  

---

## Page: Tracker (`/tracker`)

**Tabs:** Overview | Modules | Performance | Streaks

| Visualization | Data source |
|---------------|-------------|
| Today's summary card | `/tracker/dashboard` |
| 52-week heatmap | `/tracker/heatmap` |
| Module progress rings | `/progress` |
| XP timeline | `/tracker/history` |
| Weekly bar chart | `/tracker/dashboard` |
| Achievements | Streak records, milestone badges |

Components: `StreakCounter`, `HeatmapCalendar`, `ProgressRing`, `WeeklyChart`

---

## Page: Revision (`/revision`)

- Due today list with SM-2 priority indicators  
- Upcoming week count  
- Review flow: show exercise → user rates recall (0–5) → schedule next review  
- One-click "Start revision session"  

---

## Page: Tutor (`/tutor`)

- Full-page chat interface with PyTorch tutor  
- Context badge when opened from exercise page  
- Message history (last 50)  
- Daily usage counter vs limit  
- Code suggestion blocks with syntax highlighting  

Components: `ChatInterface`, `MessageBubble`, `CodeSuggestion`

---

## Page: Import (`/import`)

**Tabs:** Manual Entry | CSV Import | JSON Import | Notebook URL

- Drag-drop upload for CSV/JSON  
- Template download links (spec §15 formats)  
- Import history table  
- Preview before save  
- Community share toggle (`is_shared`)  

---

## Page: Profile (`/profile`)

- Username, email, avatar  
- PyTorch level selector (beginner/intermediate/advanced)  
- Daily goal setting  
- Streak and XP summary  

---

## Component conventions (shadcn/ui)

| Pattern | Component |
|---------|-----------|
| Data tables | `Table` + pagination |
| Filters | `Select`, `Command` combobox for tags |
| Modals | `Dialog` for hints, confirm submit |
| Toasts | Sonner for submit result, XP earned |
| Loading | Skeleton on exercise and dashboard loads |
| Badges | `DifficultyBadge` (basic=green, intermediate=amber, advanced=red) |

---

## Accessibility

- Keyboard navigation in Monaco toolbar  
- Focus trap in hint/solution dialogs  
- Sufficient contrast for difficulty and type badges  
- `aria-live` region for test run results and XP notifications  

---

## Responsive behavior

- **Desktop:** side-by-side editor + test panel  
- **Tablet:** stacked editor above tests  
- **Mobile:** editor full width; tests in collapsible panel; simplified dashboard charts  

---

## Design tokens (suggested)

| Token | Usage |
|-------|--------|
| `--difficulty-basic` | Green tones |
| `--difficulty-intermediate` | Amber |
| `--difficulty-advanced` | Red |
| `--streak-fire` | Streak emphasis |
| `--xp-gold` | XP earned animations |
| `--module-color-{n}` | Per-module accent from `topics.color` |
