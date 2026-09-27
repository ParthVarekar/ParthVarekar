<!-- Parth Varekar / GitHub profile. Graphics: scripts/build_static.py (static) and .github/workflows/profile.yml (live). -->

<a href="https://parthvarekar.in">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
    <img alt="Parth Varekar. I build local-first AI software: retrieval engines, voice tools and developer platforms that run on your own hardware." src="assets/header-light.svg" width="100%">
  </picture>
</a>

### At a glance

|                 |                                                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Focus**       | Local-first AI: retrieval (RAG), speech and LLM tooling that runs on your own hardware                               |
| **Languages**   | Python, TypeScript, JavaScript, Java                                                                                 |
| **Recent work** | A permission-aware RAG engine for Slack, an offline dictation app, a design-to-code canvas, and a safety layer for AI browser agents |
| **Hackathons**  | Smart India Hackathon (SIH), CodeByte 2.0 ([Credence](https://github.com/ParthVarekar/credence_final))                |
| **Contact**     | [parthvarekar.in](https://parthvarekar.in), or [open an issue](https://github.com/ParthVarekar/ParthVarekar/issues/new?title=Hello) on this repo |

### Selected work

<p>
  <a href="https://github.com/ParthVarekar/enterprise_knowledge_assistance"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-eka-dark.svg"><img alt="Enterprise Knowledge Assistant: Slack-native RAG engine with zero-trust ACL and NLI grounding" src="assets/card-eka-light.svg" width="49%"></picture></a>
  <a href="https://github.com/ParthVarekar/Susurrus"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-whisperflow-dark.svg"><img alt="WhisperFlow: offline dictation with on-device speech recognition and LLM cleanup" src="assets/card-whisperflow-light.svg" width="49%"></picture></a>
  <a href="https://github.com/ParthVarekar/frigshwar"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-codeframe-dark.svg"><img alt="Codeframe: design canvas that exports React and Tailwind" src="assets/card-codeframe-light.svg" width="49%"></picture></a>
  <a href="https://github.com/ParthVarekar/agent_safety_net"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-agent-safety-net-dark.svg"><img alt="Agent Safety Net: runtime safety layer for AI browser agents" src="assets/card-agent-safety-net-light.svg" width="49%"></picture></a>
</p>

<details>
<summary><b>Architecture notes</b> (how each of these works)</summary>

<br/>

**Enterprise Knowledge Assistant.** Permissions are checked on every chunk before retrieval, and every generated claim is checked against the sources after generation.

```mermaid
flowchart LR
    Q["Slack question"] --> ACL{"Zero-trust ACL<br/>per-chunk entitlements"}
    ACL -->|permitted docs only| R["Hybrid retrieval<br/>BM25 + dense vectors<br/>fused with RRF"]
    R --> LLM["Gemma 4 on llama.cpp<br/>full CUDA offload"]
    LLM --> NLI{"NLI grounding<br/>claim by claim"}
    NLI -->|entailed| A["Answer with citations"]
    NLI -->|unsupported| X["Abstain"]
```

**WhisperFlow.** Speech recognition and text editing are handled by two separate local models, so the output is edited text rather than a raw transcript.

```mermaid
flowchart LR
    M["Hotkey + microphone"] --> ASR["Qwen3-ASR<br/>speech to raw text"]
    ASR --> P["Gemma on llama.cpp<br/>removes fillers, applies<br/>spoken formatting"]
    P --> O["Pasted into the<br/>focused app"]
```

**Codeframe.** One scene graph drives the editor, the live preview and the code exporter, so the preview and the exported code stay in sync.

```mermaid
flowchart LR
    E["Canvas editor<br/>frames, layout, motion"] --> SG["Scene graph"]
    SG --> CSS["Scene to CSS mapping"]
    CSS --> PV["Live HTML prototype"]
    CSS --> CG["Code export: Vite + React<br/>+ Tailwind + shadcn/ui"]
```

**Agent Safety Net.** Blocking decisions are local and deterministic. The LLM is only used afterwards, to explain a decision to the user.

```mermaid
flowchart LR
    AG["AI agent on a page"] --> H["MAIN-world hook<br/>fetch / XHR"]
    H --> SW["Service worker engine<br/>PII patterns, injection heuristics,<br/>intent drift, anomaly score"]
    SW --> D{"Decision"}
    D --> AL["Allow"]
    D --> W["Warn"]
    D --> C["Confirm"]
    D --> B["Block"]
```

</details>

<details>
<summary><b>Other projects</b></summary>

<br/>

| Project | What it is | Stack |
| --- | --- | --- |
| [Nexus-AI](https://github.com/ParthVarekar/coding_game) | 2D sci-fi game that teaches Python and MLOps. Real Python runs in the browser, with a tile-based level editor and a node-graph campaign builder | JavaScript, Pyodide, Canvas, CodeMirror 6 |
| [Shorts Intelligence OS](https://github.com/ParthVarekar/shorts-intelligence-os) | Multi-agent pipeline that reads retention analytics and writes production-ready short-form video scripts, with SQLite memory and learned patterns | Python, SQLite, NVIDIA NIM |
| [Credence](https://github.com/ParthVarekar/credence_final) | Advisor and investor wealth platform built at CodeByte 2.0: risk drift detection, SIP monitoring, explainable recommendations | React, Vite, Supabase, Tailwind |
| [StudyOS](https://github.com/ParthVarekar/studyos) | Offline-first GATE 2027 prep tracker (PWA) with tests, study sessions, notes and an AI study chat | Next.js, Prisma, TanStack Query |
| [AI Voice Callbot](https://github.com/ParthVarekar/4th-sem-mini-project-call-bot-) | Voice bot that takes bookings through conversation and saves them only after explicit confirmation | Python, Flask, Gemini |
| [URL Shortener](https://github.com/ParthVarekar/url-shortener) | Full-stack workshop project with click tracking | Java, Spring Boot, React |

</details>

### Stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img alt="Languages: Python, TypeScript, JavaScript, Java, SQL. AI/ML: llama.cpp, GGUF models, RAG, NLI grounding, Gemini API, NVIDIA NIM, PyTorch. Frontend: React, Next.js, Tailwind CSS, Vite, shadcn/ui, Chrome extensions. Backend and data: Node.js, Flask, Spring Boot, Prisma, SQLite, Supabase. Tooling: Git, Linux, Docker, Vitest, GitHub Actions." src="assets/stack-light.svg" width="100%">
</picture>

### Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ParthVarekar/ParthVarekar/output/stats-dark.svg">
  <img alt="GitHub activity over the last 12 months: contributions, commits, streaks, weekly activity and languages" src="https://raw.githubusercontent.com/ParthVarekar/ParthVarekar/output/stats-light.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ParthVarekar/ParthVarekar/output/snake-dark.svg">
  <img alt="Contribution graph being eaten by a snake" src="https://raw.githubusercontent.com/ParthVarekar/ParthVarekar/output/snake-light.svg" width="100%">
</picture>

<sub>Both graphics are rebuilt every 6 hours from the GitHub API by <a href=".github/workflows/profile.yml">this workflow</a>.</sub>

### Contact

<a href="https://parthvarekar.in"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-portfolio-dark.svg"><img alt="parthvarekar.in" src="assets/btn-portfolio-light.svg" height="46"></picture></a>
<a href="https://github.com/ParthVarekar"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-follow-dark.svg"><img alt="Follow on GitHub" src="assets/btn-follow-light.svg" height="46"></picture></a>
<a href="https://github.com/ParthVarekar/ParthVarekar/issues/new?title=Hello"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-hello-dark.svg"><img alt="Say hello" src="assets/btn-hello-light.svg" height="46"></picture></a>

<img src="https://komarev.com/ghpvc/?username=ParthVarekar&label=profile%20views&color=1f5fd6&style=flat-square" alt="Profile views">
