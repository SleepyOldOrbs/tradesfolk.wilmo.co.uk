# Feature Research: Agent Pool Expansion (v1.1.0)

**Domain:** 8 new specialist agents for Claude Code agent pool plugin
**Researched:** 2026-02-20
**Confidence:** HIGH (domain skills verified via official docs, industry roadmaps, and current ecosystem analysis)

## Scope

This research covers what each of the 8 new agents should know, do, and avoid. It maps table-stakes capabilities (the agent is useless without these), differentiators (what makes a good system prompt great), and anti-features (scope that bleeds into other agents or creates confusion).

All 8 agents follow the established three-section system prompt pattern:
1. **Core expertise** -- bullet list of specific technologies and skills
2. **Working standards** -- concrete rules the agent follows
3. **When given a task** -- numbered workflow steps

---

## Agent 13: react-native-developer

**Colour:** Blue | **Tools:** Implementation | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| React Native core (components, navigation, styling) | Foundation of every RN task | LOW | StyleSheet, FlatList, ScrollView, SafeAreaView, Platform API |
| Expo SDK (52+) and managed workflow | Expo is now the default starting point for RN projects; SDK 52+ enables New Architecture by default | LOW | expo-router, expo-modules, EAS Build/Submit, expo-dev-client |
| New Architecture (Fabric renderer, TurboModules, JSI) | Enabled by default since SDK 52. Agent must not produce old-bridge code | MEDIUM | Fabric replaces the old renderer; TurboModules replace NativeModules; JSI enables synchronous native calls |
| React Navigation 7+ | Standard navigation library | LOW | Stack, Tab, Drawer navigators, deep linking, TypeScript-first API |
| TypeScript with strict mode | RN ecosystem has fully standardised on TS | LOW | Matches javascript-developer's TS standards |
| Platform-specific code handling | iOS and Android have different capabilities and UX patterns | LOW | Platform.select, .ios.tsx/.android.tsx file extensions, platform-specific imports |
| App store build and submission (EAS Build) | Shipping is the whole point of mobile dev | MEDIUM | EAS Build for cloud builds, EAS Submit for store submission, OTA updates with expo-updates |
| Mobile testing (Jest, React Native Testing Library, Detox) | Cannot ship untested mobile code | MEDIUM | Unit tests with Jest, component tests with RNTL, E2E with Detox or Maestro |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| Native module bridging (Expo Modules API) | Accessing platform APIs not covered by Expo packages -- camera, sensors, Bluetooth | MEDIUM | Expo Modules API is the modern approach; avoids raw Java/Swift bridging |
| Performance profiling (Flipper, Hermes profiler, React DevTools) | Mobile perf is harder to diagnose than web; agent should know the toolchain | MEDIUM | Hermes is the default JS engine; flipper for network/layout/performance debugging |
| Animated API and Reanimated 3 | Smooth 60fps animations are table stakes for native feel | MEDIUM | Reanimated 3 for worklet-based animations running on UI thread, gesture handler integration |
| Offline-first architecture patterns | Mobile apps must handle connectivity gracefully | MEDIUM | AsyncStorage, MMKV, WatermelonDB; network state detection; sync strategies |
| Deep linking and universal links | Mobile app discovery and cross-platform navigation | LOW | expo-linking, app.json scheme config, associated domains |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| Full native iOS/Android code writing | "React Native developer should handle everything mobile" | Dilutes the agent's React Native focus; native code is ios-developer and android-developer territory | Delegate native module implementation to ios-developer or android-developer when bridging requires significant platform-specific code |
| Web-specific React patterns (RSC, server actions, Next.js routing) | React Native uses React, so web React patterns might seem relevant | RN has no server components, no SSR, no hydration. Including these confuses the agent | Keep web React in react-specialist; this agent is mobile-only |
| Flutter or KMP code | Cross-platform mobile is a spectrum | Different languages, different paradigms. RN developer writes JavaScript/TypeScript | Not in scope. These would need separate agents if ever added |

### Boundary with Existing Agents

- **react-specialist**: Web React (RSC, Next.js, hydration). react-native-developer handles mobile React (native components, Expo, app stores). No overlap.
- **javascript-developer**: Build tooling, module systems, vanilla TS. react-native-developer uses Metro bundler but delegates Node.js backend work to javascript-developer.
- **ux-designer**: Handles mobile UX review, responsive design, accessibility. react-native-developer handles implementation of those designs in RN.

---

## Agent 14: ios-developer

