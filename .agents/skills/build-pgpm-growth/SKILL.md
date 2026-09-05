---
name: build-pgpm-growth
description: Create the permanent PgPM Growth section for the DC Daily Brief. Use whenever generating, drafting, reviewing, or validating a daily edition, or when Robert asks for progressive professional-development teaching for his PgPM role at Equinix in the data-center industry. Produce two connected lessons, six researched sources, and one optional short Daily Action while advancing beyond recent editions.
---

# Build PgPM Growth

Create Section 11 as a deliberate professional-development curriculum. Teach role-relevant judgment and reusable practices; do not turn the section into another news roundup.

## Prepare

1. Read [references/curriculum.md](references/curriculum.md) completely.
2. Search all dated briefs for prior `## PgPM Growth` sections.
3. Review the topics, maturity levels, actions, and URLs in the latest 30 editions, plus the edition manifest. Record the new pairing and recurring hypothetical case in edition metadata and map the six resources to the two topics in the research log.
4. Select two connected topics that advance the curriculum. Prefer a connection to that day's brief when it is genuinely useful.
5. Do not repeat a topic at the same maturity level or the same exercise from those 30 editions. Reuse authoritative URLs when the application advances; explain the progression. Metadata records teaching, never assumed mastery.

## Research

- Find exactly six distinct, directly relevant public sources: three per topic.
- Blend authoritative sources—PMI, standards bodies, established industry organizations, primary research, or official technical guidance—with practical articles, examples, or templates.
- Prefer direct source pages over search results, aggregators, or generic homepages.
- Verify that every link opens and supports the associated teaching.
- Use current material when the topic is time-sensitive; use durable guidance when recency adds no value.
- Do not claim or imply knowledge of confidential Equinix policies, systems, customers, or incidents. Frame company-specific applications as recommendations or hypothetical examples.

## Write

Append this section after `## Program & PM`:

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

Keep the two lessons substantive and the four resources concise. Write for Robert as an established technical PgPM spanning physical facilities, logical systems, and cross-functional delivery. Include a worked hypothetical example before a short optional exercise; connect the two lessons to the edition's technical context when useful. Explain unfamiliar concepts plainly without talking down to him.

## Validate

- Confirm `PgPM Growth` is Section 11 and follows `Program & PM`.
- Confirm there are two connected topics, six unique links, three links per topic, and one Daily Action.
- Confirm the Daily Action is time-boxed, useful, and does not create an external side effect.
- Confirm the content advances beyond recent editions and contains no invented internal Equinix claims.
- Confirm all six links render with `target="_blank"` after building the edition.
