---
layout: post
title: "I Asked Codex to Choose Its Own Engineering Projects"
date: 2026-10-04 00:00:00 -0700
permalink: /2026/10/04/agentic-engineering-experiment/
lead: "The agents moved faster than I could follow. The experience changed where I think human engineering judgment belongs."
description: "Walter Teitelbaum's experiment with Codex: four hardware-focused engineering tools, requirements-first development, independent checks, and the failures behind the passing tests."
article_wide: true
image: /assets/files/agentic-engineering/rfq-plate.png
---

The most frustrating part of this experiment was my own inability to keep up.

I had asked Codex to propose and build several engineering projects. It was researching existing tools, rationalizing requirements, implementing software, running tests, and producing reports faster than I could follow the work. I felt incompetent at supervising an experiment I had initiated. The implementation capacity was there; my capacity to absorb and judge the output had become the constraint.

That experience has pushed me toward a particular view of agentic engineering: the most valuable place for humans to collaborate is the system specification and test plan. Requirements are the essence of successful project-driven engineering. They define the problem, the intended behavior, the evidence of success, and the boundaries of the work. When execution becomes easier to delegate, the quality of that definition matters even more.

Across October 3–4, I asked Codex to research, propose, plan, and implement software projects related to my interests in hardware, manufacturing, and test engineering. I wanted to see how far an agent could get with limited implementation guidance. For this experiment, I also let it author and rationalize its own requirements and acceptance criteria. That made the assignment unusually revealing: it had to choose worthwhile problems, define what success meant, and produce evidence that its software met those definitions.

The result was four runnable Python projects: **DriverForge**, **AbyssBench**, **FixtureForge**, and **RFQFuzz**. They came with tests, command-line interfaces, demonstrations, failure records, and requirements documents. They also came with limitations that matter much more than the number of files in their repositories.

