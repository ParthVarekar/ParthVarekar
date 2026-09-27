<!-- Parth Varekar · GitHub profile · visuals in assets/ are theme-aware (light + dark) -->

<a href="https://parthvarekar.in">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
    <img alt="Parth Varekar — I build local-first AI systems: RAG engines, voice tools and developer platforms." src="assets/header-light.svg" width="100%">
  </picture>
</a>

<br/>

### ⚡ The 30-second version

|                    |                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| **What I build**   | Local-first AI software: retrieval (RAG), speech, and LLM tooling that runs on your own machine   |
| **Strongest in**   | Python · TypeScript · LLM integration (llama.cpp, Gemini, NVIDIA NIM) · React / Next.js · Node.js |
| **How I work**     | Architecture docs first, tests and benchmarks alongside, security treated as a feature            |
| **Hackathons**     | Smart India Hackathon (SIH) · CodeByte 2.0 ([Credence](https://github.com/ParthVarekar/credence_final)) |
| **Find me**        | [parthvarekar.in](https://parthvarekar.in) · or [open an issue here](https://github.com/ParthVarekar/ParthVarekar/issues/new?title=Hi%20Parth) to say hi |

<br/>

### 🧭 Featured work

<p align="left">
  <a href="https://github.com/ParthVarekar/enterprise_knowledge_assistance"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-eka-dark.svg"><img alt="Enterprise Knowledge Assistant — Slack-native RAG engine with zero-trust ACL and NLI grounding" src="assets/card-eka-light.svg" width="49%"></picture></a>
  <a href="https://github.com/ParthVarekar/Susurrus"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-whisperflow-dark.svg"><img alt="WhisperFlow — offline voice dictation with on-device ASR and LLM cleanup" src="assets/card-whisperflow-light.svg" width="49%"></picture></a>
  <a href="https://github.com/ParthVarekar/frigshwar"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-codeframe-dark.svg"><img alt="Codeframe — design canvas that exports React + Tailwind" src="assets/card-codeframe-light.svg" width="49%"></picture></a>
  <a href="https://github.com/ParthVarekar/agent_safety_net"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-agent-safety-net-dark.svg"><img alt="Agent Safety Net — runtime safety layer for AI browser agents" src="assets/card-agent-safety-net-light.svg" width="49%"></picture></a>
</p>

<details>
<summary><b>🔍 How they work under the hood</b> <sub>(click to expand architecture diagrams)</sub></summary>

<br/>

**Enterprise Knowledge Assistant.** Every chunk is permission-checked *before* retrieval, and every generated claim is verified *after* generation.

```mermaid
flowchart LR
    Q["Slack question"] --> ACL{"Zero-trust ACL<br/>per-chunk entitlements"}
    ACL -->|allowed docs only| R["Hybrid retrieval<br/>BM25 + dense vectors<br/>fused with RRF"]
    R --> LLM["Gemma 4 on llama.cpp<br/>100% CUDA offload"]
    LLM --> NLI{"NLI grounding<br/>claim-by-claim"}
    NLI -->|entailed| A["Answer + citations"]
    NLI -->|unsupported| X["Abstain"]
```

**WhisperFlow.** Speech recognition and text editing are split into two local models, so the output is polished, not just transcribed.

```mermaid
flowchart LR
    M["🎙️ Hotkey + mic"] --> ASR["Qwen3-ASR<br/>speech → raw text"]
    ASR --> P["Gemma via llama.cpp<br/>remove fillers, apply<br/>spoken formatting"]
    P --> O["Pasted into the<br/>focused app"]
```

**Codeframe.** One scene graph drives the editor, the live preview and the code exporter, so what you see is what you ship.

```mermaid
flowchart LR
    E["Canvas editor<br/>frames, layout, motion"] --> SG["Scene graph"]
    SG --> CSS["scene → CSS mapping"]
    CSS --> PV["Live HTML prototype"]
    CSS --> CG["Codegen: Vite + React<br/>+ Tailwind + shadcn/ui"]
```

**Agent Safety Net.** Decisions stay local and deterministic. The LLM only explains why something was blocked.

```mermaid
flowchart LR
    AG["AI agent on a page"] --> H["MAIN-world hook<br/>fetch / XHR"]
    H --> SW["Service-worker engine<br/>PII regex · injection heuristics<br/>intent-drift · anomaly score"]
    SW --> D{"Decision"}
    D --> AL["Allow"]
    D --> W["Warn"]
    D --> C["Confirm"]
    D --> B["Block"]
```

</details>

<details>
<summary><b>📂 More projects</b> <sub>(games, fintech, agents & more)</sub></summary>

<br/>

| Project | What it is | Stack |
| --- | --- | --- |
| [**Nexus-AI**](https://github.com/ParthVarekar/coding_game) | 2D sci-fi game that teaches Python & MLOps. Real Python runs in the browser, with a tile level editor and a node-graph campaign builder | JavaScript · Pyodide · Canvas · CodeMirror 6 |
| [**Shorts Intelligence OS**](https://github.com/ParthVarekar/shorts-intelligence-os) | Multi-agent pipeline that reads retention analytics and writes production-ready short-form scripts, with SQLite memory and learned patterns | Python · SQLite · NVIDIA NIM |
| [**Credence**](https://github.com/ParthVarekar/credence_final) | Advisor–investor wealth platform (CodeByte 2.0): risk-drift detection, SIP monitoring, explainable recommendations | React · Vite · Supabase · Tailwind |
| [**StudyOS**](https://github.com/ParthVarekar/studyos) | Offline-first GATE 2027 prep tracker PWA: tests, study sessions, notes and AI chat | Next.js · Prisma · TanStack Query |
| [**AI Voice Callbot**](https://github.com/ParthVarekar/4th-sem-mini-project-call-bot-) | Voice bot that books appointments over conversation and only saves data after explicit confirmation | Python · Flask · Gemini |
| [**URL Shortener**](https://github.com/ParthVarekar/url-shortener) | Full-stack workshop project with click tracking | Java · Spring Boot · React |

</details>

<br/>

### 🛠️ Toolbox

<a href="https://github.com/ParthVarekar?tab=repositories">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=python,ts,js,java,react,nextjs,nodejs,tailwind,vite,flask,spring,prisma,sqlite,supabase,pytorch,docker,git,linux&perline=9&theme=dark">
    <img alt="Python, TypeScript, JavaScript, Java, React, Next.js, Node.js, Tailwind, Vite, Flask, Spring, Prisma, SQLite, Supabase, PyTorch, Docker, Git, Linux" src="https://skillicons.dev/icons?i=python,ts,js,java,react,nextjs,nodejs,tailwind,vite,flask,spring,prisma,sqlite,supabase,pytorch,docker,git,linux&perline=9&theme=light">
  </picture>
</a>

**AI / LLM:** llama.cpp (CUDA) · GGUF models (Gemma, Qwen3-ASR) · Gemini API · NVIDIA NIM · RAG (BM25, embeddings, RRF) · NLI grounding

<br/>

### 📈 Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=ParthVarekar&bg_color=0d1117&color=9b968e&title_color=f3f1ec&line=ff5a1f&point=ffb38a&area=true&area_color=ff5a1f&hide_border=true&radius=12&custom_title=Contributions%20over%20the%20last%2030%20days">
  <img alt="Contribution activity graph" src="https://github-readme-activity-graph.vercel.app/graph?username=ParthVarekar&bg_color=ffffff&color=6a655c&title_color=16140f&line=e4480f&point=b8360a&area=true&area_color=e4480f&hide_border=true&radius=12&custom_title=Contributions%20over%20the%20last%2030%20days" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ParthVarekar/ParthVarekar/output/snake-dark.svg">
  <img alt="Snake eating my contribution graph" src="https://raw.githubusercontent.com/ParthVarekar/ParthVarekar/output/snake-light.svg" width="100%">
</picture>

<br/>

<p align="center">
  <a href="https://parthvarekar.in"><img src="https://img.shields.io/badge/Portfolio-parthvarekar.in-ff5a1f?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=16140f" alt="Portfolio" /></a>
  <a href="https://github.com/ParthVarekar?tab=followers"><img src="https://img.shields.io/github/followers/ParthVarekar?style=for-the-badge&logo=github&label=Follow&color=ff5a1f&labelColor=16140f" alt="Follow on GitHub" /></a>
  <a href="https://github.com/ParthVarekar/ParthVarekar/issues/new?title=Hi%20Parth"><img src="https://img.shields.io/badge/Say-hi-ff5a1f?style=for-the-badge&logo=maildotru&logoColor=white&labelColor=16140f" alt="Say hi" /></a>
</p>

<p align="center"><sub>Built the same way as everything else here: from scratch, with care, and a little too much attention to detail.</sub></p>
