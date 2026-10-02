# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

This project builds a reliable reseller analytics and alert pipeline using a four-part workflow:

```text
Dataset
   ↓
Part 1 — SQL Analytics
   ↓
Part 2 — Growth & Validation Engine
   ↓
Part 3 — Reliable AI Narrative
   ↓
Part 4 — Mock Agent Runner
   ↓
Drafted message held for human approval
```

The pipeline analyzes reseller order data, calculates category revenue and month-over-month growth, validates incoming data, creates factual business narratives, and demonstrates an agent-style reporting workflow.

The complete pipeline runs locally with **zero API keys** and does not require a paid service or external LLM.

---

## Requirements

* Python 3.x
* SQLite
* Git

No API key is required.

---

## Step 1 — Generate the Dataset

From the project root, run:

```cmd
python data/generate_dataset.py
```

This generates:

```text
data/resellers.csv
data/orders.csv
data/meesho_reseller.db
```

The dataset uses a deterministic random seed so the generated data is reproducible.

---

## Step 2 — Run Part 1: SQL Analytics

Run:

```cmd
python part1_sql/run_queries.py
```

Part 1 calculates:

* Monthly revenue by category
* Regional revenue and order count
* Top 5 resellers by total spend
* Resellers with zero orders
* `COUNT(*)` versus `COUNT(order_id)` demonstration
* June delivered Average Order Value

The SQL queries are stored in:

```text
part1_sql/queries.sql
```

Outputs are written to:

```text
part1_sql/output/
```

Expected output files:

```text
monthly_category_revenue.csv
region_revenue.csv
top_resellers.csv
inactive_resellers.csv
count_demonstration.csv
june_delivered_aov.csv
```

---

## Step 3 — Run Part 2: Growth & Validation Engine

Run the test suite:

```cmd
python -m pytest -v
```

The growth engine is:

```text
part2_engine/growth_engine.py
```

It provides:

* Month-over-month growth calculation
* Growth flagging
* Exact 8% boundary handling
* CSV validation
* Missing category detection
* Missing revenue detection
* Non-numeric revenue detection
* Negative revenue detection

Flagging rules:

```text
absolute MoM change > 8%  → flagged
absolute MoM change < 8%  → not_flagged
absolute MoM change = 8%  → escalate_exact_boundary
```

Fixtures are stored in:

```text
part2_engine/fixtures/
```

---

## Step 4 — Run Part 3: Reliable Narrative

The reusable narrative prompt pack is:

```text
part3_narrative/prompt_pack.md
```

The narrative structure is:

```text
Context → Insight → Implication
```

The worked narrative report is:

```text
part3_narrative/narrative_report.md
```

Run the masking checks:

```cmd
python part3_narrative/masking.py
```

The masking utility converts reseller IDs into external-facing aliases, for example:

```text
RS019 → ALIAS-19
RS006 → ALIAS-06
```

It also checks that raw reseller names do not leak into external-facing narrative text.

---

## Step 5 — Run Part 4: Mock Agent Runner

Part 4 demonstrates an agent-style reporting workflow without an external AI service.

### May run

```cmd
python -m part4_agent.mock_agent_runner May part4_agent/fixtures/april.csv part4_agent/fixtures/may.csv
```

### June run

```cmd
python -m part4_agent.mock_agent_runner June part4_agent/fixtures/may.csv part4_agent/fixtures/june.csv
```

### Corrupted-data hard-stop test

```cmd
python -m part4_agent.mock_agent_runner July part4_agent/fixtures/may.csv part2_engine/fixtures/corrupted_feed.csv
```

The runner:

1. Validates the input feed.
2. Calculates category MoM changes.
3. Applies the Part 2 flagging rule.
4. Selects flagged categories.
5. Drafts factual messages using the Part 3 template.
6. Holds drafts for human approval.
7. Stops when validation fails.

The runner does **not** automatically send messages.

---

## End-to-End Data Flow

```text
data/resellers.csv
data/orders.csv
        ↓
data/meesho_reseller.db
        ↓
Part 1 — SQL Analytics
        ↓
monthly_category_revenue.csv
        ↓
Part 2 — Validation + MoM Growth
        ↓
Flagged categories
        ↓
Part 3 — Narrative Templates
        ↓
Factual draft messages
        ↓
Part 4 — Mock Agent Runner
        ↓
Human approval required
```

---

## Workflow Pattern Mapping

### Part 1 → Part 2

Part 1 → Part 2 mirrors the workflow pattern:

> **Compute real numbers via SQL first, then hand off.**

SQL calculates the verified business metrics before the growth engine processes them.

### Part 2 → Part 3

Part 2 → Part 3 follows:

> **Validate and classify before narrating.**

Only validated data and calculated growth results are passed into the narrative layer.

### Part 3 → Part 4

Part 3 → Part 4 follows:

> **Use reusable templates, then automate the reporting flow.**

The narrative layer provides a controlled template that the mock agent runner fills using verified numbers.

### Part 4

Part 4 mirrors:

> **Intake → Summary → Report Draft → Validate**

The runner validates the feed, summarizes changes, drafts messages, and holds them for human approval.

---

## Zero API Keys

The entire project runs locally using:

* Python
* SQLite
* CSV files
* Deterministic calculations
* Deterministic narrative templates

No OpenAI API key, external LLM, paid service, or internet connection is required to run the pipeline.

---

## Repository Structure

```text
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db

part1_sql/
├── queries.sql
├── run_queries.py
└── output/
    ├── monthly_category_revenue.csv
    ├── region_revenue.csv
    ├── top_resellers.csv
    ├── inactive_resellers.csv
    ├── count_demonstration.csv
    └── june_delivered_aov.csv

part2_engine/
├── growth_engine.py
├── test_growth_engine.py
└── fixtures/

part3_narrative/
├── prompt_pack.md
├── narrative_report.md
└── masking.py

part4_agent/
├── agent_spec.md
├── mock_agent_runner.py
└── fixtures/

README.md
```

---

## Reliability Rules

The project follows these rules:

* Validate data before processing.
* Compute business metrics deterministically.
* Do not invent unsupported numbers.
* Keep narrative generation grounded in verified inputs.
* Mask reseller identities when required.
* Stop processing invalid feeds.
* Do not automatically send messages.
* Require human approval before external communication.

---

## Submission

Submit the **public GitHub repository link only**.