Agentic coding changes the economics of trying an engineering idea. A substantial first implementation becomes easier to obtain, while deciding what deserves to exist and how to judge it becomes a larger share of the work. Ben Thompson makes a related distinction in his discussion of [software survival](https://stratechery.com/2026/microsoft-and-software-survival/): a product's value includes integration, support, and the commitment to keep it working. My four repositories are an experiment at the beginning of that commitment.

## Why these problems interested me

My background sits where software meets physical equipment. I enjoy controls, instrumentation, fixtures, manufacturing processes, and the awkward details that appear when something has to work outside a demonstration. My existing portfolio includes [robotic gardening](/2021/07/25/Automated-Pruning-for-Polyculture/) and [printed bicycle components](/2025/04/01/3D-Printed-Bicycle-Components/). A drawing, a controller, and a measurement all interest me because each makes a claim about the physical world that can eventually be checked.

The immediate motivation was to make more of that interest visible in my portfolio. I initially asked for five project proposals informed by my experience and research into open-source tools. Then I asked Codex to select three that it could implement with minimal guidance. The drawing-review idea arrived later and became the fourth project.

There is an obvious trap in that assignment. Ask an agent for impressive portfolio projects and it can produce impressive-sounding project plans. A name, an architecture diagram, and a long feature list can give an idea the appearance of substance before anyone has established a reason to build it.

I pushed back before implementation. One of my messages said:

> “I want to implement projects that are actually useful.”

I asked the agent to write explicit MoSCoW requirements—Must, Should, Could, and Won't—with rationales and acceptance criteria. I also asked it to investigate existing tools and change the scope when the original contribution was weak. For the drawing project, I explicitly made an interesting, defensible problem more important than preserving my initial idea.

Those interventions changed the projects. DriverForge became primarily a fault-testing toolkit for instrument drivers. AbyssBench became a controller replay and timing-checking tool. FixtureForge concentrated on tool and connector access. RFQFuzz became a regression toolkit for reviewers. The common theme was verification at an engineering interface: bytes crossing a protocol boundary, events arriving at a controller, a tool moving through a fixture, or information disagreeing across a drawing package.

That was a sensible inference from my interests. It was also a narrower achievement than discovering four entirely new software categories.

## The experiment was in the instructions

I gave the first three implementation chats substantially the same kickoff instructions. Each agent had to inspect its environment, create a local Python environment, investigate existing tools, establish acceptance checks, preserve useful failures, and finish with a reproducible consumer walkthrough. Routine decisions were delegated. Publication was a later step.

The most consequential part of the prompt was this:

> “Establish independent acceptance checks, preserve failed examples, and commit coherent milestones locally.”

The repositories made those instructions durable. Requirements described the intended behavior. Acceptance documents described how it would be checked. Task records and milestone notes described what had actually happened. In RFQFuzz, a structured requirements file and dependency-linked task ledger made that relationship particularly explicit.

This matters because a coding agent works through repeated cycles of reading context, editing files, running commands, and interpreting the results. The useful unit of delegation is a change with a checkable outcome. A request such as “make the drawing tool robust” leaves considerable room for interpretation. “Reopen the exported STEP file and independently measure the hole diameter” gives the agent a concrete way to discover that its output is wrong.

The more elaborate RFQFuzz workflow used separate workers and a reviewer without inherited implementation conversation. It borrowed the idea of persistent tasks from Beads without installing Beads or Gas Town. More orchestration was a means to separate responsibilities; it was never an acceptance criterion by itself.

There is an important qualification to “minimal input.” I supplied a domain, challenged the framing, and required a disciplined process. Codex helped write the detailed prompts I subsequently used and supplied most of the requirements themselves. The eventual kickoff messages carried much more information than the initial request, but much of that information was also agent-authored. I was testing how well it could construct its own assignment as well as execute it.

For a dedicated project addressing a problem I actually needed solved, I would spend substantially more intellectual effort on those requirements before implementation. That would include the Won't list. If I fail to say that a hosted service, an automatic hardware write, or a particular feature is outside the product, an agent has room to interpret it as a helpful addition. An explicit exclusion is part of the design, every bit as much as a required capability.

This was an exploratory case study. I did not collect a controlled human-only baseline, reliable total token cost, or a comparable measure of my own implementation time. The work overlapped across chats, and publication involved another review and cleanup pass. I cannot turn the calendar interval into a defensible productivity multiplier.

## DriverForge: when a timeout does not mean nothing happened

[DriverForge](https://github.com/jewbee2000/driverforge) addresses a familiar testing problem: the real instrument is unavailable, inconvenient to automate, or too risky to use for fault injection. A driver still needs to handle malformed responses, wrong units, incomplete data, and communication failures.

The architecture separates the driver under test from a scripted transport and a conformance oracle—the code that decides what the correct behavior should have been. A run produces a report connecting a requirement and its source to the actual bytes sent and received. The useful output is a failure someone can diagnose.

Consider a write that changes an instrument's state. If the acknowledgement never arrives, the write may still have taken effect. Automatically trying again can repeat the physical action. DriverForge's synthetic protocols distinguish safe read retries from an uncertain write outcome. That distinction is small in code and substantial in consequence.

The retained signed-temperature demonstration is easier to see. The two bytes `fb 2e`, interpreted as a signed 16-bit value and scaled by 0.01, represent **−12.34 °C**. Treat them as unsigned and the result becomes **643.02 °C**. The report shows the specification, decoded value, and wire transcript together.

<figure class="experiment-figure compact">
  <a href="/assets/files/agentic-engineering/driver-signed-failure.png"><img src="/assets/files/agentic-engineering/driver-signed-failure.png" alt="DriverForge report showing expected minus 12.34 degrees Celsius and observed 643.02, with the byte transcript and signed scaling rule." loading="lazy" width="755" height="1060"></a>
  <figcaption>A deliberately broken unsigned-decoding implementation, caught by the conformance checks. This is a synthetic replay demonstration, not a measurement from hardware or an observed model failure.</figcaption>
</figure>

The original release passed **94 tests**, exercised **39 conformance cases**, and rejected **six deliberately faulty implementations**. It also integrated an existing PyMeasure Agilent driver. That integration is more persuasive than a second homegrown driver would have been, although its two retained failure cases express synthetic consumer requirements; they do not establish defects in the physical instrument. [Release evidence](https://github.com/jewbee2000/driverforge)

The agent correctly found that [PyMeasure already supports protocol testing](https://pymeasure.readthedocs.io/en/stable/dev/adding_instruments/tests.html). DriverForge's defensible contribution is reusable fault campaigns and explanations that connect a failure to its protocol contract. It is an integration tool in an existing ecosystem, with one public-driver integration demonstrating the idea. Broad driver coverage and hardware validation remain future work.

## AbyssBench: the order of events is part of the requirement

[AbyssBench](https://github.com/jewbee2000/abyssbench) asks whether a controller responded correctly and on time. It can replay recorded events or run a controller against repeatable scenarios, then explain the result in terms of engineering requirements.

A statement such as “shut down when the sensor becomes stale” conceals several decisions. Which timestamp determines age? Does a new sample arrive before or after the controller runs at the same timestamp? How long may the controller wait? If the recording ends before the deadline, is there enough evidence to decide?

These are architectural questions. They determine what the test means.

AbyssBench uses [RTAMT](https://github.com/nickovic/rtamt) to evaluate numeric range predicates. A Python event ledger checks response deadlines and preserves the ordering and history needed to explain each verdict. Missing evidence can produce an inconclusive result. A trace ending early must not quietly acquire a passing verdict.

The original release passed **116 tests** and recorded **21 Must requirements** as verified. Its property-based check was configured for **1,000 generated action/fault sequences**. The package includes pump-and-valve scenarios and a separate thermal example, plus interfaces for external controllers and imported traces. Those checks demonstrate a bounded software workflow. They do not validate a calibrated physical plant or certify a controller. [Implementation and evidence](https://github.com/jewbee2000/abyssbench)

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/abyss-timing.png"><img src="/assets/files/agentic-engineering/abyss-timing.png" alt="A synthetic valve sticks closed at 500 milliseconds. At 1,010 milliseconds the controller commands the valve open and pump off, but the simulated valve remains closed." loading="lazy" width="1920" height="1120"></a>
  <figcaption>A new plot of the retained synthetic replay: the valve sticks at 500 ms; detection and safe commands occur at 1,010 ms. The simulated valve remains closed. Passing a command-timing requirement does not establish actuator motion or physical safety.</figcaption>
</figure>

One of the most instructive development failures involved Boolean encoding in a temporal formula. The initial representation put a trigger on the zero boundary of a quantitative robustness calculation, where it could produce a misleading pass. The initial RTAMT comparison was changed to use positive and negative values for true and false. A sophisticated dependency had not removed the need to understand its semantics.

The publication review found further gaps after reproducing the 116-test result: a one-observation range trace could crash inside the pinned temporal library, and a response earlier than its trigger at the same timestamp could receive credit. Those are precisely the cases that make timing verification interesting. They were repaired with additional regression coverage before publication.

I see useful scope here for turning difficult-to-reproduce control behavior into inspectable regression tests. I also see a strong reason to distrust a green summary until I understand its treatment of time, ordering, and incomplete evidence.

## FixtureForge: fitting at the endpoint is not enough

[FixtureForge](https://github.com/jewbee2000/fixtureforge) is the most immediately visual of the four projects. It checks whether a simplified tool or connector can follow a specified straight insertion path through fixture geometry.

A part can fit in its final position while being impossible to insert along the intended route. Checking only the starting and ending positions misses obstacles in between. FixtureForge represents the tool's entire travel as a swept volume and checks that volume against imported STEP solids.

Its [comparison of CADCLAW, CadQuery, and build123d](https://github.com/jewbee2000/fixtureforge/blob/main/docs/BASELINE.md) included a small, useful counterexample: endpoint checks missed an obstacle producing **4 mm³ of overlap** along the travel path. Checking a prebuilt swept solid caught it. That comparison justified packaging the workflow around explicit paths, reproducible exports, and readable reports. It did not prove that the underlying collision operation was novel.

The demonstration is a parametric sensor clamp. The system exports geometry, reloads it for inspection, and reports where a conservative tool envelope intersects a component. A deliberately seeded obstructed path shows approximately **382.377 mm³** of overlap with the upper clamp.

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/fixture-access.jpg"><img src="/assets/files/agentic-engineering/fixture-access.jpg" alt="FixtureForge's rejected access report, with the sensor clamp, a 382.377 cubic millimetre tool-envelope intersection, and projections showing the obstruction." loading="lazy"></a>
  <figcaption>The report for a deliberately seeded obstructed path, captured during publication review. Purple shows the swept envelope; the verdict uses the solid geometry. This is a replay demonstration, with physical validation explicitly excluded.</figcaption>
</figure>

The original **61-test suite** passed again during review. Four cases inspect retained baseline, consumer, or performance records rather than rerunning those larger campaigns, so the count should not be read as 61 independent geometry experiments. Publication cleanup made the benchmark accept a fresh output directory, allowing another run without overwriting its original artifacts.

An earlier mistake was more mechanical: the agent initially described rotating the upper clamp half 180 degrees for printing. Inspection showed that the existing split face could be placed on the bed by translation. It corrected the instruction and the orientation check. Even within this narrow geometry problem, a plausible assembly explanation needed to be checked against the actual solid.

The limits are meaningful. The tool checks declared straight paths and conservative envelopes. It does not plan an articulated motion, establish clamping force, or prove that a printed part is strong enough. A conservative obstruction can reject a simplified envelope even when a more detailed tool or a different assembly sequence could work.

This is a good example of a useful engineering scope being smaller than the initial ambition. The geometry libraries do the hard geometric operations. The project contributes a repeatable question, explicit assumptions, and a way to inspect the answer.

## RFQFuzz: test the reviewer before trusting the review

My original drawing-review proposal encountered the clearest overlap with existing software. [CoLab advertises drawing completeness, dimensional consistency, and manufacturability checks](https://www.colabsoftware.com/product/autoreview), while [Palmetto provides an open-source CAD/DFM workbench](https://github.com/connorkapoor/Palmetto). The research established overlap in advertised and documented capabilities; it did not benchmark either product.

Codex proposed [RFQFuzz](https://github.com/jewbee2000/rfq-fuzz): generate controlled drawing packages, give them to a reviewer, and compare what that reviewer finds across versions.

The first feasibility gate used three versions of a plate. The STEP model contained four 6.00 mm bores. One drawing called for 6.80 ±0.05 mm at the same manufacturing stage, creating a contradiction. A corrected drawing specified 6.00 mm. A third package made a different diameter legitimate by explicitly describing an intermediate model and a later reaming stage.

That third case is essential. A reviewer that complains about every difference can look impressive on a set containing only defects. Valid alternatives test whether it understands the supplied context.

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/rfq-plate.png"><img src="/assets/files/agentic-engineering/rfq-plate.png" alt="RFQFuzz's actual plate drawing with four 6.8 plus or minus 0.05 millimetre bores and notes declaring model and drawing at the same finished stage." loading="lazy" width="2339" height="1654"></a>
  <figcaption>The original defective M0 drawing. Independent reading of its companion STEP found 6.00 mm bores. The contradiction depends on both artifacts and their declared manufacturing stage.</figcaption>
</figure>

The architecture has four jobs: generate the package, independently inspect its exported artifacts, collect the reviewer's observations, and score those observations against verified expectations. “Independently” needs qualification: the geometric paths still share the OCCT kernel. Separate code and a fresh reviewer reduce some opportunities for circular agreement, but do not eliminate common assumptions.

The final development corpus contained **145 validated packets** across plates, counterbored blocks, and pocketed blocks. The release passed **270 integrated tests** and its evaluator challenge detected **six deliberately introduced implementation faults**. All 145 core packets were development cases, with **no core holdout**. Those numbers describe the toolkit's acceptance evidence, not a general score for AI drawing review. [Corpus and evaluator challenge](https://github.com/jewbee2000/rfq-fuzz/blob/main/evidence/M4/challenge-report.md)

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/rfq-regression.png"><img src="/assets/files/agentic-engineering/rfq-regression.png" alt="RFQFuzz report showing conflicting 7075-T6 and 6061-T6 material declarations, with a detected contradiction becoming a deliberately injected silent miss." loading="lazy" width="1360" height="900"></a>
  <figcaption>Actual report output: a material contradiction becomes a silent miss after a deliberate regression is injected. This demonstrates diagnosis, not a naturally observed failure of a commercial reviewer.</figcaption>
</figure>

The genuine external-agent review is a separate, much smaller result. In the expanded two-packet review, **14 of 15 obligations received grounded matching decisions; one units assertion remained unadjudicated** under the conservative matching rules. That is useful evidence of the interface working, with an unresolved mismatch. It is far too small and too closely related to development to establish industrial accuracy. [Scoped external-review results](https://github.com/jewbee2000/rfq-fuzz/blob/main/evidence/M5/external-v1/summary.json)

RFQFuzz is the most ambitious project in this group and the one with the greatest risk of mistaking a controlled world for a general solution. It supports a finite geometry and annotation vocabulary, requires visual attestations tied to exact drawing bytes, and has no human manufacturing review or second CAD kernel. Its potential value is regression diagnosis for people developing reviewers. Practitioner demand still needs to be tested.

## What working with the agents actually involved

The chats show a shift in the kind of input I supplied. Most of my interventions concerned usefulness, scope, setup, sequencing, and the standard of evidence. The agents handled dependency selection, file creation, implementation details, test execution, and many repairs without asking me to decide each step.

The difficult part for me was keeping a useful mental model of what all four agents were doing. I had deliberately delegated the requirements, then found myself trying to catch up with the consequences. I could ask for another explanation, but the agent could produce explanations and acceptance documents just as quickly as code. More documentation was not automatically more understanding.

This is why I want the human collaboration to happen earlier. A team can discuss whether a timeout means failure or uncertainty, whether a drawing is authoritative at an intermediate manufacturing stage, and what evidence would falsify the proposed behavior. Those discussions give implementation a target. Reviewing an enormous resulting diff is an expensive way to discover that the target was wrong.

The most useful documents here connect a specific claim to a command, a result, and an artifact. A requirement-to-test matrix is valuable when it lets me follow a behavior into a failing case. A milestone labeled complete carries much less information on its own.

The session histories also contain context-compaction events. Long conversations did not remain verbatim in the agents' active context forever. Task ledgers, pinned dependencies, commits, and handoff notes provided a way to resume from external state. I cannot attribute a particular bug to compaction from these records. I can say that persistent project state was part of how the work remained inspectable across long sessions.

Ethan Mollick's [empirical treatment of uneven AI capabilities](https://www.oneusefulthing.org/p/centaurs-and-cyborgs-on-the-jagged) is a useful lens: a tool can be impressive on one task and unreliable on a nearby one. Karpathy's [discussion of agentic engineering](https://karpathy.bearblog.dev/sequoia-ascent-2026/) also emphasizes preserving the professional quality bar while delegating larger pieces of work. In this experiment, that quality bar needed to be expressed in artifacts the next agent—and eventually another engineer—could inspect.

## The failures are part of the result

Several failures are more informative than the passing totals.

**The evaluator could be wrong.** RFQFuzz's initial witness matching could give credit to a reported count of 40 when the expected count was 4 because it matched a substring. Independent probes caught that bug. The correction requires complete canonical evidence matches, which also makes the scorer less forgiving of equivalent free-form wording. That is an explicit tradeoff between accepting false evidence and requiring adjudication. [Retained correction record](https://github.com/jewbee2000/rfq-fuzz/blob/main/evidence/M5/independent-fixes.md)

**A plausible rule could exceed its source.** During RFQFuzz development, the provenance for a default inspection stage was narrowed because the cited material did not establish the claimed CNC default. The executable policy is now labeled project-selected. This is the kind of unsupported inference I worry about under the heading of hallucination: a reasonable-sounding engineering statement borrowing more authority from a source than the source supplies. [Milestone assessment](https://github.com/jewbee2000/rfq-fuzz/blob/main/docs/MILESTONE_ASSESSMENTS.md)

**The environment was part of correctness.** DriverForge's hosted CI initially failed because an artifact parent directory existed locally but was absent in the clean runner. RFQFuzz's archived input bytes were changed by Git newline normalization, breaking hashes for previously inspected artifacts. Its software-emulated Linux consumer also exceeded the initial timeout; acceptance required explicitly documented larger resource bounds. These were separate failures with separate fixes, not reasons to quietly weaken the meaning of a pass.

**Passing tests left room for additional bugs.** Before publishing this article, I asked for another code and evidence review. It reproduced the original suites, then found the AbyssBench timing edge cases described above and a DriverForge comparison gap: reports could be called unchanged despite differences in completeness, oracle version, or expected evidence. The publication pass added regression coverage and repaired those cases. Those fixes belong to this later review, rather than being retroactively counted as successes of the initial build.

The later review also found that RFQFuzz's reference reviewer could ignore a dimension's explicit inch units when the overall drawing used millimetres. The independent validator understood the local override, so a correctly expressed dimension could produce disagreement between the two paths. Another probe found a timing-dependent hole in the local adapter's output-size check: a process that exited quickly enough could evade the running-process check. Both are good examples of agent-led implementation review doing useful work after a passing release suite.

The four original suite totals—94, 116, 61, and 270—are useful reproducibility checkpoints. They are not a ranking of the projects, and their sum is not a quality score. Some tests exercise implementation details, some inspect retained evidence, and many fixtures were authored within the same agent workflow as the software they test.

The publication snapshots make the later review visible. These are passing test counts before and after the audit:

| Project | Original | Audited | Evidence |
| --- | ---: | ---: | --- |
| DriverForge | 94 | 100 | [Audit](https://github.com/jewbee2000/driverforge/tree/main/evidence/article-audit) |
| AbyssBench | 116 | 124 | [Audit](https://github.com/jewbee2000/abyssbench/tree/main/evidence/publication-audit) |
| FixtureForge | 61 | 61 | [Audit](https://github.com/jewbee2000/fixtureforge/tree/main/evidence/publication-audit) |
| RFQFuzz | 270 | 278 | [Audit](https://github.com/jewbee2000/rfq-fuzz/tree/main/evidence/publication-code-audit) |

Gary Marcus's [critique of unsupervised coding-agent use](https://garymarcus.substack.com/p/dario-amodei-hype-ai-safety-and-the) is relevant to the gap between generated code and maintained systems. Yann LeCun's [case for world models and explicit planning](https://www.linkedin.com/posts/yann-lecun_my-positionvisionproposal-paper-is-finally-activity-6947257092785278976-9AE7) raises broader questions about grounding and generalization. This small experiment cannot settle those debates. It does give me concrete reasons to demand more than fluent explanations when software makes claims about equipment or geometry.

It also clarifies my role. I should not claim that I personally discovered every bug or designed every architectural boundary. Agents did much of that work, including the publication audit. My consequential decisions were to demand usefulness, permit the scope to change, and insist on evidence beyond generated metadata. I set those expectations while delegating most of their detailed expression—and learned how difficult it was to keep pace afterward.

I do not think traditional line-by-line human code review needs to remain the default gate for this kind of work. I want the team collaborating on the spec and the test plan. Implementation still needs adversarial inspection, integration checks, and reproducible failures; agents can perform much of that work, as they did here. The human responsibility is to make sure the checks represent the problem we actually intend to solve, including behavior we explicitly do not want.

I increasingly trust agents to execute a clearly defined plan. This experiment does not establish that the first implementation follows every requirement exactly: the later defects are direct counterexamples to that stronger claim. It does support a workflow in which agents implement, challenge, and repair against an explicit contract. The distinction matters most when the same agent has also helped write the contract.

## What I will do differently next time

I think the agent performed better at finding plausible integration opportunities than at establishing unmet demand. Each project has a recognizable engineering user and a runnable demonstration. None yet has the evidence of repeated use by an independent practitioner that would tell me it deserves continued maintenance.

DriverForge has the clearest near-term integration story. AbyssBench exposes subtle and worthwhile questions about controller timing. FixtureForge offers a concrete visual check with understandable limits. RFQFuzz tackles the deepest evaluation problem, while also requiring the most care about what its synthetic corpus can establish.

The implementations are substantial enough to inspect and extend. Their strongest common property is that they make failure visible. Their shared weakness is the distance between a controlled example and a tool another engineer would trust on unfamiliar inputs.

The code is also uneven. DriverForge's typed interfaces and static checks make its boundaries relatively easy to follow. RFQFuzz has a more demanding artifact-validation pipeline, but parts of its implementation compress several operations onto one line and repeat finite rules across modules. Separate evaluation logic can help expose mistakes; duplicated semantics can also drift, as the local-unit bug demonstrated. Passing behavior and maintainable implementation are related qualities, not interchangeable ones.

That suggests a different next experiment. I would choose one project, find a practitioner with a real problem, and ask them to use it without the implementation chat. I would measure the time to a useful result, the assumptions they had to supply, the mistakes they encountered, and the amount of intervention required. For RFQFuzz, I would want an authorized engineer-authored packet and independently adjudicated expectations. For FixtureForge, a real assembly and physical measurements would teach me more than another hundred generated variants.

I will keep the requirements-first kickoff, the small feasibility gate, preserved failures, and an agent review that actively tries to break the result. I will spend more of my own attention defining and challenging the MoSCoW requirements before the work expands. I will also add a measurement plan at the start so that cost, elapsed work, and my own interventions can be discussed quantitatively. A separate agent can supply another review, while a fresh conversation alone does not create a truly independent oracle.

The strategic consequence, for my own workflow, is that more small engineering tools become worth trying. Existing open-source libraries supply capable foundations; an agent can assemble a domain-specific workflow around them at a much lower apparent cost of experimentation. Each successful experiment still creates an obligation to understand and maintain what was built.

I started with a portfolio question: could I use an agent to build something substantial in an area I care about? I now have four repositories that make the answer inspectable. I also have a clearer idea of where I should spend my attention. Keeping up with every line the agents produce is a losing strategy. Being precise about what the system must do, what it must never do, and how we will know the difference is engineering work I want to get better at.

---

**Explore the projects:** [DriverForge](https://github.com/jewbee2000/driverforge) · [AbyssBench](https://github.com/jewbee2000/abyssbench) · [FixtureForge](https://github.com/jewbee2000/fixtureforge) · [RFQFuzz](https://github.com/jewbee2000/rfq-fuzz)

*Method and authorship note: I used Codex to help draft this retrospective from my session history, repository contents, and retained results. A further agent-assisted publication review reran checks and made the repairs identified above. Figures are actual project artifacts or visualizations of recorded evidence. No physical hardware testing, manufacturing approval, broad market novelty, or controlled productivity comparison is claimed. The [publication evidence manifest](/assets/files/agentic-engineering/evidence-manifest.json) records the source snapshots, checks, and figure provenance.*
