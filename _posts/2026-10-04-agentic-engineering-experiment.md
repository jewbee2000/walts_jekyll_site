---
layout: post
title: "When the Agents Outrun the Engineer"
date: 2026-10-04 00:00:00 -0700
permalink: /2026/10/04/agentic-engineering-experiment/
lead: "Four coding projects, one electrical cabinet, and a changing idea of what engineering is for."
description: "Walter Teitelbaum on an experiment with coding agents, requirements-first engineering, careers built around delegation, physical automation, and the case for deliberately limiting AI access."
article_wide: true
image: /assets/files/agentic-engineering/rfq-plate.png
---

The most frustrating part of my latest experiment with AI was my own inability to keep up.

Across October 3–4, I asked Codex to research, propose, plan, and implement several engineering projects. It investigated existing software, wrote requirements, built tools, ran tests, and produced reports. While I was still trying to understand one set of decisions, the agents were making the next set.

I had expected to learn something about the limits of the software. I also learned something uncomfortable about the limits of my attention.

The experience sits alongside a very different task in my day-to-day engineering work. I need to reconcile the wiring in a robot's electrical control cabinet with its schematic. Changes have accumulated. Someone has to inspect the connections, establish what is actually there, resolve the discrepancies, and number and label the wires. The agent that can generate a substantial Python project cannot finish that job for me.

These two experiences are shaping how I think about AI. Some kinds of execution are becoming remarkably easy to delegate. Other work remains stubbornly physical, poorly documented, or dependent on decisions that nobody has made yet. Meanwhile, giving agents access to more of the world makes them both more useful and more consequential when they fail.

My emerging view is that engineering value is moving toward three difficult responsibilities: defining what should happen, establishing what is true, and deciding how much authority a system should have. The code matters. So do the wire, the requirement, the permission, and the connection we choose not to provide.

## I asked the agent to choose the problem

My interests sit where software meets physical equipment: controls, instrumentation, fixtures, manufacturing, and the details that become unavoidable when a design has to work. My portfolio already includes [robotic gardening](/2021/07/25/Automated-Pruning-for-Polyculture/) and [printed bicycle components](/2025/04/01/3D-Printed-Bicycle-Components/). I wanted to see whether an agent could infer useful software projects from those interests, then carry them through a disciplined engineering process.

That is a harder assignment than implementing a feature. It asks the agent to decide what deserves to exist.

I initially requested five proposals and then asked Codex to select three it could implement with little guidance. A drawing-review idea developed into a fourth project. Before implementation, I pushed back on the temptation to produce impressive portfolio theater:

> “I want to implement projects that are actually useful.”

I asked for research into existing tools, explicit requirements, acceptance criteria, and a willingness to change direction when the proposed contribution was weak. The requirements used MoSCoW: Must, Should, Could, and Won't. The implementation instructions called for isolated environments, reproducible consumer walkthroughs, coherent commits, and preserved failures. One instruction captures the intended standard:

> “Establish independent acceptance checks, preserve failed examples, and commit coherent milestones locally.”

For this experiment, I let the agents author and rationalize most of those requirements themselves. Codex also helped formulate the detailed kickoff prompts. My input was small relative to the work produced, but the process was not an empty prompt followed by a finished product. I supplied the domain and challenged the scope; agents supplied much of the detail that made the assignment executable.

The outcome was four runnable Python projects. Their common theme was verification at an engineering interface: instrument bytes, controller events, fixture geometry, and drawing packages. That was a good inference from my interests. It was a more modest achievement than discovering four new markets.

## Four tools, four ways to be wrong

### DriverForge: a timeout can conceal a successful action