**Colour:** Blue | **Tools:** Implementation | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| Swift 6 (strict concurrency, actors, async/await, Sendable) | Swift 6 enforces data-race safety at compile time; agent must write concurrency-safe code | MEDIUM | Strict concurrency checking, global actors, distributed actors |
| SwiftUI (views, modifiers, state management, navigation) | SwiftUI is Apple's primary UI framework for all new development | LOW | @State, @Binding, @Observable (Observation framework), NavigationStack, .sheet/.fullScreenCover |
| UIKit (table views, collection views, view controller lifecycle) | Legacy apps and complex custom UI still require UIKit; SwiftUI interop via UIViewRepresentable | MEDIUM | Agent must handle both pure SwiftUI and UIKit-bridged scenarios |
| SwiftData (models, queries, relationships, CloudKit sync) | Apple's modern persistence framework, replacing Core Data for new projects | MEDIUM | @Model macro, @Query, ModelContainer/ModelContext, migration support |
| Xcode project structure and build settings | Every iOS project lives in Xcode | LOW | Targets, schemes, build configurations, entitlements, code signing, SPM integration |
| App Store submission (App Store Connect, TestFlight) | Shipping requires understanding Apple's submission pipeline | LOW | Provisioning profiles, certificates, review guidelines, TestFlight distribution |
| Swift Package Manager | Standard dependency management for Swift | LOW | Package.swift, binary targets, local packages |
| XCTest and Swift Testing framework | Testing is non-negotiable | MEDIUM | @Test macro, #expect, parameterised tests, UI testing with XCUITest |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| Combine and Observation framework | Reactive data flow is central to modern iOS apps | MEDIUM | Observation framework (@Observable) is the modern replacement for ObservableObject; Combine still used for publishers/operators |
| Core ML and CreateML | On-device ML is a growing iOS differentiator | HIGH | Model conversion, inference pipeline, Vision framework integration |
| App Clips, Widgets (WidgetKit), Live Activities | Platform-specific features that extend beyond the main app | MEDIUM | WidgetKit timelines, App Intents integration, Dynamic Island |
| Accessibility (VoiceOver, Dynamic Type, accessibility modifiers) | Apple mandates and promotes accessibility heavily | MEDIUM | .accessibilityLabel, .accessibilityHint, Dynamic Type scaling, VoiceOver navigation |
| Performance profiling with Instruments | Xcode Instruments is the standard iOS profiling tool | MEDIUM | Time Profiler, Allocations, Leaks, Core Animation, Network instruments |
| StoreKit 2 (in-app purchases, subscriptions) | Monetisation is a core mobile capability | MEDIUM | Product types, Transaction listeners, subscription status, receipt validation |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| Android/Kotlin code generation | "Mobile developer should do both platforms" | Completely different language, tools, and platform APIs | android-developer handles Kotlin/Android exclusively |
| React Native bridging code | "iOS dev should write the native modules for RN" | RN bridging has its own patterns (Expo Modules API, TurboModules); mixing native-app dev with RN bridging muddles both | react-native-developer handles RN-specific bridging; ios-developer only writes pure iOS code |
| Backend API development | "iOS dev should build the API too" | Backend architecture is a separate domain | backend-architect and python-developer handle API work |
| macOS/visionOS/watchOS app development | "Apple developer should cover all platforms" | Each platform has distinct UI paradigms and frameworks; covering all dilutes iOS expertise | Keep focused on iOS (iPhone/iPad). Platform expansion is a future consideration |

### Boundary with Existing Agents

- **react-native-developer**: RN uses a JS runtime with native components. ios-developer writes pure Swift/UIKit/SwiftUI. They collaborate when RN needs custom native modules, but the ios-developer writes the Swift side independently.
- **ux-designer**: Designs the UI patterns; ios-developer implements them in SwiftUI/UIKit.
- **security-auditor**: Reviews iOS-specific security (Keychain usage, App Transport Security, certificate pinning); ios-developer implements the fixes.

---

## Agent 15: android-developer

**Colour:** Green | **Tools:** Implementation | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| Kotlin (coroutines, flows, sealed classes, extension functions, DSLs) | Kotlin is the primary language for Android; coroutines are essential for async work | LOW | Structured concurrency with coroutineScope, Flow for reactive streams, StateFlow/SharedFlow |
| Jetpack Compose (composables, state, theming, navigation) | Google's modern declarative UI toolkit, required for all new Android development | LOW | remember, mutableStateOf, LazyColumn/LazyGrid, Material 3, Compose Navigation |
| Android SDK fundamentals (Activities, Fragments, lifecycle, intents) | Still required for system integration even in Compose-first apps | MEDIUM | Fragment interop, Activity lifecycle, broadcast receivers, content providers |
| Room database (entities, DAOs, migrations, relationships) | Standard local persistence for Android | MEDIUM | @Entity, @Dao, @Database, TypeConverters, auto-migrations |
| Gradle build system (Kotlin DSL, version catalogs, build variants) | Every Android project uses Gradle | LOW | libs.versions.toml, buildSrc/convention plugins, product flavors, build types |
| Play Store submission (Play Console, internal/closed/open testing) | Shipping is the point | LOW | App bundles (AAB), signing configs, staged rollouts, Play Console policies |
| Dependency injection (Hilt/Dagger, Koin) | Standard architecture pattern for testable Android code | MEDIUM | Hilt is Google's recommended DI; Koin for simpler setups |
| Android testing (JUnit 5, Compose Testing, Espresso, Robolectric) | Testing is non-negotiable | MEDIUM | createComposeRule, onNodeWithText, Espresso for view-based UI, Robolectric for JVM-side tests |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| Architecture patterns (MVVM with ViewModel, MVI, Clean Architecture) | Well-structured Android apps follow established architectural patterns | MEDIUM | ViewModel with SavedStateHandle, UiState sealed classes, Repository pattern, UseCases |
| WorkManager and background processing | Android's strict background execution limits require proper scheduling | MEDIUM | OneTimeWorkRequest, PeriodicWorkRequest, constraints, chaining, expedited work |
| Kotlin Multiplatform (KMP) shared logic | KMP adoption is surging (7% to 23% in one year); sharing business logic across platforms | HIGH | expect/actual, KMP modules for networking/data/domain, Compose Multiplatform for shared UI |
| App performance (Baseline Profiles, R8, startup optimization) | Android has more device fragmentation requiring performance attention | MEDIUM | Baseline Profiles for AOT compilation, R8 shrinking/obfuscation, Macrobenchmark |
| Jetpack libraries (CameraX, Media3, Health Connect) | Platform-specific capabilities that differentiate mobile apps | MEDIUM | CameraX for camera, Media3 for audio/video, Health Connect for fitness data |
| Material 3 Dynamic Color and adaptive layouts | Modern Android design language with per-device theming | LOW | Dynamic color from wallpaper, WindowSizeClass for adaptive layouts, Material 3 components |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| iOS/Swift code | "Mobile developer should do both" | Different language, different IDE, different platform APIs | ios-developer handles Swift/iOS |
| React Native Java/Kotlin native modules | "Android dev writes the Android side of RN modules" | RN bridging has its own patterns and is handled by react-native-developer | react-native-developer owns the full RN stack including native module bridging |
| Backend/server development in Kotlin | "Kotlin works on servers too (Ktor, Spring)" | Server-side Kotlin is a different domain | backend-architect and python-developer handle server-side work |

