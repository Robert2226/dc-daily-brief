---
name: build-pgpm-growth
description: Create the permanent PgPM Growth section for the DC Daily Brief. Use whenever generating, drafting, reviewing, or validating a daily edition, or when Robert asks for progressive professional-development teaching for his PgPM role at Equinix in the data-center industry. Produce two connected lessons, six researched sources, and one optional short Daily Action while advancing beyond recent editions.
---

# Build PgPM Growth

Create the third subject on the separate Deep Dives page as a deliberate professional-development curriculum. Format-2 historical editions retain Section 11. Teach role-relevant judgment and reusable practices; do not turn the section into another news roundup.

## Prepare

1. Read [references/curriculum.md](references/curriculum.md) completely.
2. Read the latest lesson and the last 30 editions' topic metadata in the edition manifest.
3. Open older lessons only where a proposed topic overlaps and the prior maturity level, action or URLs need checking; do not scan all full briefs each run. Record the new pairing and recurring hypothetical case in edition metadata and briefly map the six resources to the two topics in the research log.
4. Select two connected topics that advance the curriculum. Prefer a connection to that day's brief when it is genuinely useful.
5. Do not repeat a topic at the same maturity level or the same exercise from those 30 editions. Reuse authoritative URLs when the application advances; explain the progression. Metadata records teaching, never assumed mastery.

## Research

- Find exactly six distinct, directly relevant public sources: three per topic.
- Blend authoritative sources—PMI, standards bodies, established industry organizations, primary research, or official technical guidance—with practical articles, examples, or templates.
- Prefer direct source pages over search results, aggregators, or generic homepages.
- Verify that every link opens and supports the associated teaching.
- Use current material when the topic is time-sensitive; use durable guidance when recency adds no value.
- Use publicly reported incidents and remediation as teaching cases when pertinent. Distinguish sourced facts, uncertain causal claims, engineering interpretations and hypothetical leadership examples; never infer an unpublished root cause. Incident cases are optional, not a daily quota.
- Do not claim or imply knowledge of confidential Equinix policies, systems, customers, or incidents. Frame company-specific applications as recommendations or hypothetical examples.

## Write

In format 3, append this source section after `## Physical Deep Dive` and `## Logical Deep Dive`. Display it as the third learning subject, with its metadata title. Professional growth stands on its own; do not force a tie-in to a news story. New lean-v1 editions have no Program & PM news section and no study links from News. An optional, relevant `news:` reference from a lesson does not count toward the six external resources:

```markdown
## PgPM Growth
- **<Topic 1 lesson headline>** — <A concise lesson tailored to PgPM work in data-center programs, including why it matters and how to apply it.> [<Primary source>](<URL 1>)
- **<Topic 2 lesson headline>** — <A connected lesson at the appropriate maturity level, including why it matters and how to apply it.> [<Primary source>](<URL 2>)
- **Resource · <Topic 1 resource>** — <One sentence explaining its practical use.> [<Source>](<URL 3>)
- **Resource · <Topic 1 resource>** — <One sentence explaining its practical use.> [<Source>](<URL 4>)
- **Resource · <Topic 2 resource>** — <One sentence explaining its practical use.> [<Source>](<URL 5>)
- **Resource · <Topic 2 resource>** — <One sentence explaining its practical use.> [<Source>](<URL 6>)
> **Daily Action · <Action title>.** <One optional, safe, concrete, short time-boxed exercise that produces a useful artifact or practices a behavior today. Do not send messages or modify external systems.>
```

From September 21 onward, aim for 350–450 words total, including resources, worked example
and Daily Action. Keep each teaching entry to one focused paragraph and each resource
annotation to one short sentence. Use one compact example connecting both topics, not
multiple scenarios or repeated summaries. Retain all six sources. Write for Robert as an
established technical PgPM spanning physical facilities, logical systems and delivery;
connect to the technical context only when useful. Explain unfamiliar concepts plainly.

## Validate

- Confirm `PgPM Growth` is the third learning subject and follows the physical and logical source sections. Historical format 2 retains Section 11 after Program & PM.
- Confirm there are two connected topics, six unique external links, three links per topic, and one Daily Action.
- Confirm the Daily Action is time-boxed, useful, and does not create an external side effect.
- Confirm the content advances beyond recent editions and contains no invented internal Equinix claims.
- Confirm all six links render with `target="_blank"` after building the edition.
