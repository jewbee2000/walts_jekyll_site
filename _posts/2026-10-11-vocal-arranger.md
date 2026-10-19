---
layout: post
card_title: Vocal Arranger
thumbnail: /assets/images/project-cards/vocal-arranger.webp
thumbnail_alt: Five-part score for the Velvet Conversation arrangement
title: "Building a vocal arranger with AI"
date: 2026-10-11 00:00:00 -0700
permalink: /2026/10/11/vocal-arranger/
lead: "Using Codex to turn a lead sheet and musical instructions into a five-part a cappella arrangement."
description: "I wanted to arrange a song for my a cappella group. Here is what I learned working with Codex, with a completed Diamonds score and Sinsy sung demo."
article_wide: true
---

<style>
.vocal-arranger-media audio { display: block; width: 100%; margin: 1rem 0; }
.vocal-arranger-media img { display: block; max-width: 100%; height: auto; }
.vocal-arranger-media details { margin-top: 1rem; }
.vocal-arranger-media summary { cursor: pointer; font-weight: 600; }
.vocal-arranger-media details p { margin-top: 1.5rem; }
</style>

I sing in [an a cappella group](https://youtu.be/ictqLjDXr2Y), and I wanted to
arrange a song for us. That was the inspiration for this project. I wondered
whether Codex could help me turn a lead sheet and some plain-English
instructions into a five-part a cappella arrangement. I tried it with Paul
Simon's “Diamonds on the Soles of Her Shoes,” and I was pleasantly surprised
by what came back.

A lead sheet supplies a song's melody, chords and lyrics. I wanted the software
to develop that foundation into parts for soprano, alto, tenor, baritone and
bass. I specified eleven singers sharing those five parts: one soprano, four
altos, and two each on tenor, baritone and bass. I asked for intermediate
difficulty, ten different arrangements, and three finalists with printable
scores, editable notation, rehearsal files and simulated singing.

I worked with Codex to build the software, giving it musical goals and letting
it choose the detailed parameters. After the first batch, I asked for one
revision: more rhythmic variety and syncopation, occasional backing responses
using words from the song, and more sharing of complete lead phrases among the
voices. I wanted the backing parts to have something interesting to do, too.

My workflow had four steps:

1. **Read the music.** The software turned the lead sheet into a precise list
   of notes, durations, words and chords that it could work with.
2. **Give the voices different jobs.** Codex wrote rules for bass movement,
   harmony, accompaniment rhythms, lead handoffs and changes in texture. It
   developed the short supplied edition into arrangements a little over three
   minutes long, with introductions, repeated sections and endings.
3. **Check and compare.** Software checked things such as whether a bar added
   up correctly, a part stayed within its assumed range, or the original words
   and melody were preserved. Separate AI reviewers assessed the ten candidates
   for source fidelity, harmony, rhythm, singability and musical coherence.
4. **Make the results usable.** The project exported scores and rehearsal
   tracks, then used the [Sinsy singing synthesizer](https://sinsy.sp.nitech.ac.jp/en)
   to make vocal demonstrations from the written parts.

What impressed me was having several complete, editable arrangements to work
with after that one revision. The three finalists were “Velvet Conversation,”
“Street-Corner Replies” and “Dancing Counterlines.” I could see my requests
showing up in the music. I'd still want musicians to try the parts and tell me
what works; an AI review score only goes so far.

The Sinsy sung demos sounded hilarious. I noticed a bug where the bass, baritone
and tenor weren't singing the lyrics. The alto and soprano did sing them,
but with what sounded to me like German accents. It was a very funny way to
preview the music.

Here's “Velvet Conversation,” one of the completed arrangements, along with
its matching sung demo. You can listen and follow the score below.

<figure class="experiment-figure vocal-arranger-media">
  <figcaption><strong>Velvet Conversation — Sinsy sung demo</strong></figcaption>
  <audio controls preload="metadata" aria-label="Velvet Conversation sung demo">
    <source src="/assets/projects/vocal-arranger/diamonds-velvet-conversation.mp3" type="audio/mpeg">
    <a href="/assets/projects/vocal-arranger/diamonds-velvet-conversation.mp3">Listen to the sung demo</a>.
  </audio>
  <p><a href="/assets/projects/vocal-arranger/diamonds-velvet-conversation.mp3">Open or download the sung demo</a> (3:07).</p>
</figure>

<figure class="experiment-figure vocal-arranger-media">
  <figcaption><strong>Diamonds on the Soles of Her Shoes — Velvet Conversation</strong><br>Complete five-part arrangement</figcaption>
  <a href="/assets/projects/vocal-arranger/diamonds-velvet-conversation.pdf">
    <img src="/assets/projects/vocal-arranger/score/page-01.png" alt="Velvet Conversation score, page 1 of 14" width="100%">
  </a>
  <p>Page 1 of 14. Open the pages below to follow the complete arrangement.</p>
  <details>
    <summary>View score pages 2–14</summary>
    <p>Page 2 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-02.png" alt="Velvet Conversation score, page 2 of 14" loading="lazy" width="100%">
    <p>Page 3 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-03.png" alt="Velvet Conversation score, page 3 of 14" loading="lazy" width="100%">
    <p>Page 4 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-04.png" alt="Velvet Conversation score, page 4 of 14" loading="lazy" width="100%">
    <p>Page 5 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-05.png" alt="Velvet Conversation score, page 5 of 14" loading="lazy" width="100%">
    <p>Page 6 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-06.png" alt="Velvet Conversation score, page 6 of 14" loading="lazy" width="100%">
    <p>Page 7 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-07.png" alt="Velvet Conversation score, page 7 of 14" loading="lazy" width="100%">
    <p>Page 8 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-08.png" alt="Velvet Conversation score, page 8 of 14" loading="lazy" width="100%">
    <p>Page 9 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-09.png" alt="Velvet Conversation score, page 9 of 14" loading="lazy" width="100%">
    <p>Page 10 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-10.png" alt="Velvet Conversation score, page 10 of 14" loading="lazy" width="100%">
    <p>Page 11 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-11.png" alt="Velvet Conversation score, page 11 of 14" loading="lazy" width="100%">
    <p>Page 12 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-12.png" alt="Velvet Conversation score, page 12 of 14" loading="lazy" width="100%">
    <p>Page 13 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-13.png" alt="Velvet Conversation score, page 13 of 14" loading="lazy" width="100%">
    <p>Page 14 of 14</p>
    <img src="/assets/projects/vocal-arranger/score/page-14.png" alt="Velvet Conversation score, page 14 of 14" loading="lazy" width="100%">
  </details>
  <p><a href="/assets/projects/vocal-arranger/diamonds-velvet-conversation.pdf">Open or download the complete score</a>.</p>
</figure>

The harder problem appeared when I tried starting with a recording instead of
a known-good lead sheet. A waveform or MP3 contains overlapping sounds;
producing readable music requires identifying the melody and chords, finding
the beat and bar lines, and deciding how performed timing should be written.
A singer's slight delay, a swung pair of notes and a deliberate offbeat entrance
need different interpretations. A transcription can capture plausible pitches
yet lose the rhythm and feel that make the song recognizable to a musician.
That helped me understand the limitations described by the tools themselves: Spotify's
[Basic Pitch](https://github.com/spotify/basic-pitch) says it works best on one
instrument at a time, while [Sheet Sage's documentation](https://github.com/chrisdonahue/sheetsage#improving-results)
describes tempo and downbeat errors that can distort the notation. In my
experiments, getting a trustworthy, intuitive lead sheet remained the weak link.

I came away impressed by how far I could get with Codex, a good lead sheet and
a little feedback. I also came away with a much greater appreciation for the work
involved in writing that lead sheet in the first place. I've
[released the code on GitHub](https://github.com/jewbee2000/vocal-arranger),
including an original demo that others can try. The code repository is separate
from the “Diamonds” score and sung example included here.