### Boundary with Existing Agents

- **react-native-developer**: RN handles cross-platform mobile with JS. android-developer writes pure Kotlin/Compose. They collaborate on "Native iOS+Android" template but work independently.
- **devops-engineer**: Handles CI/CD pipeline config (GitHub Actions for Android builds). android-developer focuses on Gradle config and app-level build settings.
- **database-specialist**: Handles server-side database design. android-developer handles local Room database setup.

---

## Agent 16: embedded-engineer

**Colour:** Cyan | **Tools:** Full access | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| C for embedded (bare-metal, register-level, memory-mapped I/O) | C remains the backbone of firmware development; most MCU SDKs are C-based | LOW | Volatile qualifiers, bit manipulation, linker scripts, startup code |
| C++ for embedded (RAII, templates, constexpr, no-exceptions/no-RTTI builds) | C++ is increasingly used for larger embedded projects with OOP benefits | MEDIUM | Compile-time computation, zero-cost abstractions, embedded-friendly subset |
| RTOS fundamentals (FreeRTOS, Zephyr) | Most non-trivial embedded systems need real-time task scheduling | MEDIUM | Tasks/threads, semaphores, mutexes, message queues, ISR-safe APIs, priority inversion avoidance |
| Microcontroller architectures (ARM Cortex-M, ESP32, STM32, nRF) | Must understand target hardware to write effective firmware | MEDIUM | Memory-mapped peripherals, interrupt vectors, clock trees, DMA, sleep modes |
| Communication protocols (SPI, I2C, UART, CAN) | Hardware communication is fundamental to embedded work | LOW | Bus timing, addressing modes, protocol-specific error handling, logic analyser interpretation |
| Build toolchains (GCC ARM, CMake, Make, PlatformIO) | Embedded builds are not npm install; cross-compilation is the norm | MEDIUM | Cross-compilation toolchains, linker scripts, memory layout, build flags for size/speed optimisation |
| Hardware debugging (JTAG/SWD, GDB, logic analysers, oscilloscopes) | printf debugging is insufficient for real-time embedded systems | MEDIUM | OpenOCD, J-Link, breakpoints in ISRs, peripheral register inspection |
| Power management and low-power design | Battery-powered IoT devices must minimise power consumption | MEDIUM | Sleep modes, clock gating, wake sources, current measurement, duty cycling |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| IoT protocols (MQTT, CoAP, BLE, LoRaWAN, Zigbee, Thread/Matter) | IoT connectivity is the primary reason embedded skills are in demand in 2026 | HIGH | MQTT for cloud telemetry, BLE for local device communication, Matter for smart home interoperability |
| OTA firmware updates | Production IoT devices need field-updatable firmware | HIGH | Dual-bank flash, bootloader design, delta updates, rollback mechanisms, signature verification |
| Zephyr RTOS (devicetree, Kconfig, west build system) | Zephyr is the rising standard for production IoT; Linux Foundation backed with broad vendor support | HIGH | Zephyr's devicetree-driven hardware abstraction, west meta-tool, Kconfig configuration system |
| Safety-critical firmware patterns | Embedded code in medical, automotive, or industrial contexts requires formal rigour | HIGH | Watchdog timers, stack overflow detection, MISRA C compliance, defensive programming, fault injection testing |
| Embedded Rust (no_std, embassy, RTIC) | Rust is gaining traction in embedded for memory safety without GC overhead | HIGH | no_std crates, Hardware Abstraction Layer (HAL) traits, embassy async runtime for embedded |
| Sensor fusion and signal processing | IoT devices often combine multiple sensor inputs | MEDIUM | Kalman filters, moving averages, digital filtering, sensor calibration routines |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| Cloud/server backend development | "IoT needs a cloud backend" | Cloud infrastructure is devops-engineer and backend-architect territory | embedded-engineer writes firmware; devops-engineer deploys the cloud side |
| Mobile companion app development | "IoT devices often have mobile apps" | Mobile apps are react-native-developer/ios-developer/android-developer territory | Delegate companion app work to the appropriate mobile agent |
| Full Linux kernel development | "Embedded Linux is embedded" | This agent targets constrained devices (MCUs, RTOS). Full Linux is systems-programmer territory | systems-programmer handles Linux kernel modules, device drivers for full Linux |
| PCB design and hardware schematics | "Embedded engineer should do hardware too" | Hardware design requires different tools (KiCad, Altium) and a different skillset. Claude Code edits code, not schematics | Keep focused on firmware and software; hardware design is out of scope for a code agent |

### Boundary with Existing Agents

- **systems-programmer**: Handles Rust/Go/C++ for desktop/server performance work, full Linux systems. embedded-engineer handles constrained MCU environments, RTOS, bare-metal.
- **devops-engineer**: Handles cloud infrastructure, CI/CD. embedded-engineer handles firmware CI (cross-compilation, flash scripting) but delegates cloud deployment.
- **security-auditor**: Reviews firmware for security issues (hardcoded keys, unencrypted OTA). embedded-engineer implements the secure patterns.

---

## Agent 17: llm-application-developer

