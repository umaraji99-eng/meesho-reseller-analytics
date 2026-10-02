# Reliable AI Narrative & Prompt-Pack Report

## 3.2 — Worked Narrative Report

### May — Ethnic Wear

#### Context

The analysis measures month-over-month revenue for the **Ethnic Wear** category, comparing **May with April**.

#### Insight

**Fact:** Ethnic Wear revenue increased by exactly **77.1% MoM** from April to May.

#### Implication

**Hypothesis:** The increase may reflect stronger demand or reseller activity during May, but the supplied revenue data alone does not establish the cause.

**Action:** The regional manager should compare May Ethnic Wear order activity and reseller-level performance with April before deciding whether the increase should be treated as a sustained trend.

---

### June — Ethnic Wear

#### Context

The analysis measures month-over-month revenue for the **Ethnic Wear** category, comparing **June with May**.

#### Insight

**Fact:** Ethnic Wear revenue decreased by exactly **58.74% MoM** from May to June. The verified MoM result is **-58.74%**.

#### Implication

**Hypothesis:** The decline may be related to reduced demand or lower reseller activity, but the supplied revenue data alone does not establish the cause.

**Action:** The regional manager should check June Ethnic Wear order activity and reseller-level performance against May to identify whether the decline was concentrated in particular regions or resellers before taking corrective action.

---

## Self-Score Against the 4-Criterion Refinement Checklist

### 1. Specificity — Pass

Both narratives use the exact **Ethnic Wear** category name, the correct months, and the exact verified MoM percentages of **77.1%** and **-58.74%**.

### 2. Audience Fit — Pass

The narratives are written for a regional manager and focus on business interpretation and next actions rather than implementation or engineering details.

### 3. Completeness — Pass

Each narrative contains all three required sections: **Context, Insight, and Implication**.

### 4. Actionability — Pass

Each narrative gives a concrete next step: compare order activity and reseller-level performance with the previous month to identify where the movement occurred.

---

# 3.3 — Chart-Choice Justification

## Question 1 — Which month had the highest total revenue?

**Recommended chart: Column chart.**

This is a **univariate comparison** because the business question compares one measure, total revenue, across one categorical dimension, month. A column chart makes the three monthly revenue values easy to compare within about 10 seconds. The y-axis should start at zero so that the differences in revenue are not visually exaggerated. There is only one series, so a legend is unnecessary. A 3D chart should be avoided because it can make comparisons harder.

The verified values are:

- April: INR 419417.43
- May: INR 444594.25
- June: INR 398055.24

---

## Question 2 — What percentage share does Ethnic Wear represent of April's total revenue?

**Recommended chart: Donut chart.**

This is a **univariate part-to-whole question** because the objective is to show Ethnic Wear's share of April's total revenue. A donut chart can communicate the part-to-whole relationship quickly when there are only a small number of relevant components. The chart should clearly label the Ethnic Wear share as **24.92%** and avoid unnecessary 3D effects. Because this is a single part being compared with the remainder, a legend should only be used if it improves identification of multiple displayed segments.

Verified values:

- Ethnic Wear April revenue: INR 104520.77
- April total revenue: INR 419417.43
- Ethnic Wear share: 24.92%

---

## Question 3 — How do the four regions compare on total revenue?

**Recommended chart: Bar chart.**

This is a **univariate comparison** because the question compares one measure, total revenue, across one categorical dimension, region. A horizontal bar chart makes the four regional values easy to compare and keeps the region names readable. The numerical axis should start at zero to avoid exaggerating differences, and no 3D effect should be used. Because there is only one revenue series, a legend is unnecessary.

The verified regional revenue values from Part 1 are:

- North: INR 337125.46
- South: INR 316736.68
- East: INR 275098.45
- West: INR 333106.33

---

# 3.4 — Masking Policy

External-facing narratives must never expose raw reseller names.

A reseller must instead be represented using:

`alias_for(reseller_id)`

The required alias format is:

`ALIAS-{reseller_id[3:]}`

Examples:

- `RS019` → `ALIAS-19`
- `RS006` → `ALIAS-06`

The narrative may reference the reseller's region together with the coded alias, but must never expose the raw reseller name.

## Top-reseller narrative

**Fact:** The Part 1 top-reseller results identify five high-spend resellers across the verified regional data.

For external-facing communication, the resellers are represented only by coded aliases and region:

- **Mumbai — ALIAS-19**
- **Mumbai — ALIAS-22**
- **Hyderabad — ALIAS-12**
- **Lucknow — ALIAS-06**
- **Jaipur — ALIAS-05**

**Action:** The regional manager should use these aliases when discussing the top-reseller results in any external-facing summary.

No raw reseller names are included in this narrative.

---

## Masking Tests

Required positive test:

`alias_for("RS019") == "ALIAS-19"`

Required negative-case test:

`assert_no_raw_names_leak` must return `False` when the text still contains the raw name:

`Mumbai Reseller 1`

Required final test:

`assert_no_raw_names_leak` must return `True` for the final masked top-reseller narrative.