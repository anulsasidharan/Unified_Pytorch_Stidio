# AI Tutor — PyTorch Learning Studio

*Extracted from `.claude/rules/CLAUDE.md` §9 AI Tutor — System Prompt & Configuration*

Provider: **Anthropic** `claude-sonnet-4-20250514` (only provider; record in MEMORY).

---

## Capabilities

| Mode | Endpoint | Behavior |
|------|----------|----------|
| Concept explanation | `POST /tutor/chat` | Explain PyTorch concepts with runnable code examples |
| Code debugging | `POST /tutor/chat` | Identify shape mismatches, device errors, NaN loss root causes |
| Autograd explanation | `POST /tutor/chat` | Explain computation graphs, grad_fn chains, hooks |
| Architecture review | `POST /tutor/chat` | Review user model code; suggest improvements |
| Progressive hints | Context from exercise page | Tiered hints; never dump full solution immediately |
| Paper implementations | `POST /tutor/chat` | Explain paper architectures in PyTorch with MREs |

---

## Model configuration

| Setting | Value |
|---------|-------|
| Model | `claude-sonnet-4-20250514` |
| Max tokens | 2048 |
| Temperature | 0.3 (deterministic, technical) |
| Daily limit (free) | 20 messages/day |
| Daily limit (pro) | Unlimited (V3) |

---

## System prompt principles

1. **PyTorch expert** — deep knowledge of autograd, nn.Module, training loops, deployment.  
2. **Runnable examples** — always provide PyTorch 2.x syntax in ` ```python ` blocks.  
3. **Root cause debugging** — identify why something fails, not just how to fix it.  
4. **Shape traces** — for shape errors, show full shape trace through the computation.  
5. **Training loop completeness** — always include zero_grad, forward, loss, backward, step.  
6. **Version awareness** — mention PyTorch version when behavior differs across versions.  
7. **No full solution** on first interaction unless user explicitly requests after hints.  
8. **Safety** — refuse non-PyTorch requests; no personal data collection.

Full system prompt: `rules/CLAUDE.md` §9 (`PYTORCH_TUTOR_SYSTEM_PROMPT`).

---

## Context assembly

Include in system/context payload when on exercise page:

- Module name, exercise title, difficulty, question_type  
- Problem statement (not hidden test outputs)  
- User's current code and last error message  
- Hints already revealed (count for XP tracking)  
- Tags and related techniques  

**Exclude:** hidden test inputs, other users' data, API keys.

Exercise context template: `rules/CLAUDE.md` §9 (`EXERCISE_CONTEXT_TEMPLATE`).

---

## Hint behavior

| Tier | Content level |
|------|----------------|
| 1 | Conceptual nudge — what to think about |
| 2 | Specific PyTorch API or pattern hint |
| 3 | Approach name + partial code structure |
| 4+ | Detailed guidance (still not full solution) |

Each hint costs −2 XP. Track `hints_used` on `user_attempts`.

---

## Code review output format

```markdown
✅ Correct logic
⚠️ Shape issue: expected (32, 10), got (10, 32) — check weight matrix dimensions
💡 Suggestion: use `nn.Linear(in_features, out_features)` with correct ordering
```

Offer optimized version only after user confirms.

---

## Rate limiting & cost

| Limit | Value |
|-------|-------|
| Tutor messages | 20/day per user (free tier) |
| Max tokens | 2048 output; truncate long code inputs |
| Timeout | 30s per request |

Log token usage per user for future billing tier (V3 premium).

---

## Import classification (Phase 4)

When user pastes raw exercise text or notebook content:

1. LLM extracts: title, description, difficulty, module, tags, question_type  
2. User reviews in UI before `POST /import/manual`  
3. Store in `custom_questions` with `import_source`  

---

## Error handling

| Case | Response |
|------|----------|
| Provider timeout | 503 + retry message |
| Content policy block | 400 + explain revision |
| Missing context | 400 + require question_id for exercise-scoped chat |
| Daily limit exceeded | 429 + show usage count and reset time |

Never expose Anthropic API keys or raw stack traces to client.

**Degradation:** On Anthropic outage, show static DB hints and "tutor unavailable" message.

---

## Testing

- Mock Anthropic in CI with fixture responses  
- Golden tests: tutor must not give full solution on first message for exercise context  
- Regression: shape error responses must include shape trace  
- Verify exercise context injection includes problem statement and user code