**Colour:** Magenta | **Tools:** Implementation | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| LLM API integration (OpenAI, Anthropic, Google, open-source) | Every LLM app starts with API calls; agent must handle multiple providers | LOW | Chat completions, streaming, function calling/tool use, structured outputs, model selection |
| RAG pipeline design (chunking, embedding, retrieval, generation) | RAG is the most common LLM application pattern in production | MEDIUM | Document ingestion, text splitting strategies, embedding models (OpenAI, Cohere, open-source), retrieval with reranking, context window management |
| Vector databases (Pinecone, ChromaDB, Weaviate, pgvector, Qdrant) | Vector stores are the backbone of RAG and semantic search | MEDIUM | Index creation, metadata filtering, hybrid search (dense + sparse), batch upserts, distance metrics |
| Orchestration frameworks (LangChain, LangGraph, LlamaIndex) | Standard tooling for chaining LLM calls, managing context, building agents | MEDIUM | LlamaIndex for RAG-heavy apps, LangGraph for agentic workflows with cycles, choosing the right framework for the task |
| Prompt management (templating, versioning, few-shot examples) | Production LLM apps need managed, testable prompts | LOW | Jinja/f-string templates, prompt versioning, few-shot example selection, system/user/assistant message construction |
| Structured output parsing (JSON mode, function calling, Pydantic) | LLM outputs must be reliably parsed into application data structures | LOW | OpenAI JSON mode, Anthropic tool use for structured output, Pydantic models for validation, retry on parse failure |
| Token management and cost optimization | LLM API costs scale with tokens; production apps must manage this | LOW | Token counting (tiktoken), context window budgeting, prompt compression, caching strategies |
| Error handling for LLM calls (retries, fallbacks, rate limits) | LLM APIs are unreliable; production code must handle failures gracefully | LOW | Exponential backoff, fallback models, rate limit detection, timeout handling, graceful degradation |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| Agent orchestration (tool use, multi-step reasoning, self-correction) | Agentic AI is the frontier of LLM applications in 2026 | HIGH | ReAct pattern, tool definition and execution, agent loops with termination conditions, multi-agent coordination |
| Evaluation and testing (LLM-as-judge, reference-based, custom metrics) | LLM outputs are non-deterministic; testing requires specialised approaches | HIGH | Promptfoo, RAGAS for RAG evaluation, LLM-as-judge patterns, human evaluation pipelines, regression testing |
| Advanced RAG patterns (hybrid search, reranking, query transformation) | Basic RAG has known limitations; production systems need advanced retrieval | HIGH | HyDE (hypothetical document embeddings), query decomposition, cross-encoder reranking, parent-child chunk retrieval, graph RAG |
| Guardrails and safety (input/output filtering, content moderation) | Production LLM apps need safety boundaries | MEDIUM | Input validation, output filtering, PII detection, topic boundaries, prompt injection defense |
| Streaming and real-time responses | Users expect responsive LLM interactions, not 30-second waits | MEDIUM | Server-sent events, WebSocket streaming, token-by-token rendering, streaming with tool calls |
| Multi-modal inputs (images, audio, documents) | Modern LLMs support multiple input types; apps should leverage this | MEDIUM | Vision API integration, document parsing (PDF, images), audio transcription pipeline |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| Model training and fine-tuning | "LLM developer should train models" | Training is data-scientist territory; this agent builds applications that use LLMs, not the LLMs themselves | data-scientist handles training/fine-tuning; llm-application-developer handles inference and application logic |
| System prompt crafting and optimization | "LLM app dev should write the prompts" | Prompt design is a distinct skill with its own methodology | prompt-engineer handles prompt design, evaluation, and optimization; llm-application-developer integrates the prompts into the application |
| Model deployment and serving infrastructure | "Need to deploy the model" | Infrastructure and serving are mlops-engineer territory | mlops-engineer handles model serving (vLLM, TGI, Triton); llm-application-developer calls the served API |
| General web application development | "LLM apps are web apps" | The LLM-specific patterns (RAG, agents, streaming) are the value; generic web dev goes elsewhere | react-specialist and javascript-developer handle the frontend; python-developer handles non-LLM backend logic |

### Boundary with Existing Agents

- **data-scientist**: Trains models, runs experiments, analyses data. llm-application-developer builds production applications that consume LLMs via APIs. The boundary is inference-time vs training-time.
- **prompt-engineer**: Designs and evaluates prompts. llm-application-developer integrates those prompts into application code with proper templating, versioning, and error handling.
- **python-developer**: Handles general Python web development (FastAPI, Django). llm-application-developer handles the LLM-specific patterns (RAG pipelines, agent loops, vector stores).
- **backend-architect**: Designs the overall system architecture. llm-application-developer implements the LLM-specific components within that architecture.

---

## Agent 18: prompt-engineer

