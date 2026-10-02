# Reusable Prompt Pack — Flagged Category Narrative

## Trigger

Start this prompt when a category's `is_flagged` result is exactly:

`flagged`

The prompt is used to convert verified Part 1 / Part 2 category results into a stakeholder-facing update.

---

## Input list

The prompt requires these verified placeholder values:

- `{category}` — category name
- `{previous_revenue}` — revenue in the previous month
- `{current_revenue}` — revenue in the current month
- `{mom_pct}` — month-over-month percentage change
- `{month}` — current month
- `{prev_month}` — previous month

These values must come from the verified Part 1 / Part 2 output.

---

## Prompt

You are writing a concise business update for a regional manager.

Use only the verified values supplied in these placeholders:

- Category: `{category}`
- Previous month: `{prev_month}`
- Current month: `{month}`
- Previous revenue: `{previous_revenue}`
- Current revenue: `{current_revenue}`
- MoM change: `{mom_pct}%`

Write the update using exactly this structure:

### Context
State what category is being measured and compare `{month}` with `{prev_month}`.

### Insight
State the MoM change of `{mom_pct}%` and explicitly label it as a **Fact**.

Use only numbers supplied in the placeholders.

### Implication
Give one specific and actionable next step for the regional manager.

If you suggest a possible reason for the change, label it explicitly as a **Hypothesis**, because the supplied data does not prove the cause.

Important rules:

1. Never invent a number.
2. Never calculate or introduce an additional number that is not supplied in the placeholders.
3. Never introduce unsupported causes as facts.
4. Keep the category and month names exactly as supplied.
5. Write for a regional manager rather than a data engineer.
6. Keep the recommendation specific and actionable.
7. Do not mention internal implementation details unless they are directly relevant.
8. If a reseller is mentioned, use only its coded alias and never its raw reseller name.

## Checklist

Before the narrative is used, verify all of the following:

1. **Number check:** Does every number in the draft exactly match one of the supplied placeholder values?

2. **Fact check:** Is the MoM result explicitly labeled as a **Fact**?

3. **Hypothesis check:** Is every proposed cause clearly labeled as a **Hypothesis** rather than presented as a proven fact?

4. **Structure check:** Are Context, Insight, and Implication all present?

5. **Actionability check:** Does the Implication contain a specific next action rather than a vague instruction such as "look into it"?

6. **Audience check:** Is the narrative written for a regional manager and understandable without reading the Python code?

7. **Privacy check:** If a reseller is referenced, is only the coded alias used and is the raw reseller name absent?

8. **Category/month check:** Do the category and month names exactly match the supplied verified data?