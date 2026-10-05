---
layout: post
title: "FixtureForge: Checking Tool Access in CAD"
date: 2026-10-04 00:00:00 -0700
permalink: /2026/10/04/fixtureforge/
lead: "Inspect whether a simplified tool can follow a declared path through a fixture or small assembly."
description: "Inspect whether a simplified tool can follow a declared path through a fixture or small assembly. Part of Walter Teitelbaum's two-day AI engineering experiment."
article_wide: true
experiment_project: true
project_id: fixtureforge
image: /assets/files/agentic-engineering/fixture-access.jpg
---

A part can fit inside a fixture while leaving no route for a screwdriver or connector to reach it. [FixtureForge](https://github.com/jewbee2000/fixtureforge) checks that narrower assembly question: can a simplified tool follow a specified straight path without intersecting the parts around it?

I see this as a small, inspectable integration of existing CAD tools. CadQuery supplies the geometric operations; FixtureForge adds an input contract, repeatable checks, and reports identifying the obstructing part. Its [comparison with CadQuery, build123d, and CADCLAW](https://github.com/jewbee2000/fixtureforge/blob/main/docs/BASELINE.md) illustrates why checking only the starting and ending positions can miss an obstacle in between.

## How it is used

The intended user is an engineer checking access in a fixture or small assembly. After following the [installation and demo instructions](https://github.com/jewbee2000/fixtureforge#reproduce-locally), the workflow is:

1. Supply each part as a single-solid STEP file in millimetres.
2. Define a box or cylinder representing the tool, its starting and ending positions, and the parts present at that assembly stage in the [JSON access contract](https://github.com/jewbee2000/fixtureforge/blob/main/docs/PUBLIC_API.md).
3. Run the inspection and open the local HTML report. The check considers the volume occupied along the whole path.

The supplied sensor-clamp demonstration deliberately routes a tool through the upper clamp. Its report shows approximately **382.377 mm³** of overlap. The demo also includes a corrected path, making it possible to inspect both outcomes.

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/fixture-access.jpg"><img src="/assets/files/agentic-engineering/fixture-access.jpg" alt="FixtureForge report showing a deliberately obstructed tool path through a sensor clamp, with 382.377 cubic millimetres of overlap." loading="lazy"></a>
  <figcaption>A deliberately seeded obstruction. Purple shows the swept envelope; this is a geometry replay, not a physical measurement.</figcaption>
</figure>

## Validation and limits

The publication audit passed **61 tests**; four inspect retained campaign evidence rather than rerunning those campaigns. The [audit evidence](https://github.com/jewbee2000/fixtureforge/tree/main/evidence/publication-audit) records the checks. The software is runnable, with setup verified on Windows and Python 3.12.

I would use it to investigate a declared access path, not approve an assembly. It supports straight translations and conservative envelopes, which can over-report collisions. It does not plan rotating motions or establish clamping force or material strength. The clamp has not been physically validated, and usefulness to an independent practitioner remains untested.