**Colour:** Magenta | **Tools:** Documentation | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| Prompt design patterns (zero-shot, few-shot, chain-of-thought, ReAct) | Core vocabulary of prompt engineering | LOW | When to use each pattern, how to structure examples, chain-of-thought formatting |
| System prompt architecture (role, constraints, output format, examples) | System prompts are the primary interface for LLM behavior specification | LOW | Clear role definition, explicit constraints, output contracts, success criteria |
| Model-specific prompt optimization | Different models respond differently to the same prompt | MEDIUM | Claude prefers logic-first prompts with XML tags; GPT benefits from redundant constraints with markdown headers; Gemini prefers structured separation |
| Output structuring (JSON schemas, XML tags, markdown formatting) | LLM outputs must be reliably structured for downstream consumption | LOW | JSON mode prompts, XML tag patterns, structured output specifications, format enforcement |
| Evaluation methodology (automated scoring, human evaluation, A/B testing) | Prompts must be measurably good, not subjectively "fine" | MEDIUM | Promptfoo for automated evaluation, scoring rubrics, multi-criteria evaluation, statistical significance |
| Few-shot example selection and curation | Example quality directly determines output quality | LOW | Representative examples, edge case coverage, negative examples, example ordering effects |
| Prompt versioning and documentation | Production prompts need change tracking and rationale documentation | LOW | Version numbering, changelog, performance metrics per version, A/B test results |
| Failure mode analysis (hallucination, refusal, format breaking, drift) | Understanding how prompts fail is essential for improving them | MEDIUM | Hallucination triggers, refusal patterns, edge cases that break formatting, prompt injection vectors |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| Red-teaming and adversarial testing | Finding prompt vulnerabilities before production | HIGH | Prompt injection attacks, jailbreak attempts, boundary testing, PyRIT/Promptfoo red-team modules |
| Multi-turn conversation design | Many LLM applications involve multi-turn interactions that need careful design | MEDIUM | Context management across turns, conversation state tracking, graceful topic transitions, memory summarization |
| Evaluation pipeline design (automated regression testing) | Continuous prompt quality assurance | HIGH | Test suites for prompts, regression detection, performance dashboards, CI integration for prompt changes |
| Prompt compression and token optimization | Reducing token usage while maintaining output quality | MEDIUM | Removing redundant instructions, concise example selection, dynamic prompt assembly based on input |
| Task decomposition for complex prompts | Breaking complex tasks into manageable prompt chains | MEDIUM | When to use single vs multi-step prompts, intermediate validation, conditional branching |
| Domain-specific prompt libraries | Reusable prompt patterns for common use cases | LOW | Summarization, classification, extraction, generation, translation, code generation patterns |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| Application code writing | "Prompt engineer should build the app that uses the prompts" | Code implementation is llm-application-developer or python-developer territory | prompt-engineer writes and evaluates prompts; developers integrate them |
| Model training or fine-tuning | "If prompts aren't enough, fine-tune" | Training is data-scientist territory; prompt-engineer maximizes what can be achieved without training | Escalate to data-scientist when prompt engineering hits its ceiling |
| UI/UX design for chatbots | "Prompt engineer should design the conversation UI" | UI design is ux-designer territory | ux-designer handles the interface; prompt-engineer handles the conversation logic |
| Infrastructure or deployment work | "Deploy the prompts to production" | Deployment is devops-engineer territory | prompt-engineer documents prompts; devops-engineer and llm-application-developer handle deployment |

### Boundary with Existing Agents

- **llm-application-developer**: Builds the application code around prompts. prompt-engineer crafts the prompts themselves, evaluates them, and documents their behavior.
- **data-scientist**: Analyses model performance quantitatively. prompt-engineer focuses on prompt-level evaluation (does this prompt produce the right output?), not model-level metrics.
- **technical-writer**: Both produce documentation. prompt-engineer documents prompts and evaluation results; technical-writer documents APIs, user guides, and architecture.

### Why Documentation Tier Tools

prompt-engineer gets Read, Grep, Glob, Write, Edit, Bash -- the Documentation tier. This is intentional. Prompt engineering is a design and evaluation activity. The agent reads existing prompts, writes new ones, runs evaluation scripts via Bash, and documents results. It does not write application code (no MultiEdit, no NotebookEdit needed).

---

## Agent 19: mlops-engineer

**Colour:** Cyan | **Tools:** Full access | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| Experiment tracking (MLflow, Weights & Biases, Neptune) | Reproducible ML requires logging parameters, metrics, and artifacts | MEDIUM | MLflow tracking server setup, run logging, artifact storage, experiment comparison |
| Model registry and versioning | Production ML needs versioned, staged models with metadata | MEDIUM | MLflow Model Registry, model staging (dev/staging/prod), model lineage, approval workflows |
| Training pipelines (Kubeflow Pipelines, Airflow, Prefect) | Automated, reproducible training workflows | HIGH | DAG-based pipeline definition, component reuse, caching, parameterised runs |
| Model serving (TorchServe, Triton, vLLM, TGI, BentoML) | Models must be served as scalable, monitored endpoints | HIGH | REST/gRPC endpoints, batching, GPU scheduling, model warm-up, A/B serving |
| Containerisation for ML (Docker, NVIDIA Container Toolkit) | ML workloads need reproducible environments with GPU support | MEDIUM | Multi-stage builds for ML, CUDA base images, pip freeze for determinism, GPU passthrough |
| GPU infrastructure (CUDA, scheduling, multi-GPU training) | Modern ML requires GPU management | HIGH | CUDA toolkit, nvidia-smi monitoring, multi-GPU data parallelism, GPU memory management |
| Model monitoring and drift detection | Production models degrade over time; monitoring catches this | MEDIUM | Data drift, concept drift, prediction drift, feature importance shift, alerting thresholds |
| CI/CD for ML (automated retraining, validation gates, deployment) | ML needs its own CI/CD patterns beyond traditional software CI | HIGH | Training triggered by data changes, validation gates (accuracy thresholds), shadow deployment, canary rollout |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| LLMOps (prompt tracking, LLM evaluation pipelines, fine-tuning infra) | LLM-specific operations are the fastest-growing MLOps subfield in 2026 | HIGH | Prompt versioning, LLM evaluation (RAGAS, promptfoo), fine-tuning pipelines (LoRA/QLoRA), inference cost tracking |
| Feature stores (Feast, Tecton) | Centralised feature management for consistent training and serving | HIGH | Feature definitions, online/offline stores, point-in-time joins, feature freshness |
| Data versioning (DVC, LakeFS) | ML reproducibility requires versioned datasets alongside versioned code | MEDIUM | DVC for Git-integrated data versioning, LakeFS for data lake versioning, lineage tracking |
| Kubernetes for ML (KubeFlow, Ray, Volcano scheduler) | Scaling ML workloads on K8s requires specialised scheduling | HIGH | GPU-aware scheduling, distributed training operators, job queuing, resource quotas |
| Cost optimization for ML infrastructure | GPU compute is expensive; optimisation is a core MLOps concern | MEDIUM | Spot/preemptible instances, right-sizing GPU selection, inference batching, model quantisation for serving |
| A/B testing and shadow deployment for models | Safe model deployment requires comparing new vs old in production | MEDIUM | Traffic splitting, shadow mode (run new model alongside old without serving), statistical comparison |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| Model architecture design | "MLOps should pick the model architecture" | Model design is data-scientist territory; MLOps deploys what data scientists build | data-scientist designs models; mlops-engineer deploys and operates them |
| Data analysis and feature engineering | "MLOps touches data" | Data analysis is data-scientist work; MLOps manages the infrastructure for data pipelines | data-scientist does analysis; mlops-engineer builds the pipeline infrastructure |
| General Kubernetes/cloud administration | "MLOps runs on K8s" | General K8s management is devops-engineer territory; mlops-engineer handles ML-specific K8s patterns | devops-engineer manages the cluster; mlops-engineer manages ML workloads on it |
| Application code for LLM products | "MLOps for LLMs" | Application code is llm-application-developer territory | mlops-engineer handles serving and monitoring; llm-application-developer writes the app |

