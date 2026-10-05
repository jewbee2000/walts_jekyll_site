---
layout: page
title: AI Engineering Experiment
permalink: /2026/10/04/agentic-engineering-experiment/
description: Four concise project notes from Walter Teitelbaum's two-day experiment with AI engineering agents.
article_wide: true
---

# Four projects from a two-day experiment

I’ve replaced the combined essay with a short article for each project. Each explains what the tool does, how to try it, and what its validation establishes.

{% for project in site.data.experiment-projects %}
- [{{ project.name }}]({{ project.url | relative_url }}) — {{ project.summary }}
{% endfor %}

The [evidence manifest](/assets/files/agentic-engineering/evidence-manifest.json) records the repository snapshots, test results, and figure provenance for the series.