[DriverForge](https://github.com/jewbee2000/driverforge) tests instrument drivers without requiring the physical instrument. A scripted transport supplies responses and faults; separate conformance logic checks whether the driver followed its protocol contract. Reports connect the requirement, actual behavior, and wire transcript.

The architectural detail I like most concerns retries. If a command changes an instrument's state and its acknowledgement disappears, the action may already have happened. Sending the command again can repeat it. The synthetic protocols distinguish safe read retries from an uncertain write outcome.

A simpler failure is visible below. The bytes `fb 2e`, decoded as a signed 16-bit value and scaled by 0.01, mean **−12.34 °C**. Decode them as unsigned and the result becomes **643.02 °C**. Both calculations run successfully. Only one satisfies the contract.

<figure class="experiment-figure compact">
  <a href="/assets/files/agentic-engineering/driver-signed-failure.png"><img src="/assets/files/agentic-engineering/driver-signed-failure.png" alt="DriverForge report showing expected minus 12.34 degrees Celsius and observed 643.02, with the byte transcript and signed scaling rule." loading="lazy" width="755" height="1060"></a>
  <figcaption>A deliberately broken unsigned-decoding implementation, caught by the conformance checks. This is a synthetic replay demonstration, not a measurement from hardware or an observed model failure.</figcaption>
</figure>

The original release passed 94 tests, exercised 39 conformance cases, and rejected six deliberately faulty implementations. It also integrated an existing PyMeasure Agilent driver. Since [PyMeasure already provides protocol-testing tools](https://pymeasure.readthedocs.io/en/stable/dev/adding_instruments/tests.html), DriverForge's contribution is reusable fault campaigns and diagnostic evidence. Its Agilent failure cases express synthetic consumer requirements, not proven defects in an actual instrument. Hardware validation remains outside the result.

### AbyssBench: time is part of the specification

[AbyssBench](https://github.com/jewbee2000/abyssbench) replays controller events and tests whether a response happened correctly and on time. “Shut down when the sensor becomes stale” sounds like a requirement until somebody has to implement it. Which timestamp defines staleness? What if the trigger and response share a timestamp? What if the recording ends before the response deadline?

The system uses [RTAMT](https://github.com/nickovic/rtamt) for numeric range predicates and a Python event ledger for response deadlines, ordering, and history. An incomplete observation window can produce an inconclusive verdict. That distinction prevents missing evidence from quietly becoming a pass.

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/abyss-timing.png"><img src="/assets/files/agentic-engineering/abyss-timing.png" alt="A synthetic valve sticks closed at 500 milliseconds. At 1,010 milliseconds the controller commands the valve open and pump off, but the simulated valve remains closed." loading="lazy" width="1920" height="1120"></a>
  <figcaption>A new plot of the retained synthetic replay: the valve sticks at 500 ms; detection and safe commands occur at 1,010 ms. The simulated valve remains closed. Passing a command-timing requirement does not establish actuator motion or physical safety.</figcaption>
</figure>

The original suite passed 116 tests and recorded 21 Must requirements as verified. A property-based check was configured for 1,000 generated action/fault sequences. Yet the most useful thing in the figure is a distinction no test count can communicate: the controller issued safe commands while the simulated valve remained stuck. A valid command is evidence about the controller. It is not proof that the actuator moved or that a physical system is safe.

### FixtureForge: a part can fit and still be impossible to insert

[FixtureForge](https://github.com/jewbee2000/fixtureforge) checks whether a simplified tool or connector can travel along a declared straight path through fixture geometry. It constructs the volume occupied over the whole travel and tests that swept volume against imported STEP solids.

Its [comparison of CADCLAW, CadQuery, and build123d](https://github.com/jewbee2000/fixtureforge/blob/main/docs/BASELINE.md) included an obstacle that endpoint checks missed, with 4 mm³ of overlap along the path. The geometry libraries already supplied the essential operations. The useful contribution was packaging them into a reproducible access check with an inspectable report.

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/fixture-access.jpg"><img src="/assets/files/agentic-engineering/fixture-access.jpg" alt="FixtureForge's rejected access report, with the sensor clamp, a 382.377 cubic millimetre tool-envelope intersection, and projections showing the obstruction." loading="lazy"></a>
  <figcaption>The report for a deliberately seeded obstructed path, captured during publication review. Purple shows the swept envelope; the verdict uses the solid geometry. This is a replay demonstration, with physical validation explicitly excluded.</figcaption>
</figure>

The original 61-test suite passed again during review. Four cases check retained campaign records rather than rerunning the larger experiments. The tool handles conservative envelopes and specified straight paths; it does not establish clamping force, material strength, or the feasibility of an articulated assembly sequence. An earlier instruction to rotate the upper clamp half for printing also needed correction: inspecting the solid showed that translation could place its existing split face on the bed.

That is a useful reminder of where fluent explanation meets geometry. The explanation can sound finished before anyone has checked the part.

### RFQFuzz: the reviewer needs an evaluator

My drawing-review proposal encountered obvious overlap with [CoLab's advertised review capabilities](https://www.colabsoftware.com/product/autoreview) and [Palmetto's open-source CAD/DFM workbench](https://github.com/connorkapoor/Palmetto). Rather than preserve the original pitch, the project became [RFQFuzz](https://github.com/jewbee2000/rfq-fuzz): a toolkit for generating controlled drawing packages and diagnosing changes in how a reviewer handles them. The competitive research established overlap, not a benchmark of either product.

The first feasibility gate contained a plate with four 6.00 mm bores in its STEP model. One drawing specified 6.80 ±0.05 mm at the same manufacturing stage. A corrected drawing specified 6.00 mm. A third package made a different diameter legitimate by declaring an intermediate model and a later reaming stage.

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/rfq-plate.png"><img src="/assets/files/agentic-engineering/rfq-plate.png" alt="RFQFuzz's actual plate drawing with four 6.8 plus or minus 0.05 millimetre bores and notes declaring model and drawing at the same finished stage." loading="lazy" width="2339" height="1654"></a>
  <figcaption>The original defective M0 drawing. Independent reading of its companion STEP found 6.00 mm bores. The contradiction depends on both artifacts and their declared manufacturing stage.</figcaption>
</figure>

The third case is the interesting one. A reviewer that objects to every difference can look capable on a corpus containing only defects. Valid alternatives test whether it understands the supplied context.

RFQFuzz generates a package, reopens its exported artifacts, collects a reviewer's observations, and scores them against verified expectations. The geometry inspection has separate code, although both paths share the OCCT kernel. That reduces some opportunities for circular agreement without removing common assumptions.

The final corpus contained 145 validated development packets across three simple geometry families, with no core holdout. The original suite passed 270 tests, and the evaluator challenge caught six deliberately introduced implementation faults. Those are results about a finite toolkit, not an accuracy score for reviewing arbitrary manufacturing drawings. [Corpus and challenge evidence](https://github.com/jewbee2000/rfq-fuzz/blob/main/evidence/M4/challenge-report.md)

<figure class="experiment-figure">
  <a href="/assets/files/agentic-engineering/rfq-regression.png"><img src="/assets/files/agentic-engineering/rfq-regression.png" alt="RFQFuzz report showing conflicting 7075-T6 and 6061-T6 material declarations, with a detected contradiction becoming a deliberately injected silent miss." loading="lazy" width="1360" height="900"></a>
  <figcaption>Actual report output: a material contradiction becomes a silent miss after a deliberate regression is injected. This demonstrates diagnosis, not a naturally observed failure of a commercial reviewer.</figcaption>
</figure>

A separate external-agent review was much smaller: across two packets, 14 of 15 obligations received grounded matching decisions; one units assertion remained unadjudicated. That demonstrated a working interface and an unresolved mismatch. It did not establish industrial reliability. [External-review results](https://github.com/jewbee2000/rfq-fuzz/blob/main/evidence/M5/external-v1/summary.json)

Of the four projects, RFQFuzz makes the evaluation problem most explicit. If the system deciding what counts as correct is wrong, a better score can mean very little.

## Passing tests did not end the experiment

The agents produced substantial, inspectable software. They also made mistakes that explain why I care so much about the specification and test plan.

RFQFuzz's initial witness matching could give credit to a reported count of 40 when the expected count was 4 because it matched a substring. Independent probes caught it. Elsewhere, a default inspection-stage rule claimed more support from a cited source than the source actually supplied; the policy was narrowed and labeled project-selected. One error was executable. The other was a plausible engineering assertion borrowing unearned authority. Both could undermine the meaning of a passing result. [Scoring repair](https://github.com/jewbee2000/rfq-fuzz/blob/main/evidence/M5/independent-fixes.md), [milestone assessment](https://github.com/jewbee2000/rfq-fuzz/blob/main/docs/MILESTONE_ASSESSMENTS.md)

Environment assumptions failed too. DriverForge's hosted CI relied on an artifact directory that happened to exist locally. RFQFuzz's archived input bytes were changed by Git newline normalization, invalidating hashes of previously inspected artifacts. Its software-emulated Linux consumer needed explicitly documented longer timeouts. A local demonstration had not settled reproducibility.

Before publication, I requested another agent-assisted code and evidence review. It reproduced the original suites, then found additional defects. AbyssBench could crash on a one-observation range trace and credit a response that preceded its trigger at the same timestamp. DriverForge could overlook changed report evidence. RFQFuzz's reference reviewer could ignore a dimension's local inch units under a millimetre drawing header; a fast-exiting local process could also evade a running-process output-size check.

Those issues were repaired and covered by regressions. Here are the passing suite counts, with the original experiment separated from the later audit:

| Project | Original | Audited | Evidence |
| --- | ---: | ---: | --- |
| DriverForge | 94 | 100 | [Audit](https://github.com/jewbee2000/driverforge/tree/main/evidence/article-audit) |
| AbyssBench | 116 | 124 | [Audit](https://github.com/jewbee2000/abyssbench/tree/main/evidence/publication-audit) |
| FixtureForge | 61 | 61 | [Audit](https://github.com/jewbee2000/fixtureforge/tree/main/evidence/publication-audit) |
| RFQFuzz | 270 | 278 | [Audit](https://github.com/jewbee2000/rfq-fuzz/tree/main/evidence/publication-code-audit) |

These are reproducibility checkpoints, not a quality ranking. The implementations differ in maintainability too. DriverForge has relatively clear typed interfaces and static checks. RFQFuzz has more demanding artifact validation but also compressed code and repeated finite rules whose meanings can drift. More code and more tests do not automatically make a better product.

Gary Marcus's [critique of coding-agent failures](https://garymarcus.substack.com/p/dario-amodei-hype-ai-safety-and-the) is a useful counterweight here: generating code and maintaining a dependable system are different achievements. The agents were useful enough that I want to delegate more work to them. The retained failures tell me where that delegation needs a stronger contract.

The long chats contained context-compaction events. Requirements files, task ledgers, commits, and handoff notes gave subsequent work something durable to resume from. I cannot attribute a particular defect to lost context, but I would not want a project's state to exist only in a conversation's memory.

I also cannot claim a productivity multiplier. I did not collect a controlled human-only baseline, reliable total token cost, or a comparable measure of my own implementation time. What I can show is four runnable tools, recorded failures, and the amount of useful work the agents completed with limited implementation direction.

That is enough to change my workflow. It is not enough to suspend my judgment.

## The human review should move toward the spec

The part that frustrated me was trying to keep a coherent mental model of everything the agents were doing. Asking for more explanation did not necessarily help: an agent can produce rationales and acceptance documents as quickly as code.

For an experiment, letting it write its own assignment was revealing. For a tool intended to solve an actual problem of mine, I would invest much more intellectual effort before implementation. I would work through the MoSCoW requirements with the agent, challenge the assumptions, and decide what evidence would convince me that each important requirement had been met.

I consider system requirements the essence of successful engineering, whether the result is software, a machine, or a manufacturing process. A test can verify the behavior we specified. It cannot decide that we specified the right problem.

The Won't list deserves particular attention. If I omit a feature from my description, the agent may infer that adding it is helpful. A hosted service, automatic hardware write, or extra workflow might be a reasonable interpretation of an underspecified request and still be something I do not want. An explicit exclusion removes that ambiguity.

My conclusion is stronger than “AI can help with code review.” I do not think traditional line-by-line human code review needs to remain the default collaboration model for agent-written software. I want the team spending its attention on the spec and the test plan: what the system must do, what it must never do, which assumptions are justified, and which failures the checks must expose.

Implementation still needs adversarial inspection and integration testing. The audit demonstrated that agents can do useful work there too. This is a proposal to change where humans concentrate their effort, not evidence that every first implementation follows its plan exactly. The defects above rule out that stronger claim.

There is a limit to delegating evaluation as well. Separate agents can share the same mistaken assumption. A fresh conversation does not create an independent physical measurement. Sometimes the right acceptance evidence comes from another implementation; sometimes it comes from another person; sometimes somebody has to go and inspect the wire.

Ethan Mollick's [work on uneven AI capabilities](https://www.oneusefulthing.org/p/centaurs-and-cyborgs-on-the-jagged) helps explain why local success should not become blanket trust. Karpathy's [discussion of agentic engineering](https://karpathy.bearblog.dev/sequoia-ascent-2026/) emphasizes preserving a professional quality bar while delegating execution. I find both perspectives useful because the hard question is how to express that bar in a form a system can be tested against.

## A more managerial kind of individual contributor

This is also why I think people should start practicing a more managerial way of working, well before their job title changes.

I mean learning to define outcomes, decompose work, provide context, establish acceptance criteria, and integrate the result. Those are skills an individual engineer can use. Managing people involves relationships and development that do not map neatly onto agents; the transferable part here is organizing work and owning its consequences.

I have found myself imagining a person coordinating a hundred agents. The number is an illustration, not a target. If four projects can outrun my attention, multiplying the workers without changing how I specify and evaluate their work is unlikely to solve the problem.

[A study of agent-system scaling, revised in April 2026 to cover 260 configurations](https://arxiv.org/abs/2512.08296v3), found gains on decomposable tasks and losses on sequential planning in the benchmarks it studied. More agents can add coordination costs and propagate errors. The useful measure is the amount of validated work completed, including the effort required to resolve exceptions.

My forecast is that effective delegation will become valuable across a wide range of professions. I would not claim that every industry will change at the same rate, or that coordinating agents guarantees a career. Access to customers, physical evidence, institutional trust, and the ability to recognize a bad assumption can matter more than producing another answer.

Nor is “be the manager” a permanent refuge from automation. My agents already wrote plans, assigned work, and synthesized findings. Some of the managerial work is itself being automated. The responsibility I want to develop is deciding whether the work is worth doing and whether the evidence is good enough to use its result.

That creates an uncomfortable learning problem. The tasks we delegate are often the tasks through which we acquire judgment. If I never debug the mistaken unit conversion, how do I learn to ask about units?

In [a randomized study of 52 mostly junior engineers learning an unfamiliar Python library](https://www.anthropic.com/research/AI-assistance-coding-skills), the AI-assisted group scored 50% on the subsequent comprehension quiz, compared with 67% for the unaided group. The completion-time difference was not statistically significant. One short learning task does not establish the long-term effects on engineering careers, but it makes the distinction between producing a result and acquiring expertise difficult to dismiss.

How should we preserve that learning? Studying failures, doing some work unaided, and reconstructing an explanation are possibilities worth testing. Delegation should expand what I can take responsibility for, rather than leave me approving outputs I cannot interrogate.

## The cabinet is where the abstraction stops

The more digital work I delegate, the more visible the remaining work becomes. My electrical cabinet is a concrete example.

I need a reliable account of which wire connects which endpoints, whether those connections agree with the intended design, and which changes belong in the schematic. I also need the physical labels and wire numbers to agree with the documentation. An agent can help organize that task. The agent on my computer cannot inspect hidden connections or attach the labels for me.

That makes me interested in a robot built specifically for this work: looking through existing cabinets, identifying wires and components, recovering connections, and applying markers. It is the kind of startup idea I notice when I stop asking only what AI can do and start looking at the expensive task it leaves behind.

There is already serious automation nearby. [Rittal's Wire Terminal](https://www.rittal.com/com-en/products/PG20231215RAS101/PG20240408RAS202/PG20240408RAS205/PRO136436?variantId=4051205) prepares and labels wires. [Eplan's Smart Wiring check mode](https://www.eplan.help/en-us/Infoportal/Content/ESW/Content/htm/smartwiring_k_connection_list_checking_mode.htm) supports a person checking installed connections. [Wirebot advertises robotic panel wiring](https://www.wirebot.tech/products-sharp), while [WSCAD's Cabinet AR](https://www.wscad.com/en/apps/) provides access to project wiring information and schematic redlining. Those capabilities do not, by themselves, establish autonomous reconciliation of an arbitrary cabinet after undocumented modifications. Building from known design data and reconstructing an uncertain existing state are different problems.

The difficulty is partly perception: wires disappear into ducts, similar wires cross, and labels can be wrong. It is partly manipulation: applying a marker to an installed wire is different from marking one before assembly. It is also a question of authority. If the cabinet and schematic disagree, which one is wrong?

LeCun's [proposal for world models and planning](https://www.linkedin.com/posts/yann-lecun_my-positionvisionproposal-paper-is-finally-activity-6947257092785278976-9AE7) offers a research direction for machines reasoning about an uncertain world. My immediate question is what evidence a tool needs before it claims to understand this particular cabinet.

Automatically redrawing the schematic to match the cabinet could turn an assembly error into apparently approved documentation. A useful system would preserve the difference between an observation, an inference, an electrically tested connection, and an approved change. An unresolved endpoint should remain unresolved rather than receive a confident guess.

This is the same problem RFQFuzz encountered with manufacturing stages. A difference between two artifacts becomes meaningful only after we understand what each artifact is supposed to represent.

One way to test the opportunity would be to measure whether assisted reconciliation saves an engineer time: capture evidence, propose endpoint matches, expose uncertainty, and produce candidate drawing updates and labeling lists. The results could show where software helps and where better sensing or robotic manipulation is essential. That is a product hypothesis, not a fifth completed project or a claim that nobody is working on it.

Difficulty alone does not make a business. Someone has to need the result often enough, trust it enough, and pay enough to justify the equipment and integration. Ben Thompson's [argument about software survival](https://stratechery.com/2026/microsoft-and-software-survival/) is relevant here: customers buy maintenance, integration, and a working product, not merely its source code. Easier implementation makes experiments cheaper to attempt. It does not make the remaining obligations disappear.

My four projects suggest that agents are already good at assembling plausible workflows from existing libraries. Establishing unmet demand was much less convincing. The next useful experiment would put one tool in another engineer's hands and measure whether it solves a problem without the implementation chat beside it.

## Capability becomes consequential through access

The cabinet also connects my enthusiasm for automation to my concern about AI risk. We want agents to do more than generate suggestions. Every additional tool or connection gives them another way to affect the world.

My instinct is that a major digital incident—a serious data breach, corrupted records, or a destructive loss of access—is a more immediate concern than a scenario centered on an AI's own physical body. A disruption to banking records or payment systems, for example, could interfere with people's ability to pay rent or operate a business. That is the kind of near-term consequence I worry about.

I need to qualify the physical distinction. Lack of a robot body does not imply lack of physical influence. Industrial control systems already connect digital commands to equipment, and people act on information supplied by software. [CISA and its partners have documented physical effects from attacks on exposed operational technology](https://www.cisa.gov/sites/default/files/2024-05/defending-ot-operations-against-ongoing-pro-russia-hacktivist-activity-508c.pdf). That advisory concerns cyberattacks, not proof of AI-caused injury. It shows why the relevant question is what a system can reach and control.

The Hugging Face incident made this concern more concrete for me. Its [technical reconstruction](https://huggingface.co/blog/agent-intrusion-technical-timeline) describes an intrusion originating in an agent evaluation environment. [OpenAI's account](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) describes unauthorized access through package-management infrastructure and evaluation conditions with reduced safeguards. An [independent METR and Redwood investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) also examined the event. These accounts differ in their interpretation of the agents' immediate objectives, so I would not present their motives as settled.

The architectural lesson is clearer: there was a reachable path through infrastructure expected to contain the evaluation. This was not a demonstration of an agent reaching across an absent physical connection. It was a demonstration that the boundaries people believed they had established did not match the available route.

Not every agent incident has that mechanism. An authorized agent might make a mistake. An attacker might use one as a tool. An agent might treat instructions embedded in untrusted material as something to obey. [Simon Willison's account of prompt-injection risk](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) focuses on the dangerous combination of private-data access, untrusted input, and a way to send information outward. Those failures need different investigations even when their consequences overlap.

Confidentiality, integrity, and availability also matter differently. Leaked designs cannot be made secret again by restoring a backup. Corrupted records can leave a service running while its answers are wrong. An outage can prevent people from using accurate records that still exist. “The data is backed up” addresses only part of the problem.

I do not need to settle every debate about machine intelligence to ask a practical engineering question: if this system behaves unexpectedly, what can it damage before another boundary stops it?

## Some connections may stop being worth having

For much of my life, connecting more things to the internet has felt like the default direction of progress. I suspect increasingly capable agents will make organizations reconsider some of those connections.

My forecast is selective disconnection: valuable intellectual property held in genuinely isolated environments, sensitive workloads with fewer network paths, and narrower authority for systems that remain connected. A major agent-driven data incident could accelerate that change. It would make the tradeoff between convenience and exposure difficult to ignore.

There are already products for disconnected deployments. [Microsoft announced expanded disconnected sovereign infrastructure in February 2026](https://blogs.microsoft.com/blog/2026/02/24/microsoft-sovereign-cloud-adds-governance-productivity-and-support-for-large-ai-models-securely-running-even-when-completely-disconnected/), and [Google described air-gapped AI infrastructure in April](https://cloud.google.com/blog/topics/hybrid-cloud/google-distributed-cloud-at-next26). Both announcements preceded the July Hugging Face incident. They establish that the deployment model exists, not that my forecast has occurred at scale or that this incident caused it.

A physical boundary is attractive because it does not require the agent to understand the reason for the boundary. If a remote process has no communication path to an isolated store, better reasoning does not create that missing path. But the operating process has to maintain the separation. A local agent may already have access. Imported software or removable media may carry a threat. A person can move sensitive information across the boundary. “On premises” is not synonymous with isolated or trustworthy; [NIST's zero-trust guidance](https://www.nist.gov/publications/zero-trust-architecture) explicitly rejects implicit trust based on network location.

An offline backup serves another purpose: recovery. It does not remove access to the working copy or undo disclosure. [CISA's ransomware guidance](https://www.cisa.gov/stopransomware/ransomware-guide) treats recovery copies and network separation as distinct controls. A serious design has to say which failure each boundary is intended to address.

There are costs to disconnection: updates, maintenance, collaboration, transfer procedures, and the useful work that a connected agent could otherwise do. I do not expect every organization to disconnect everything. I expect more deliberate decisions about whether a particular connection earns the authority it creates.

This brings me back to the spec, with an essential distinction. Writing “must not transmit this design” defines the intended behavior. Restricting the process's communication path enforces a limit independently of whether it follows that instruction. A comprehensive test plan is valuable, but I do not believe people can anticipate every interaction between an adaptive agent and a complicated environment. The architecture should limit the consequences of what the test plan misses.

My own experiment supplies a small, concrete example. RFQFuzz's process runner passed its release suite while retaining an output-limit race. Fixing the race was worthwhile. Calling that same-user process runner a security sandbox would still be wrong. Confidence should track the property actually enforced.

The decision to delegate implementation and the decision to constrain authority belong together. The more useful work I want an agent to perform without my continuous attention, the more deliberately I need to design the conditions under which it acts.

## The work I want to get better at

I remain excited by what happened in this experiment. I can explore a hardware-adjacent software idea and get far enough to inspect the architecture, run a demonstration, and discover real failure modes. Open-source libraries provide the foundations; agents make more of the integration work feasible. That expands the set of ideas worth trying.

I also have a clearer view of my own bottleneck. I cannot solve it by reading faster while requesting more output. I need to be more deliberate about what work I initiate, what I delegate, and what evidence returns to me.

On the next project, I want to spend more time collaboratively defining requirements before implementation, including the Won't list. I want acceptance checks that could prove the agent wrong, an implementation review with a different line of attack, and explicit limits on access. I want to measure the total effort—including my review and the repairs—rather than celebrate a fast first draft.

For my career, that means practicing delegation while continuing to build the domain knowledge that makes delegation useful. For a potential business, it means studying the task left behind, such as reconciling that cabinet, and finding out whether someone values the result. For AI risk, it means treating access and physical infrastructure as design decisions, rather than assuming a well-written instruction will contain every failure.

There is no guarantee that these responsibilities will remain exclusively human. There is plenty of evidence, including my own difficulty keeping pace, that I need to get better at them now.

I began by asking whether an agent could build substantial software from a small amount of direction. I now have four repositories that make the answer inspectable. The question I care about next is what I should authorize it to build, how I will know it worked, and which parts of the world it should be able to reach while trying.

---

**Explore the projects:** [DriverForge](https://github.com/jewbee2000/driverforge) · [AbyssBench](https://github.com/jewbee2000/abyssbench) · [FixtureForge](https://github.com/jewbee2000/fixtureforge) · [RFQFuzz](https://github.com/jewbee2000/rfq-fuzz)

*Method and authorship note: I used Codex to help research and draft this article from my own notes, personal reflections, session history, and project evidence. Agents performed the implementation and publication audits described here. The figures are actual project artifacts or plots of recorded evidence. The cabinet system is an idea, not a completed prototype; the career and infrastructure arguments are my forecasts. No physical validation, manufacturing approval, broad market novelty, or controlled productivity comparison is claimed. The [publication evidence manifest](/assets/files/agentic-engineering/evidence-manifest.json) records project snapshots, checks, and figure provenance.*