### Boundary with Existing Agents

- **data-scientist**: Designs experiments, trains models, analyses results. mlops-engineer takes those models to production -- building pipelines, serving infrastructure, and monitoring.
- **devops-engineer**: Manages general infrastructure (CI/CD, K8s, cloud). mlops-engineer specialises in ML-specific infrastructure (GPU scheduling, model serving, experiment tracking). They share Cyan colour because both are infrastructure roles.
- **llm-application-developer**: Builds LLM applications. mlops-engineer handles the operational side -- model serving, fine-tuning pipelines, inference monitoring.

---

## Agent 20: computer-vision-engineer

**Colour:** Magenta | **Tools:** Implementation | **Permission:** default

### Table Stakes

| Capability | Why Essential | Complexity | Notes |
|------------|---------------|------------|-------|
| Image processing fundamentals (OpenCV, PIL/Pillow, scikit-image) | Foundation of all CV work: loading, transforming, filtering, annotating images | LOW | Colour spaces, geometric transforms, filtering, morphological operations, contour detection |
| Deep learning for vision (PyTorch, torchvision, timm) | Modern CV is deep-learning-first; PyTorch is the dominant framework | MEDIUM | CNN architectures, transfer learning, fine-tuning pre-trained models, data augmentation |
| Object detection (YOLO, Detectron2, RT-DETR) | The most common production CV task | MEDIUM | YOLOv8/v11 for real-time detection, Detectron2 for research, anchor-free vs anchor-based, NMS, mAP evaluation |
| Image classification and feature extraction | Fundamental CV task; also used as backbone for other tasks | LOW | ResNet, EfficientNet, ViT, transfer learning, feature extraction for downstream tasks |
| Image segmentation (semantic, instance, panoptic) | Required for scene understanding, medical imaging, autonomous systems | MEDIUM | SAM (Segment Anything Model), Mask R-CNN, U-Net, pixel-level evaluation (mIoU, Dice) |
| Data pipeline for vision (dataset loading, augmentation, preprocessing) | CV models need properly managed data pipelines | MEDIUM | PyTorch DataLoader, albumentations for augmentation, COCO/VOC format handling, annotation tools |
| Model evaluation and metrics (precision, recall, mAP, IoU, confusion matrices) | CV models need quantitative evaluation beyond "looks right" | LOW | mAP@50/75, IoU thresholds, per-class metrics, confusion matrices, qualitative failure analysis |
| Training loop fundamentals (loss functions, optimizers, schedulers, mixed precision) | Must understand training mechanics to fine-tune or train from scratch | MEDIUM | CrossEntropy, focal loss, AdamW, cosine annealing, AMP (automatic mixed precision), gradient accumulation |

### Differentiators

| Capability | Value Proposition | Complexity | Notes |
|------------|-------------------|------------|-------|
| Vision-language models (CLIP, BLIP, Florence, GPT-4V integration) | Multimodal AI is the frontier; combining vision with language understanding | HIGH | CLIP for zero-shot classification, BLIP for image captioning, GPT-4V for visual QA, embedding-based search |
| OCR and document understanding (Tesseract, PaddleOCR, DocTR, LayoutLM) | Document processing is a high-demand production use case | MEDIUM | Text extraction, layout analysis, table detection, form parsing, handwriting recognition |
| Diffusion models (Stable Diffusion, SDXL, ControlNet, ComfyUI) | Image generation and editing are rapidly adopted capabilities | HIGH | txt2img, img2img, inpainting, ControlNet for guided generation, LoRA training for custom styles |
| Edge deployment (ONNX, TensorRT, Core ML, TFLite) | Production CV often runs on devices, not cloud servers | HIGH | Model export to ONNX, TensorRT optimization, quantisation (INT8/FP16), inference benchmarking |
| Video analysis (tracking, action recognition, temporal models) | Video extends CV from frames to sequences | HIGH | Object tracking (ByteTrack, DeepSORT), temporal models, frame extraction, video segmentation |
| 3D vision (depth estimation, point clouds, NeRF) | Emerging domain for AR/VR, robotics, and spatial computing | HIGH | Monocular depth estimation, stereo matching, point cloud processing (Open3D), 3D reconstruction |

### Anti-Features

