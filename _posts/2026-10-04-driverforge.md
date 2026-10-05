---
layout: post
title: "DriverForge: Testing Instrument Drivers Without Hardware"
date: 2026-10-04 00:00:00 -0700
permalink: /2026/10/04/driverforge/
lead: "A small Python tool for replaying protocol faults and inspecting how an instrument driver responds."
description: "A small Python tool for replaying protocol faults and inspecting how an instrument driver responds. Part of Walter Teitelbaum's two-day AI engineering experiment."
article_wide: true
experiment_project: true
project_id: driverforge
image: /assets/files/agentic-engineering/driver-signed-failure.png
---

An instrument driver translates between software and a physical device. That translation can fail even when a response looks perfectly reasonable. For [DriverForge](https://github.com/jewbee2000/driverforge), I asked Codex to investigate a useful addition to existing instrument libraries, establish acceptance checks, and preserve failed examples.

The result is a small Python tool for engineers maintaining instrument drivers, particularly when the hardware is unavailable in continuous integration. It supplies a simulated communication channel, controlled faults, and reports showing the exact bytes exchanged alongside the expected and observed results.

## How it is used

The workflow starts with an explicit protocol contract and expected readings. An engineer connects a driver to the test transport, schedules faults such as fragmented responses or timeouts, then inspects the resulting HTML or JSON report. The [public API](https://github.com/jewbee2000/driverforge/blob/main/docs/PUBLIC_API.md) also provides a pytest fixture. One integration uses an unchanged PyMeasure Agilent34410A driver through its existing adapter interface. [PyMeasure already supports protocol testing](https://pymeasure.readthedocs.io/en/stable/dev/adding_instruments/tests.html); DriverForge's contribution is the reusable fault schedules and detailed diagnostic records.


After following the [installation instructions](https://github.com/jewbee2000/driverforge#install-and-demonstrate) and activating the environment, run:

```text
python -m driverforge demo --offline --output artifacts/demo
```

Open `artifacts/demo/report.html` to explore the evidence.

## A small example

One example makes the purpose concrete. A deliberately broken reference driver interprets hexadecimal `FB2E` as an unsigned temperature value, producing **643.02 °C** instead of **−12.34 °C**. The report preserves the response bytes and the incorrect interpretation, making the mistake traceable.

<figure class="experiment-figure compact">
  <a href="/assets/files/agentic-engineering/driver-signed-failure.png"><img src="/assets/files/agentic-engineering/driver-signed-failure.png" alt="DriverForge report showing expected minus 12.34 degrees Celsius and observed 643.02 after a deliberately incorrect unsigned decode." loading="lazy" width="755" height="1060"></a>
  <figcaption>A seeded decoding defect under synthetic replay; no hardware measurement is involved.</figcaption>
</figure>

## Validation and limits

The publication audit passed **100 tests**. That includes six regressions added during publication review after discovering that report comparison missed changes to completion status and source evidence. Separately, the offline demo passes 39 reference cases and rejects six deliberately introduced defects.

I would treat this as a starting point for driver development. No physical instruments or independent practitioners have validated it. The reference protocols are fictional, Windows/Python 3.12 is the verified environment, and two synthetic fault cases still fail the upstream integration's stated consumer contract. Those failures remain visible in the [audit evidence](https://github.com/jewbee2000/driverforge/tree/main/evidence/article-audit).
