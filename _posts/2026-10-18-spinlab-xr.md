---
layout: post
title: "SpinLab XR: Rotor Balancing in Virtual Reality"
date: 2026-10-18 00:00:00 -0700
permalink: /2026/10/18/spinlab-xr/
lead: "A virtual engineering lab for learning how to measure vibration and balance a spinning rotor."
description: "SpinLab XR brings a rotor-balancing station to Meta Quest 2, combining physical interaction, scientific measurement methods, and a narrated learning experience."
article_wide: true
image: /assets/projects/spinlab-xr/station.png
---

An off-center mass can make a spinning assembly shake. Correcting it takes more
than adding a weight: you need to measure the vibration, understand its timing,
and determine where a correction will help. I built **SpinLab XR** to make that
process something you can explore with your hands.

The app runs directly on Meta Quest 2. Using the Touch controllers, you load a
rotor, lower the guard, turn a probe micrometer, and adjust correction mass and
angle. A monitor beside the bench displays captured vibration signals and how
the response changes with rotational speed.

<figure class="experiment-figure">
  <img src="{{ '/assets/projects/spinlab-xr/station.png' | relative_url }}" alt="Virtual rotor-balancing bench with a raised guard, rotor cassette, probe micrometer, adjustment knobs, side monitor, and operating console." width="1728" height="1200" loading="lazy">
  <figcaption>The virtual station, shown in a desktop view of the Quest app.</figcaption>
</figure>

A 38-step narrated course starts with the basics and introduces each concept
when you need it. Small prompts appear beside the next control; completing the
task advances the lesson immediately. You establish a baseline, measure the
effect of known trial masses in two correction planes, calculate a correction,
and take a fresh measurement to check the result. Stopping, fault recovery,
repeatability, and saving a test report are part of the exercise, too.

Behind the station is a numerical model with tachometer-referenced vibration
analysis and single- or two-plane influence-coefficient balancing. The
measurements are synthetic, but the experiment follows a real engineering
workflow: prepare, measure, identify, correct, and verify.

Built with **Godot and OpenXR** and tested on Quest 2, SpinLab XR combines
mechanical interaction, signal analysis, and guided instruction in one offline
lab. It offers a way to rehearse a complex procedure before using physical
equipment.

[Explore the project on GitHub](https://github.com/jewbee2000/spinlab-xr-public)
or [download the Quest APK and installation guide](https://github.com/jewbee2000/spinlab-xr-public/releases/tag/v0.8.0).