| Anti-Feature | Why Tempting | Why Problematic | Alternative |
|-------------|--------------|-----------------|-------------|
| General-purpose ML/data science | "CV engineer should handle all ML tasks" | Tabular ML, NLP (non-vision), time series are different domains | data-scientist handles general ML; computer-vision-engineer handles vision-specific work |
| Frontend/UI for displaying results | "Need to show the detection results in a web app" | Web development is react-specialist territory | react-specialist builds the display; computer-vision-engineer provides the vision pipeline |
| Model deployment infrastructure | "Need to serve the model" | Model serving is mlops-engineer territory | mlops-engineer handles TorchServe/Triton deployment; computer-vision-engineer builds the model |
| Robotics control systems | "CV is used in robotics" | Control systems, motion planning, and ROS are beyond CV scope | Computer-vision-engineer provides the perception pipeline; robotics would need a separate agent (out of scope) |

### Boundary with Existing Agents

- **data-scientist**: Handles general ML (tabular, NLP, statistics, experiment design). computer-vision-engineer handles vision-specific models, datasets, and evaluation.
- **llm-application-developer**: Handles LLM API integration including multimodal inputs. computer-vision-engineer handles the computer vision processing that feeds into or supplements LLM applications.
- **mlops-engineer**: Deploys and monitors models. computer-vision-engineer builds and trains the vision models that mlops-engineer then serves.

---

## Feature Dependencies

```
[react-native-developer]
    (no dependencies on other new agents)
    └──collaborates-with──> [ios-developer] (native module bridging)
    └──collaborates-with──> [android-developer] (native module bridging)

[ios-developer]
    (no dependencies on other new agents)
    └──collaborates-with──> [android-developer] (Native iOS+Android template)

[android-developer]
    (no dependencies on other new agents)
    └──collaborates-with──> [ios-developer] (Native iOS+Android template)

[embedded-engineer]
    (no dependencies on other new agents)
    └──collaborates-with──> [systems-programmer] (IoT System template)

[llm-application-developer]
    └──collaborates-with──> [prompt-engineer] (AI Application template)
    └──collaborates-with──> [computer-vision-engineer] (multimodal AI apps)

[prompt-engineer]
    └──collaborates-with──> [llm-application-developer] (AI Application template)
    └──collaborates-with──> [data-scientist] (evaluation methodology)

[mlops-engineer]
    └──collaborates-with──> [data-scientist] (ML Pipeline template)
    └──collaborates-with──> [computer-vision-engineer] (model deployment)
    └──collaborates-with──> [devops-engineer] (infrastructure overlap)

[computer-vision-engineer]
    └──collaborates-with──> [data-scientist] (training methodology, experiment design)
    └──collaborates-with──> [mlops-engineer] (model serving and deployment)
```

### Dependency Notes

- **No sequential dependencies exist.** All 8 agents can be written in parallel because they are independent markdown files. The "collaborates-with" relationships are advisory -- they inform team template composition and assemble-team recommendations, not build order.
- **llm-application-developer and prompt-engineer are the tightest pair.** Their boundary must be crisp: prompt-engineer designs prompts, llm-application-developer integrates them into applications. The description examples must make this distinction unmistakable.
- **mlops-engineer and devops-engineer share Cyan colour and infrastructure overlap.** The distinction is ML-specific vs general infrastructure. The description examples must clearly route "deploy my model" to mlops-engineer and "deploy my web app" to devops-engineer.
- **computer-vision-engineer and data-scientist share Magenta colour and ML overlap.** The distinction is vision-specific vs general ML. Description examples must route "detect objects in images" to computer-vision-engineer and "predict customer churn" to data-scientist.

---

## Updated Team Templates (5 new)

These are the 5 new team templates from the approved design, with rationale for each composition:

| # | Template | Lead | Members | Rationale |
|---|----------|------|---------|-----------|
| 8 | Mobile App | react-native-developer | ux-designer, qa-tester | Cross-platform mobile. RN developer leads because the app is JS-based. UX for mobile design patterns, QA for mobile testing. |
| 9 | Native iOS + Android | ios-developer | android-developer, ux-designer, qa-tester | Platform-native. iOS developer leads (arbitrary; could be Android). Both platform specialists work independently. UX and QA are shared. |
| 10 | AI Application | llm-application-developer | prompt-engineer, python-developer, qa-tester | LLM-powered features. LLM developer leads application architecture. Prompt engineer crafts the prompts. Python developer handles non-LLM backend. QA tests the non-deterministic outputs. |
| 11 | ML Pipeline | mlops-engineer | data-scientist, python-developer, devops-engineer | Training and serving. MLOps leads infrastructure. Data scientist handles model design. Python developer handles data processing code. DevOps provides general infra support. |
| 12 | IoT System | embedded-engineer | systems-programmer, devops-engineer | Firmware and device management. Embedded engineer leads firmware. Systems programmer handles performance-critical gateway code. DevOps handles cloud-side deployment. |

---

## Updates to Existing Skills

### assemble-team

Must add 8 new entries to the agent roster table:

| Agent | Domain |
|-------|--------|
| react-native-developer | React Native, Expo, mobile UI, native modules, app store builds |
| ios-developer | Swift, SwiftUI, UIKit, Core Data, Xcode, App Store |
| android-developer | Kotlin, Jetpack Compose, Room, Gradle, Play Store |
| embedded-engineer | C/C++ firmware, RTOS, microcontrollers, IoT protocols |
| llm-application-developer | RAG pipelines, vector stores, agent orchestration, LLM APIs |
| prompt-engineer | System prompt design, evaluation, red-teaming, output structuring |
| mlops-engineer | Model serving, experiment tracking, training pipelines, GPU infra |
| computer-vision-engineer | Image/video processing, object detection, diffusion models, OpenCV/PyTorch |

### browse-pool

Must add the 8 new agents to the roster display, grouped under two new headings:
- **Platform Specialists**: react-native-developer, ios-developer, android-developer, embedded-engineer
- **AI/ML Depth**: llm-application-developer, prompt-engineer, mlops-engineer, computer-vision-engineer

