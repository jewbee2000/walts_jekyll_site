---
layout: post
title: "AbyssBench: Checking Controller Timing"
date: 2026-10-04 00:00:00 -0700
permalink: /2026/10/04/abyssbench/
lead: "Replay controller events and check whether the recorded response satisfies an explicit timing contract."
description: "Replay controller events and check whether the recorded response satisfies an explicit timing contract. Part of Walter Teitelbaum's two-day AI engineering experiment."
article_wide: true
experiment_project: true
project_id: abyssbench
image: /assets/files/agentic-engineering/abyss-timing.png
---

A controller can issue the right command while the machine continues doing the wrong thing. [AbyssBench](https://github.com/jewbee2000/abyssbench) explores that distinction: when a sensor reading becomes stale or an actuator stops responding, did the controller issue the required response before its deadline—and does the recorded evidence actually establish that?

I see it as a small tool for engineers developing control logic or reviewing test logs. It combines pytest with [RTAMT](https://github.com/nickovic/rtamt), an existing temporal monitoring library. Its contribution is the surrounding workflow: explicit timing rules, repeatable traces, and evidence that keeps commands separate from measured behavior.

## How it is used

I would start with the [installation and offline demo](https://github.com/jewbee2000/abyssbench#try-it-locally-powershell-python-312). The [public API walkthrough](https://github.com/jewbee2000/abyssbench/blob/main/docs/API.md) offers two starting points: import a supported JSONL or explicitly mapped CSV trace, or supply a trusted Python controller to the example simulator. Define acceptable ranges, measurement age, response deadlines, and prohibited transitions; run the check; then inspect each rule's verdict and supporting events. Incomplete observation windows remain inconclusive. A recent packet carrying an old measurement does not become fresh just because it arrived recently.

## A small example

The pump-and-valve example makes the distinction visible. The simulated valve sticks closed at 500 milliseconds. At 1,010 milliseconds, the controller detects the persistent mismatch and issues pump-off and valve-open commands. The valve remains closed. The response check can pass because the required commands were issued; that says nothing about mechanical recovery.

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/abyss-timing.png"><img src="/assets/files/agentic-engineering/abyss-timing.png" alt="Simulation timeline: a valve sticks at 500 milliseconds and the controller issues safe commands at 1,010 milliseconds while the valve remains closed." loading="lazy" width="1920" height="1120"></a>
  <figcaption>Recorded simulation events: commanded and actual valve positions remain separate.</figcaption>
</figure>

## Validation and limits

The original release passed 116 tests. The publication review nevertheless found two edge cases: a single observation could crash the monitor, and a command preceding a fault at the same timestamp could incorrectly satisfy its response rule. Both were repaired; the publication audit passed **124 tests**. The [audit preserves the failing cases](https://github.com/jewbee2000/abyssbench/blob/main/evidence/publication-audit/README.md).

The tool supports one clock and trusted controller callbacks; its fluid model is uncalibrated, with no hardware validation. A real trace and an independent engineer's trial are the next useful tests.
