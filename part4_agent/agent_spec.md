\# Part 4 — Agent Specification



\## 4.1 Agent Specification



\### Goal



Keep Meesho category managers informed of categories whose month-on-month revenue moves beyond the 8% threshold, while requiring human approval before any drafted message is considered sent.



\### Tools



The monitoring agent uses the following existing project functions:



\- `validate\_feed()` from Part 2 to validate the monthly revenue CSV before processing.

\- `mom\_growth()` from Part 2 to calculate month-on-month revenue change.

\- `is\_flagged()` from Part 2 to classify each category according to the 8% threshold.

\- Part 3 prompt-pack template-fill logic to create the stakeholder-facing draft message.



The Part 2 functions are imported and used without re-implementing their logic.



\### Memory / State



The agent must use the previous month's revenue per category as state for the next month-over-month calculation.



For each category, the relevant state is:



\- category name

\- previous month's revenue

\- current month's revenue

\- calculated MoM percentage

\- flag status



The previous-month CSV provides the revenue baseline for the current run.



\### Planner



The agent executes these subtasks in order:



1\. Load the monthly revenue feed and run `validate\_feed()`.

2\. If validation fails, Hard Stop and report all validation errors.

3\. If validation succeeds, compute `mom\_growth()` for every category against the previous month.

4\. Run `is\_flagged()` on every category.

5\. Sort flagged categories by absolute MoM percentage in descending order.

6\. Draft a message using the Part 3 template for at most the top 3 flagged categories.

7\. Log remaining flagged categories as `suppressed, review manually` without drafting a message.

7b. Separately record categories whose result is `escalate\_exact\_boundary` in `escalated\_categories` without drafting a message.

8\. Emit one structured JSON object for the run.



\### Feedback Loop



Every drafted message is held for human approval.



The mock agent does not send emails or other messages. The output uses:



`drafted\_and\_held\_for\_approval`



to show that messages were drafted but not automatically sent.



\---



\## Guardrails



\### Input Guardrail



`validate\_feed()` must pass before any other processing occurs.



If validation fails, no MoM calculation or message drafting is attempted.



\### Action Guardrail



No message is ever automatically sent.



Messages are only drafted and held for human approval.



\### Output Guardrail



Every number in a drafted message must trace back to a verified Part 1 or Part 2 value.



The agent must never invent business figures.



\---



\## Success and Error Stopping Conditions



\### Success



A run succeeds when:



\- the input feed passes validation;

\- MoM calculations are completed;

\- flagged categories are classified correctly;

\- the top 3 flagged categories are drafted;

\- additional flagged categories are suppressed;

\- exact-boundary categories are escalated separately;

\- every number in every drafted message is traceable to Part 1 or Part 2;

\- a structured JSON object is emitted.



A valid run may also produce zero drafts when no category crosses the threshold.



\### Error



If `validate\_feed()` returns `False`, the agent performs a Hard Stop.



The validation errors are surfaced in the JSON output.



No MoM computation is attempted.



No messages are drafted.



\---



\## 4.2 Ordered Subtasks



1\. Load the monthly revenue feed and run `validate\_feed()`.

2\. If invalid, Hard Stop and report errors.

3\. If valid, compute `mom\_growth()` for every category against the previous month.

4\. Run `is\_flagged()` on every category.

5\. Sort flagged categories by `abs(mom\_pct)` descending.

6\. Draft a message using the Part 3 template for at most the top 3 flagged categories.

7\. Log remaining flagged categories as `suppressed, review manually`.

7b. Record every `escalate\_exact\_boundary` category in `escalated\_categories` without drafting a message.

8\. Emit one structured JSON object per run.



\---



\## 4.3 Structured JSON Output Schema



Every run must emit one JSON object with exactly these top-level keys:



\- `run\_month`

\- `validation\_status`

\- `validation\_errors`

\- `flagged\_categories`

\- `suppressed\_categories`

\- `escalated\_categories`

\- `action\_taken`



\### `validation\_status`



Allowed values:



\- `valid`

\- `invalid`



\### `validation\_errors`



A list of validation error strings.



It must be empty when validation succeeds.



\### `flagged\_categories`



A list of objects containing:



\- `category`

\- `mom\_pct`

\- `previous\_revenue`

\- `current\_revenue`

\- `drafted`

\- `message` when drafted



\### `suppressed\_categories`



A list of category names that were flagged but exceeded the top-3 drafting cap.



\### `escalated\_categories`



A list of category names whose `is\_flagged()` result is:



`escalate\_exact\_boundary`



Exact-boundary categories must not be drafted or silently dropped.



\### `action\_taken`



Allowed values:



\- `drafted\_and\_held\_for\_approval`

\- `hard\_stop`



\---



\## 4.4 Given-When-Then Agent Specifications



\### Specification 1 — Ethnic Wear May Growth



\*\*Given\*\* the verified April and May monthly revenue feeds



\*\*When\*\* the agent calculates Ethnic Wear month-on-month growth



\*\*Then\*\* the result must be `77.1%` and the category must be flagged.



\### Specification 2 — Beauty \& Personal Care June Boundary



\*\*Given\*\* the verified May and June monthly revenue feeds



\*\*When\*\* the agent evaluates Beauty \& Personal Care



\*\*Then\*\* the result must be `5.67%` and the category must be `not\_flagged`.



\### Specification 3 — Exact Threshold Boundary



\*\*Given\*\* a category with exactly `8.0%` month-on-month growth



\*\*When\*\* the agent evaluates the category using `is\_flagged()`



\*\*Then\*\* the result must be `escalate\_exact\_boundary`.



\### Specification 4 — Corrupted Feed



\*\*Given\*\* a monthly revenue feed containing negative revenue and missing category or revenue values



\*\*When\*\* the agent runs `validate\_feed()`



\*\*Then\*\* the agent must Hard Stop, surface the validation errors, and perform no MoM computation or message drafting.