### team-templates

Must add the 5 new templates (8-12) to the template list.

---

## Context Budget Verification

| Metric | v1.0 (12 agents) | v1.1 (20 agents) | Budget |
|--------|-------------------|-------------------|--------|
| Total description chars | ~3,903 | ~6,500 (est.) | Must stay well under 2% of context window |
| Total system prompt chars | ~39,000 | ~65,000 (est.) | Loaded on-demand per agent, not all at once |

The description field for each new agent should be approximately 300-350 characters (matching existing agents), keeping the total roster description under 7,000 characters. System prompts are loaded only when an agent is spawned, so their length does not impact the context budget of the pool itself.

---

## MVP Definition (v1.1.0)

### Must Ship

- [ ] All 8 agent markdown files with frontmatter and three-section system prompts
- [ ] 3 `<example>` blocks per agent description for delegation matching
- [ ] Correct tool tiers and permission modes per approved design
- [ ] 5 new team templates added to team-templates skill
- [ ] assemble-team roster table updated with 20 agents
- [ ] browse-pool updated with new agent categories
- [ ] CLAUDE.md roster table updated
- [ ] Context budget verified under 2% for descriptions

### Should Ship

- [ ] README.md updated with new agent descriptions
- [ ] CHANGELOG.md entry for v1.1.0

### Defer

- [ ] New supporting skills for AI/ML agents (e.g., "rag-patterns" skill)
- [ ] Additional team templates beyond the 5 planned
- [ ] Cross-agent collaboration guidelines document

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| react-native-developer agent | HIGH | MEDIUM | P1 |
| ios-developer agent | HIGH | MEDIUM | P1 |
| android-developer agent | HIGH | MEDIUM | P1 |
| embedded-engineer agent | MEDIUM | MEDIUM | P1 |
| llm-application-developer agent | HIGH | MEDIUM | P1 |
| prompt-engineer agent | HIGH | LOW | P1 |
| mlops-engineer agent | MEDIUM | MEDIUM | P1 |
| computer-vision-engineer agent | MEDIUM | MEDIUM | P1 |
| 5 new team templates | HIGH | LOW | P1 |
| assemble-team roster update | HIGH | LOW | P1 |
| browse-pool update | MEDIUM | LOW | P1 |
| CLAUDE.md roster table update | MEDIUM | LOW | P1 |
| Context budget verification | HIGH | LOW | P1 |
| README.md update | MEDIUM | LOW | P2 |
| CHANGELOG.md v1.1.0 entry | MEDIUM | LOW | P2 |

**Priority key:**
- P1: Must have for v1.1.0 release
- P2: Should have, add alongside or immediately after

---

## Sources

- [React Native New Architecture - Expo Documentation](https://docs.expo.dev/guides/new-architecture/) -- HIGH confidence (official Expo docs)
- [Expo SDK 52 Changelog](https://expo.dev/changelog/2024-11-12-sdk-52) -- HIGH confidence (official Expo release notes)
- [Android Jetpack Compose - Android Developers](https://developer.android.com/compose) -- HIGH confidence (official Google docs)
- [Kotlin for Jetpack Compose](https://developer.android.com/develop/ui/compose/kotlin) -- HIGH confidence (official Google docs)
- [Zephyr RTOS vs FreeRTOS Comparison](https://www.ezurio.com/resources/blog/zephyr-rtos-vs-freertos-a-comprehensive-comparison-for-iot-and-embedded-systems) -- MEDIUM confidence (vendor blog, verified by multiple sources)
- [LangChain vs LlamaIndex vs LangGraph RAG Framework Comparison](https://research.aimultiple.com/rag-frameworks/) -- MEDIUM confidence (research aggregator)
- [IBM Prompt Engineering Guide 2026](https://www.ibm.com/think/prompt-engineering) -- HIGH confidence (IBM official)
- [Promptfoo Red Team Documentation](https://www.promptfoo.dev/docs/red-team/) -- HIGH confidence (official tool docs)
- [MLOps/LLMOps Roadmap 2026](https://medium.com/@sanjeebmeister/the-complete-mlops-llmops-roadmap-for-2026-building-production-grade-ai-systems-bdcca5ed2771) -- MEDIUM confidence (practitioner article, verified against multiple sources)
- [MLflow Model Registry](https://lakefs.io/blog/mlflow-model-registry/) -- MEDIUM confidence (verified against MLflow official docs)
- [OpenCV Computer Vision Engineer Roadmap](https://opencv.org/blog/computer-vision-engineer-roadmap/) -- HIGH confidence (official OpenCV)
- [SwiftData vs Core Data 2025](https://distantjob.com/blog/core-data-vs-swiftdata/) -- MEDIUM confidence (practitioner comparison)
- [Kotlin Multiplatform vs React Native](https://kotlinlang.org/docs/multiplatform/kotlin-multiplatform-react-native.html) -- HIGH confidence (official Kotlin docs)
- [The Ultimate Android Developer Roadmap 2026](https://tiwariashuism.medium.com/the-ultimate-android-developer-roadmap-2026-from-novice-to-expert-afd14fc97d1b) -- MEDIUM confidence (practitioner roadmap)
- [iOS Developer Skills 2025](https://www.tealhq.com/skills/ios-developer) -- MEDIUM confidence (skills aggregator)
- [Embedded Systems Skills 2025](https://embeddedjobs.online/10-most-in-demand-skills-for-embedded-developers-in-2025/) -- MEDIUM confidence (industry survey)

---
*Feature research for: Agent Pool v1.1.0 Expansion (8 new specialist agents)*
*Researched: 2026-02-20*
