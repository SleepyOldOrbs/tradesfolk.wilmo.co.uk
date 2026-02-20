# Technology Stack: 8 New Specialist Agents

**Project:** Agent Pool v1.1.0 Expansion
**Researched:** 2026-02-20
**Scope:** Technology stacks for react-native-developer, ios-developer, android-developer, embedded-engineer, llm-application-developer, prompt-engineer, mlops-engineer, computer-vision-engineer
**Overall Confidence:** HIGH (multiple authoritative sources cross-referenced per domain)

This document defines the specific technologies, frameworks, libraries, and tools each new agent must know deeply. These feed directly into the "Core expertise" section of each agent's system prompt.

---

## 1. react-native-developer (Agent #13)

**Colour:** Blue | **Tier:** Implementation | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| React Native | 0.78+ (current: 0.82 in development) | Cross-platform mobile framework | 0.78 brought React 19 support and React Compiler. New Architecture is mandatory from 0.82 onward -- the legacy architecture was frozen June 2025. Agent must write New Architecture code by default. |
| Expo SDK | 53 (current stable) | Managed workflow, build services, OTA updates | SDK 53 ships React Native 0.79, React 19, 74.6% of SDK 52 projects already use New Architecture. Expo is the recommended way to build React Native apps -- even React Native's own docs recommend it. |
| React | 19 | UI library | Full React 19 support landed in React Native 0.78. Agent must know `use()`, `useOptimistic`, `useFormStatus`, `useActionState`, and the React Compiler. |
| TypeScript | 5.x | Type safety | Standard for all modern React Native projects. Expo templates ship with TypeScript by default. |

### Navigation & Routing

| Technology | Purpose | Why |
|------------|---------|-----|
| Expo Router | File-based routing | The standard for Expo projects. Built on React Navigation but provides file-system routing (like Next.js for mobile). Deep linking, typed routes, shared layouts out of the box. |
| React Navigation 7 | Stack/tab/drawer navigation | Underlying navigation library. Still needed for advanced patterns (custom navigators, nested stacks). Expo Router wraps this. |

### State & Data

| Technology | Purpose | Why |
|------------|---------|-----|
| TanStack Query | Server state management | Same pattern as web React. Handles caching, revalidation, offline support. |
| Zustand | Client state | Lightweight, no boilerplate. Works identically in React Native and web. |
| MMKV | Fast key-value storage | 30x faster than AsyncStorage. C++ JSI bridge. The standard for local storage in React Native. |
| WatermelonDB or Expo SQLite | Local database | WatermelonDB for offline-first apps with sync. Expo SQLite for simpler local queries. |

### Build & Deploy

| Technology | Purpose | Why |
|------------|---------|-----|
| EAS Build | Cloud builds for iOS/Android | Eliminates local Xcode/Android Studio build dependency. Handles signing, provisioning profiles. |
| EAS Submit | App store submission | Automated submission to App Store and Play Store. |
| EAS Update | Over-the-air JS updates | Push JS bundle updates without app store review. Critical for rapid iteration. Cannot update native code. |

### Testing

| Technology | Purpose | Why |
|------------|---------|-----|
| Jest + React Native Testing Library | Unit and component tests | Standard testing stack. RNTL mirrors React Testing Library patterns (user-centric queries). |
| Maestro | E2E testing | Recommended by Expo. YAML-based, no app modifications needed, automatic retries for stability. Replaced Detox as the default E2E tool. |

### Native Modules & Platform APIs

| Technology | Purpose | Why |
|------------|---------|-----|
| Expo Modules API | Custom native modules | TypeScript-first API for writing native modules. Replaces the old native module bridge pattern. |
| expo-camera, expo-location, expo-notifications | Platform capabilities | First-party Expo modules for device APIs. Maintained, tested, New Architecture compatible. |

### Integration with Existing Agents

- **react-specialist (02):** Shares React 19 knowledge. react-native-developer handles mobile-specific concerns (navigation, device APIs, app store builds). react-specialist handles web-specific patterns (SSR, hydration, Next.js).
- **ux-designer (03):** Collaborates on mobile UI. react-native-developer implements; ux-designer reviews accessibility, gesture patterns, platform conventions.
- **qa-tester (08):** qa-tester handles test strategy; react-native-developer writes Maestro flows and RNTL tests.

---

## 2. ios-developer (Agent #14)

**Colour:** Blue | **Tier:** Implementation | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| Swift | 6.2 (released September 2025) | Primary language | Swift 6.2 brings simplified concurrency (main actor isolation by default), compile-time macros, and the Observations async sequence. Agent must write Swift 6-safe concurrent code. |
| SwiftUI | Framework (ships with Xcode 17) | Declarative UI | Apple's primary UI framework. Now mature enough for production. Liquid Glass design language (iOS 26). Spatial layout support for visionOS. |
| Xcode | 17 (current beta) | IDE and build system | Live previews that behave like the real app. Agentic coding features. Required for App Store submission. |
| iOS | 17+ deployment target (current: iOS 26) | Target platform | iOS 15.1 is the minimum for React Native 0.76+, but for native Swift apps, targeting iOS 17+ gives access to SwiftData and Observation framework. |

### Data & Persistence

| Technology | Purpose | Why |
|------------|---------|-----|
| SwiftData | Data persistence (new projects) | Apple's modern replacement for Core Data. Pure Swift, no NSManagedObject, integrates with Observation framework. Use for all new projects targeting iOS 17+. |
| Core Data | Data persistence (legacy/complex) | Still more mature for complex scenarios (multi-writer, large datasets, custom migration). Agent should know both but default to SwiftData. |
| Keychain Services | Secure storage | For credentials, tokens, sensitive data. No alternative for secure storage on iOS. |

### Concurrency & Reactivity

| Technology | Purpose | Why |
|------------|---------|-----|
| Swift Concurrency (async/await, actors) | Asynchronous programming | The modern standard. Swift 6.2 makes it default with main actor isolation. TaskGroup for structured concurrency. |
| Observation framework (`@Observable`) | State observation | Replaces Combine's `ObservableObject` for SwiftUI. Lighter weight, works with async sequences in Swift 6.2. |
| Combine | Reactive streams (legacy/specific) | Use only for ongoing event streams (search-as-you-type, form validation). async/await replaces Combine for request/response patterns. Not deprecated but not the default choice for new code. |

### Networking & APIs

| Technology | Purpose | Why |
|------------|---------|-----|
| URLSession with async/await | HTTP networking | Built-in, no dependencies. async/await makes it clean. Use for most networking. |
| Alamofire | Advanced HTTP (optional) | Only when URLSession is insufficient (complex retry logic, request adaptation, response validation chains). Most projects don't need it. |
| Swift Protobuf / gRPC Swift | Binary protocols | For services using Protocol Buffers. Apple maintains the Swift gRPC implementation. |

### Testing

| Technology | Purpose | Why |
|------------|---------|-----|
| Swift Testing | Unit and integration tests | Apple's modern testing framework (WWDC 2024). Macro-based, parameterized tests, parallel execution by default. Replaces XCTest for new test code. |
| XCTest | UI tests, legacy tests | Still required for UI testing (XCUITest). Can coexist with Swift Testing for incremental migration. |
| Xcode Previews | Visual testing | Live previews in Xcode 17 support interaction -- scroll, tap, animate. Use as rapid visual verification. |

### App Distribution

| Technology | Purpose | Why |
|------------|---------|-----|
| TestFlight | Beta distribution | Apple's official beta testing platform. Supports internal and external testers. |
| App Store Connect API | Automated submission | For CI/CD pipeline integration. Fastlane wraps this but the raw API is available. |
| Fastlane | Build automation | De facto standard for iOS CI/CD. Handles signing, building, uploading, metadata. |

### Platform Capabilities

| Technology | Purpose | Why |
|------------|---------|-----|
| WidgetKit | Home screen and lock screen widgets | Timeline-based widgets with SwiftUI. |
| App Intents | Siri and Shortcuts integration | Modern replacement for SiriKit intents. Declarative, Swift-native. |
| ActivityKit | Live Activities and Dynamic Island | Real-time updates on lock screen. |
| visionOS / RealityKit | Spatial computing | For apps targeting Apple Vision Pro. SwiftUI spatial layout support. |

### Integration with Existing Agents

- **react-native-developer (13):** Distinct domains. ios-developer handles native Swift/SwiftUI work. react-native-developer handles cross-platform. They collaborate in the "Native iOS + Android" team template when native modules are needed.
- **security-auditor (09):** Reviews Keychain usage, App Transport Security, data protection classes.
- **ux-designer (03):** Ensures iOS Human Interface Guidelines compliance.

---

## 3. android-developer (Agent #15)

**Colour:** Green | **Tier:** Implementation | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| Kotlin | 2.3.0 (released December 2025) | Primary language | Latest stable. K2 compiler enabled by default, unused return value checker, explicit backing field syntax. ProGuard mappings for Compose stack traces with R8. |
| Jetpack Compose | 1.10.1 (January 2026) | Declarative UI | Android's modern UI toolkit. Material 3 1.4 support. Compose Compiler Gradle plugin (no manual Kotlin compatibility checks with Kotlin 2.0+). |
| Android Studio | Ladybug / latest stable | IDE | First-class Compose tooling, live previews, layout inspector for Compose. |
| Gradle | 8.x with Kotlin DSL | Build system | `build.gradle.kts` is the standard. Version Catalogs (`libs.versions.toml`) for dependency management. |

### Architecture & DI

| Technology | Purpose | Why |
|------------|---------|-----|
| Hilt (Dagger) | Dependency injection (Android-only) | Google's recommended DI for Android. Built on Dagger, integrates with ViewModels, Navigation, WorkManager. Use for pure Android projects. |
| Koin 4 | Dependency injection (multiplatform) | Use instead of Hilt when targeting Kotlin Multiplatform. Lightweight, no code generation, KMP-compatible. |
| Architecture Components (ViewModel, Lifecycle) | MVVM architecture | Google's official architecture guidance. ViewModels survive configuration changes. |

### Networking & Data

| Technology | Purpose | Why |
|------------|---------|-----|
| Retrofit + OkHttp | HTTP networking (Android-only) | De facto standard for Android REST APIs. Type-safe, interceptors, logging. Not KMP-compatible (Java dependency). |
| Ktor Client | HTTP networking (multiplatform) | Use when targeting Kotlin Multiplatform. Coroutine-native, platform-agnostic. |
| Room | Local database | Google's SQLite abstraction. KSP for annotation processing (replacing kapt). Supports Kotlin Multiplatform as of Room 2.8.3. |
| DataStore | Key-value and typed storage | Replaces SharedPreferences. Proto DataStore for typed data, Preferences DataStore for key-value. KMP-compatible. |

### Navigation

| Technology | Purpose | Why |
|------------|---------|-----|
| Navigation Compose | In-app navigation | Type-safe navigation with Compose. Supports deep links, nested graphs, animated transitions. |
| Compose Multiplatform Navigation | Cross-platform navigation | For KMP projects sharing UI across Android/iOS/Desktop. |

### Testing

| Technology | Purpose | Why |
|------------|---------|-----|
| JUnit 5 + Compose UI Test | Unit and UI tests | JUnit 5 for unit tests. Compose testing APIs for UI assertion/interaction. |
| Robolectric | Local Android tests | Runs Android framework tests on JVM without emulator. Fast feedback loop. |
| Espresso | Instrumented UI tests | For complex UI interactions on real devices/emulators. Slower but more accurate than Robolectric. |
| Maestro | E2E testing | Cross-platform E2E. Same tool as React Native -- YAML-based, stable. |

### Platform APIs

| Technology | Purpose | Why |
|------------|---------|-----|
| WorkManager | Background work | Guaranteed execution of deferrable background tasks. Handles constraints (network, battery). |
| CameraX | Camera access | Jetpack camera API. Simpler than Camera2, lifecycle-aware. |
| Material 3 | Design system | Google's current design language. Compose-native, dynamic color (Material You). |

### Kotlin Multiplatform (KMP)

| Technology | Purpose | Why |
|------------|---------|-----|
| Compose Multiplatform | Shared UI across platforms | JetBrains framework. iOS support reached stable in 2025 (version 1.8.0+). Shares Compose UI code between Android, iOS, Desktop, Web. |
| KMP shared modules | Shared business logic | Share networking, data models, business logic across platforms. UI can be native or shared via Compose Multiplatform. |

### Integration with Existing Agents

- **ios-developer (14):** Companion in "Native iOS + Android" team template. Parallel platform expertise.
- **react-native-developer (13):** Complementary. android-developer handles native Kotlin work; react-native-developer handles cross-platform.
- **database-specialist (07):** Collaborates on Room schema design, migration strategies.
- **backend-architect (05):** Reviews API contracts, offline-first architecture patterns.

---

## 4. embedded-engineer (Agent #16)

**Colour:** Cyan | **Tier:** Full access | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| C | C17/C23 | Primary firmware language | Dominant language for microcontrollers. C23 brings `typeof`, `nullptr`, `constexpr`, `static_assert` without message. MISRA C:2023 for safety-critical code. |
| C++ | C++17/C++20 (embedded subset) | Higher-level firmware | Used where OOP patterns help (HAL abstractions, state machines). Avoid exceptions, RTTI, dynamic allocation in constrained environments. |
| Rust (embedded) | Stable | Memory-safe firmware | Growing adoption for new embedded projects. `no_std` support, ownership prevents memory bugs. Embassy framework for async embedded Rust. |

### RTOS & Operating Systems

| Technology | Purpose | Why |
|------------|---------|-----|
| FreeRTOS | Traditional RTOS | Most widely used RTOS globally. Lightweight preemptive scheduler. Default RTOS in ESP-IDF. Use for resource-constrained MCUs and when vendor SDK includes it. |
| Zephyr RTOS | Modern connected RTOS | Rapidly becoming the default for new connected MCU projects. Unified build system (CMake + devicetree + Kconfig), 900+ board support, multi-architecture (ARM, RISC-V, x86). v4.3 released November 2025. Use for IoT devices with multi-year product lifecycles. |
| Bare metal | No OS firmware | For extremely constrained devices or hard real-time requirements where RTOS overhead is unacceptable. |

### Hardware Platforms & SDKs

| Technology | Purpose | Why |
|------------|---------|-----|
| ESP-IDF | Espressif ESP32 development | Official SDK for ESP32 family. Includes FreeRTOS, WiFi/BLE stacks, OTA updates. v5.5.2 current. Dominant IoT prototyping platform. |
| STM32CubeIDE / STM32 HAL | ST Microelectronics MCUs | Covers STM32 family (Cortex-M0 to M7). HAL for portability, LL drivers for performance. Large industrial footprint. |
| nRF Connect SDK | Nordic Semiconductor (BLE/Thread) | Based on Zephyr. For BLE, Thread, Zigbee, LTE-M/NB-IoT devices. nRF52/nRF53/nRF54 series. |
| Arduino Core | Rapid prototyping | Quick hardware validation. Not for production firmware. Useful for proof-of-concept before moving to vendor SDK. |

### Build & Development Tools

| Technology | Purpose | Why |
|------------|---------|-----|
| CMake | Build system | Standard for Zephyr, ESP-IDF, and most modern embedded projects. Cross-compilation toolchain files. |
| PlatformIO | Multi-platform build tool | VS Code extension supporting 30+ frameworks (ESP-IDF, Zephyr, STM32, Arduino). Unified build/upload/debug across MCU families. |
| West | Zephyr meta-tool | Manages Zephyr workspace: fetch, build, flash, debug. Required for Zephyr projects. |
| GDB + OpenOCD / J-Link | Hardware debugging | JTAG/SWD debugging. OpenOCD is open-source; J-Link (Segger) for commercial. GDB for breakpoints, memory inspection, register views. |
| Devicetree | Hardware description | Zephyr uses devicetree for hardware abstraction. Agent must understand `.dts` / `.dtsi` / `.overlay` files. |

### Communication Protocols

| Technology | Purpose | Why |
|------------|---------|-----|
| MQTT | Cloud telemetry | Lightweight pub/sub over TCP. Dominant protocol for IoT cloud connectivity. QoS levels for reliability guarantees. |
| CoAP | Constrained device communication | UDP-based, REST-like. Lower overhead than MQTT. Use for very constrained networks or devices. |
| Bluetooth LE | Short-range wireless | Wearables, asset tags, smartphone-to-device. GATT profiles, mesh networking. |
| Matter | Smart home protocol | IP-based, cross-ecosystem (Apple, Google, Amazon). Built on Thread/WiFi. Growing standard for home automation. |
| I2C, SPI, UART | On-board peripherals | Fundamental bus protocols for sensor/actuator communication. Agent must know timing, pull-ups, clock speeds. |
| CAN | Automotive/industrial | Controller Area Network for vehicles and industrial systems. CAN FD for higher bandwidth. |

### Testing & Quality

| Technology | Purpose | Why |
|------------|---------|-----|
| Unity (C test framework) | Unit testing | Lightweight C test framework for embedded. Runs on target or host. |
| Ceedling | Build/test automation for C | Wraps Unity + CMock for C projects. Test runner with mocking support. |
| QEMU | Hardware emulation | Test firmware without physical hardware. Zephyr has excellent QEMU support for CI. |
| Static analysis (cppcheck, PC-lint) | Code quality | MISRA compliance checking. Essential for safety-critical firmware. |

### Integration with Existing Agents

- **systems-programmer (06):** Shares C/C++/Rust expertise. embedded-engineer focuses on MCU-constrained environments; systems-programmer handles desktop/server systems programming.
- **devops-engineer (10):** Collaborates on firmware CI/CD pipelines, OTA update infrastructure.
- **security-auditor (09):** Reviews secure boot, firmware signing, key storage on hardware.

---

## 5. llm-application-developer (Agent #17)

**Colour:** Magenta | **Tier:** Implementation | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| Python | 3.12+ | Primary language | LLM ecosystem is Python-first. Type hints, async support, match statements. |
| TypeScript | 5.x | Alternative/frontend | LangChain.js, Vercel AI SDK. Use when building full-stack LLM apps with Next.js. |
| LangChain | Latest stable | LLM orchestration | Modular chains, tool integration, memory, output parsers. The standard orchestration layer for multi-step LLM workflows. |
| LangGraph | Latest stable | Agent orchestration | DAG-based multi-agent workflows. Recommended by LangChain for all new agent implementations. Supports conditional branching, parallel execution, persistent state. Supervisor and Swarm patterns built in. |
| LlamaIndex | Latest stable | Data indexing and retrieval | Data-first framework for RAG. 35% retrieval accuracy improvement in 2025. Superior document indexing, flexible connectors. Use alongside LangChain (not instead of). |

### RAG (Retrieval-Augmented Generation)

| Technology | Purpose | Why |
|------------|---------|-----|
| pgvector | Vector storage (Postgres teams) | Add vector capabilities to existing PostgreSQL. No new infrastructure. Use when the team already runs Postgres. |
| ChromaDB | Vector storage (prototyping) | Embedded, zero-config. Fastest path to working prototype. Rust rewrite (2025) delivers 4x performance improvement. |
| Qdrant | Vector storage (production, filtered search) | Rust-based, consistently low latency. Best-in-class filtered vector search (similarity + metadata constraints). |
| Pinecone | Vector storage (managed, scale) | Fully managed, serverless. Minimal ops. Use when team wants zero infrastructure management. |

### LLM APIs & Providers

| Technology | Purpose | Why |
|------------|---------|-----|
| Anthropic Claude API | Primary LLM provider | Tool use, long context, structured output. MCP integration. Agent must know the Messages API, tool_use blocks, prompt caching. |
| OpenAI API | Alternative LLM provider | GPT-4o, function calling, structured outputs, batch API. Industry standard. |
| Hugging Face Inference API | Open-source models | Access to thousands of models. Use for specialized tasks (embeddings, classification, small models). |
| Ollama | Local model serving | Run open-source LLMs locally. Development and testing without API costs. |

### Agent & Tool Frameworks

| Technology | Purpose | Why |
|------------|---------|-----|
| Model Context Protocol (MCP) | Tool integration standard | Open standard (Anthropic, now Linux Foundation). 97M+ monthly SDK downloads. 75+ official connectors. Agent must understand MCP server/client patterns. |
| Anthropic Tool Use | Native tool calling | Claude's built-in tool use with structured JSON schemas. Prefer over LangChain tool abstraction when targeting Claude specifically. |
| Vercel AI SDK | Full-stack AI (TypeScript) | Streaming, tool calling, generative UI. Use for Next.js + LLM applications. |

### Evaluation & Observability

| Technology | Purpose | Why |
|------------|---------|-----|
| LangSmith | Tracing and evaluation | LangChain's observability platform. Agent-specific metrics, tool calling traces, trajectory tracking. |
| Promptfoo | Prompt evaluation and red-teaming | Open-source. Compare model outputs, run security tests, CI/CD integration. |
| Braintrust | Evaluation platform | Logging, scoring, dataset management for LLM applications. |

### Supporting Libraries

| Technology | Purpose | Why |
|------------|---------|-----|
| Pydantic | Structured output parsing | Define output schemas. LangChain and direct API calls both use Pydantic models for structured outputs. |
| tiktoken / anthropic-tokenizer | Token counting | Estimate costs, manage context windows, chunk documents appropriately. |
| Unstructured | Document parsing | Extract text from PDFs, DOCX, HTML for RAG pipelines. Handles complex layouts. |
| FastAPI | API serving | Serve LLM-powered features as APIs. Async, Pydantic validation, OpenAPI docs. |

### Integration with Existing Agents

- **python-developer (04):** Shares Python expertise. llm-application-developer focuses on LLM-specific patterns (RAG, agents, prompts); python-developer handles general Python/API work.
- **prompt-engineer (18):** Collaborates closely. llm-application-developer builds the pipeline; prompt-engineer designs and optimises the prompts within it.
- **data-scientist (11):** Collaborates on evaluation metrics, fine-tuning data preparation.
- **database-specialist (07):** Advises on vector index configuration, hybrid search schemas.

---

## 6. prompt-engineer (Agent #18)

**Colour:** Magenta | **Tier:** Documentation | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| DSPy | Latest stable | Programmatic prompt optimisation | Stanford's framework for programming (not prompting) LLMs. Compiles and optimises prompts from validation data. MIPROv2 and BetterTogether optimisers. Replaces manual trial-and-error with mathematical optimisation. |
| Promptfoo | Latest stable | Prompt evaluation and testing | Open-source. Declarative YAML configs for testing prompts against models. Built-in red-teaming and security testing. CI/CD integration. |
| Anthropic Claude API | Latest | Primary LLM for prompt development | Must know prompt caching, system prompts, tool_use, XML tag conventions, chain-of-thought elicitation patterns specific to Claude. |

### Evaluation & Testing

| Technology | Purpose | Why |
|------------|---------|-----|
| LLM-as-Judge | Automated evaluation | Using models (Claude, GPT-4o) to score outputs at scale. Moved from experimental to essential in 2025. Agent must design judge prompts and rubrics. |
| Promptfoo red-teaming | Security testing | Adversarial prompt testing. Jailbreak detection, prompt injection resistance, PII leakage checks. |
| Custom evaluation scripts (Python) | Deterministic metrics | BLEU, ROUGE, exact match, regex validation. For cases where LLM-as-judge is insufficient. |
| Opik | Open-source evaluation platform | Integrates with LangChain, LlamaIndex, OpenAI. Evaluation, testing, monitoring for LLM applications. |

### Prompt Design Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| System prompt architecture | Set model behaviour and constraints | Every LLM application. Agent must know XML tag structuring, role definition, constraint specification. |
| Few-shot examples | Guide output format and quality | When zero-shot quality is insufficient. Agent designs example selection strategies. |
| Chain-of-thought (CoT) | Improve reasoning accuracy | Complex reasoning tasks. Agent knows when CoT helps vs. hurts (simple tasks don't benefit). |
| Output structuring (JSON mode, tool_use) | Reliable structured output | When downstream code parses LLM output. Prefer tool_use over JSON-in-text for Claude. |
| Constitutional AI / self-critique | Safety and quality guardrails | Red-teaming, output filtering, self-correction chains. |

### Supporting Tools

| Technology | Purpose | Why |
|------------|---------|-----|
| Anthropic Workbench | Interactive prompt development | Browser-based prompt testing with Claude. Variable substitution, comparison mode. |
| LangSmith Prompt Hub | Prompt versioning and sharing | Version-controlled prompts with deployment tracking. |
| Weights & Biases Prompts | Prompt tracking and evaluation | Track prompt iterations alongside model experiments. |

### Integration with Existing Agents

- **llm-application-developer (17):** Primary collaborator. prompt-engineer designs prompts; llm-application-developer integrates them into pipelines. prompt-engineer focuses on prompt quality, not infrastructure.
- **technical-writer (12):** Shares documentation skills. prompt-engineer writes system prompts and evaluation criteria; technical-writer writes user-facing docs.
- **qa-tester (08):** Collaborates on evaluation strategies. prompt-engineer designs test cases for LLM outputs.

---

## 7. mlops-engineer (Agent #19)

**Colour:** Cyan | **Tier:** Full access | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| MLflow | 3.x (latest) | Experiment tracking, model registry, LLM ops | Most widely adopted open-source MLOps platform. v3 adds native LLM support: prompt engineering, agent tracing, GenAI evaluation. Use as the experiment tracking backbone. |
| Kubeflow | Latest stable | ML pipeline orchestration on Kubernetes | Preferred for platform teams with Kubernetes expertise. Scalable training, serving, and orchestration. Pipelines SDK for defining DAGs. |
| Python | 3.12+ | Primary language | MLOps ecosystem is Python-first. |

### Experiment Tracking & Model Management

| Technology | Purpose | Why |
|------------|---------|-----|
| MLflow Tracking | Log experiments, parameters, metrics | Open-source, self-hostable, integrates with all major ML frameworks. |
| Weights & Biases (W&B) | Experiment tracking (managed) | Leading managed platform. 200,000+ ML practitioners. Used by OpenAI, Toyota, Samsung. Use when team prefers managed service over self-hosted MLflow. |
| DVC (Data Version Control) | Data and model versioning | Git-like versioning for datasets and models. Tracks data without storing it in Git. Use alongside MLflow. |
| Hydra | Configuration management | Composable configs for experiments. Override parameters from command line. Standard for PyTorch training scripts. |

### Model Serving & Inference

| Technology | Purpose | Why |
|------------|---------|-----|
| vLLM | LLM inference engine | Best-in-class time to first token (TTFT). Continuous batching, speculative decoding, PagedAttention. The standard for serving large language models. |
| BentoML | Model packaging and serving | Developer-friendly packaging layer. Decouples ML workflow from infrastructure. Integrates with vLLM, MLflow, Triton. |
| KServe | Kubernetes-native model serving | Standardised serverless inference on Kubernetes. Canary rollouts, autoscaling, multi-framework support. Use on Kubernetes clusters. |
| TGI (Text Generation Inference) | Hugging Face model serving | Up to 13x faster than vLLM on long prompts with prefix caching. Use for Hugging Face model deployments. |
| Triton Inference Server | Multi-framework GPU inference | NVIDIA's inference server. Supports PyTorch, TensorFlow, ONNX, TensorRT. Use for GPU-heavy, multi-model serving. |
| Ray Serve | Distributed serving | Scalable serving framework. Handles model composition, batching, multi-model pipelines. Part of Ray ecosystem. |

### Pipeline Orchestration

| Technology | Purpose | Why |
|------------|---------|-----|
| Kubeflow Pipelines | ML workflow DAGs | Define training/evaluation/deployment pipelines as code. Kubernetes-native. |
| Apache Airflow | General workflow orchestration | When ML pipelines are part of larger data workflows. Mature, well-understood. |
| Prefect | Modern workflow orchestration | Python-native, easier than Airflow for ML teams. Handles retries, scheduling, observability. |
| ZenML | MLOps framework | Connects MLflow, Kubeflow, cloud providers into a unified pipeline. Abstracts infrastructure choices. |

### Infrastructure

| Technology | Purpose | Why |
|------------|---------|-----|
| Docker | Containerisation | Standard for reproducible ML environments. GPU support via NVIDIA Container Toolkit. |
| Kubernetes | Container orchestration | Production ML workloads. GPU scheduling, autoscaling, multi-tenancy. |
| Terraform / Pulumi | Infrastructure as code | Provision GPU instances, storage, networking. Terraform for established teams; Pulumi for Python-native IaC. |
| AWS SageMaker / GCP Vertex AI / Azure ML | Managed ML platforms | When teams prefer managed over self-hosted. Each cloud has its own training/serving/registry stack. |

### Monitoring & Observability

| Technology | Purpose | Why |
|------------|---------|-----|
| Evidently AI | Data and model monitoring | Detect data drift, prediction drift, data quality issues. Open-source. |
| Great Expectations | Data validation | Define expectations for data quality. Catches data issues before they reach models. |
| Prometheus + Grafana | Infrastructure monitoring | Standard for Kubernetes monitoring. Custom metrics for model latency, throughput, GPU utilisation. |
| Arize AI | ML observability (managed) | Production model monitoring, embedding drift detection, LLM tracing. |

### Integration with Existing Agents

- **data-scientist (11):** Primary collaborator. data-scientist trains models; mlops-engineer deploys and monitors them. data-scientist owns experiment design; mlops-engineer owns the infrastructure that runs experiments.
- **devops-engineer (10):** Shares Kubernetes, Docker, CI/CD expertise. mlops-engineer focuses on ML-specific infrastructure (GPU scheduling, model serving); devops-engineer handles general infrastructure.
- **python-developer (04):** Collaborates on API endpoints that serve predictions. python-developer builds the web API; mlops-engineer ensures the model behind it scales.

---

## 8. computer-vision-engineer (Agent #20)

**Colour:** Magenta | **Tier:** Implementation | **Permission:** default

### Core Technologies

| Technology | Version | Purpose | Why This Version |
|------------|---------|---------|------------------|
| Python | 3.12+ | Primary language | CV ecosystem is Python-first. |
| PyTorch | 2.x (latest stable) | Deep learning framework | Dominant framework for CV research and production. TorchScript and TorchServe for deployment. PyTorch Lightning for structured training. |
| OpenCV | 4.x stable (5.0 alpha available) | Image processing | Most widely used CV library. 4.x is production-ready. 5.0 alpha available but not production-ready (radical API revision, C API removal, revamped DNN engine). Agent should use 4.x and be aware of 5.0 changes. |
| torchvision | Matches PyTorch version | CV-specific PyTorch utilities | Pretrained models, transforms, datasets, training utilities. Tightly integrated with PyTorch. |

### Object Detection & Segmentation

| Technology | Purpose | Why |
|------------|---------|-----|
| YOLO (Ultralytics) | Real-time object detection | YOLO26 (September 2025) is the latest. Removes NMS and DFL bottlenecks. YOLO11 and YOLOv8 are also widely deployed. Ultralytics provides unified Python API across versions. |
| Detectron2 | Object detection and segmentation | Meta's library. Mask R-CNN, Panoptic FPN. Use for instance/panoptic segmentation tasks. |
| SAM 2 (Segment Anything Model 2) | Zero-shot segmentation | Meta's foundation model for segmentation. Segment anything with prompts (points, boxes, text). |
| MMDetection / MMSegmentation | Detection/segmentation toolbox | OpenMMLab suite. Wide model zoo, modular design. Use when Detectron2 or YOLO don't cover the architecture needed. |

### Generative & Multimodal Vision

| Technology | Purpose | Why |
|------------|---------|-----|
| Hugging Face Diffusers | Diffusion models | State-of-the-art image/video generation. Stable Diffusion, SDXL, Flux, SANA-Sprint. Use for image generation, inpainting, super-resolution. |
| Hugging Face Transformers (vision) | Vision transformers | ViT, DINOv2, Swin Transformer, multimodal models (LLaVA, Florence). Use for classification, feature extraction, VLMs. |
| CLIP | Image-text alignment | OpenAI's contrastive learning model. Zero-shot image classification, image search, multimodal embeddings. |

### Image Processing & OCR

| Technology | Purpose | Why |
|------------|---------|-----|
| OpenCV | Classical image processing | Filtering, morphology, contour detection, colour space conversion, geometric transforms. Foundation for pre/post-processing pipelines. |
| Pillow (PIL) | Image I/O and basic processing | Loading, saving, resizing, format conversion. Lighter than OpenCV for simple operations. |
| Tesseract + pytesseract | OCR | Open-source OCR engine. Good for printed text. Use PaddleOCR or EasyOCR for multilingual/scene text. |
| PaddleOCR | Advanced OCR | Superior for scene text, multilingual text, rotated text. Lighter and faster than Tesseract for production. |

### Training & Optimization

| Technology | Purpose | Why |
|------------|---------|-----|
| PyTorch Lightning | Structured training | Removes boilerplate from training loops. Handles distributed training, mixed precision, logging. |
| Albumentations | Image augmentation | Fast, flexible augmentation library. 70+ transforms, pipeline composition. Standard for CV data augmentation. |
| ONNX Runtime | Model optimization and inference | Export PyTorch models to ONNX for cross-platform deployment. Quantization, graph optimization. |
| TensorRT | GPU inference optimization | NVIDIA's inference optimizer. INT8/FP16 quantization. Use for production GPU deployment. |

### Data & Annotation

| Technology | Purpose | Why |
|------------|---------|-----|
| Roboflow | Dataset management and annotation | Upload, annotate, augment, version datasets. Export to YOLO/COCO/VOC formats. Inference API for deployment. |
| Label Studio | Open-source annotation | Self-hosted annotation platform. Supports bounding boxes, polygons, keypoints, semantic segmentation. |
| COCO format | Dataset standard | Common Objects in Context. Standard annotation format for detection and segmentation. Agent must read/write COCO JSON. |
| FiftyOne | Dataset exploration and curation | Visualise, query, and curate CV datasets. Find label errors, duplicates, hard examples. |

### Deployment

| Technology | Purpose | Why |
|------------|---------|-----|
| TorchServe | PyTorch model serving | Official PyTorch serving solution. Model archiving, batching, metrics. |
| Triton Inference Server | Multi-model GPU serving | When serving multiple models on GPUs. Dynamic batching, model ensembles. |
| ONNX Runtime Web / TensorFlow.js | Browser inference | For edge/client-side CV. Run models in the browser. |
| Edge deployment (TFLite, CoreML, ONNX) | Mobile/edge inference | Export models for mobile devices. TFLite for Android, CoreML for iOS, ONNX for cross-platform. |

### Integration with Existing Agents

- **data-scientist (11):** Shares ML fundamentals. computer-vision-engineer specialises in vision tasks; data-scientist handles tabular data, statistics, and general ML.
- **mlops-engineer (19):** Deploys CV models to production. computer-vision-engineer trains and optimises; mlops-engineer handles serving infrastructure.
- **python-developer (04):** Builds API wrappers around CV models.
- **llm-application-developer (17):** Collaborates on multimodal applications (vision + language models, VLMs, image understanding pipelines).

---

## Cross-Agent Technology Overlaps

Understanding shared technologies helps the Team Lead delegate efficiently and avoid conflicting advice.

| Technology | Primary Agent | Secondary Agents | Boundary |
|------------|--------------|-------------------|----------|
| Python 3.12+ | python-developer | llm-application-developer, mlops-engineer, computer-vision-engineer, data-scientist | python-developer for general Python; others for domain-specific Python |
| React 19 | react-specialist | react-native-developer | react-specialist for web; react-native-developer for mobile |
| Kotlin | android-developer | (none) | Exclusive domain |
| Swift | ios-developer | (none) | Exclusive domain |
| C/C++ | embedded-engineer | systems-programmer | embedded-engineer for MCU/firmware; systems-programmer for desktop/server |
| Docker/Kubernetes | devops-engineer | mlops-engineer | devops-engineer for general infra; mlops-engineer for ML-specific (GPU scheduling, model serving) |
| PyTorch | data-scientist | computer-vision-engineer | data-scientist for general ML; computer-vision-engineer for vision models |
| LangChain/LangGraph | llm-application-developer | (none) | Exclusive domain |
| Prompt design | prompt-engineer | llm-application-developer | prompt-engineer for prompt quality/evaluation; llm-application-developer for pipeline integration |
| MLflow | mlops-engineer | data-scientist | mlops-engineer for infrastructure; data-scientist for experiment logging |
| Maestro (testing) | react-native-developer | android-developer | Both use Maestro for E2E; react-native-developer for cross-platform, android-developer for native |

## Model Assignment Recommendations

| Agent | Recommended `model:` | Rationale |
|-------|----------------------|-----------|
| react-native-developer | `inherit` | Implementation agent. Let user config decide. |
| ios-developer | `inherit` | Implementation agent. Needs full reasoning for Swift/SwiftUI patterns. |
| android-developer | `inherit` | Implementation agent. Needs full reasoning for Kotlin/Compose patterns. |
| embedded-engineer | `inherit` | Full access tier. Complex hardware/firmware reasoning benefits from capable models. |
| llm-application-developer | `inherit` | Implementation agent. Needs strong reasoning for agent orchestration patterns. |
| prompt-engineer | `sonnet` | Documentation tier. Writes prompts and evaluation criteria, not complex application code. Similar to ux-designer and technical-writer rationale. |
| mlops-engineer | `inherit` | Full access tier. Infrastructure complexity warrants capable model. |
| computer-vision-engineer | `inherit` | Implementation agent. Training pipelines and model architecture require strong reasoning. |

**Rationale:** Only prompt-engineer gets `sonnet` because it operates at the Documentation tier (same as ux-designer and technical-writer which already use `sonnet`). All other agents are Implementation or Full access tier and benefit from the user's configured model.

## Sources

- [React Native Releases Overview](https://reactnative.dev/docs/releases) -- RN 0.78, 0.82 New Architecture mandate (HIGH)
- [Expo SDK 52 Release](https://expo.dev/changelog/2024-11-12-sdk-52) -- SDK 52 features, New Architecture default (HIGH)
- [Expo SDK 53 Overview](https://medium.com/@onix_react/whats-new-in-expo-sdk-53-e1a8b338c19d) -- SDK 53 with RN 0.79, React 19 (MEDIUM)
- [Swift 6.2 Released](https://www.swift.org/blog/swift-6.2-released/) -- Concurrency improvements, Observations API (HIGH)
- [SwiftUI 2025 Updates](https://www.geeky-gadgets.com/apple-swiftui-2025-updates-overview/) -- Liquid Glass, spatial layout (MEDIUM)
- [Swift Testing vs XCTest](https://swiftprogramming.com/swift-testing-xctest/) -- Modern testing framework comparison (MEDIUM)
- [SwiftData vs Core Data 2025](https://medium.com/@hiren6997/swiftdata-vs-core-data-which-one-should-you-use-in-2025-f1bcaa6142f0) -- Data persistence guidance (MEDIUM)
- [Kotlin 2.3.0 Released](https://blog.jetbrains.com/kotlin/2025/12/kotlin-2-3-0-released/) -- K2 compiler, latest features (HIGH)
- [Jetpack Compose December 2025](https://android-developers.googleblog.com/2025/12/whats-new-in-jetpack-compose-december.html) -- Compose 1.10, Material 3 1.4 (HIGH)
- [Compose Multiplatform iOS Stable](https://www.kmpship.app/blog/compose-multiplatform-ios-stable-2025) -- KMP maturity (MEDIUM)
- [Zephyr RTOS embedded world 2026](https://embeddedcomputing.com/technology/open-source/linux-freertos-related/the-zephyr-project-grows-membership-highlights-security-and-resilience-at-embedded-world-2026) -- Zephyr growth, v4.3 (HIGH)
- [Best RTOS 2025](https://promwad.com/news/best-rtos-2025) -- FreeRTOS vs Zephyr comparison (MEDIUM)
- [PlatformIO Updates 2025](https://piolabs.com/blog/news/platformio-oss-august-2025-updates.html) -- ESP-IDF, Zephyr, STM32 support (MEDIUM)
- [LangGraph Multi-Agent Orchestration](https://www.langchain.com/langgraph) -- DAG-based agents, production recommendation (HIGH)
- [Top LLM Frameworks 2026](https://redwerk.com/blog/top-llm-frameworks/) -- LangChain, LlamaIndex, LangGraph ecosystem (MEDIUM)
- [Best Vector Databases 2026](https://www.firecrawl.dev/blog/best-vector-databases-2025) -- Pinecone, ChromaDB, Qdrant, pgvector comparison (MEDIUM)
- [DSPy Framework](https://dspy.ai/) -- Programmatic prompt optimisation (HIGH)
- [Promptfoo Red-Teaming](https://www.promptfoo.dev/blog/top-5-open-source-ai-red-teaming-tools-2025/) -- Open-source evaluation tools (MEDIUM)
- [MLOps Platforms 2026](https://addepto.com/mlops-platforms-in-2026/) -- MLflow 3, Kubeflow, W&B ecosystem (MEDIUM)
- [MLflow vs Kubeflow 2026](https://pub.towardsai.net/mlflow-vs-kubeflow-vs-airflow-choosing-the-right-mlops-tool-for-real-world-production-systems-ddcb863978f8) -- Hybrid architecture recommendation (MEDIUM)
- [vLLM and BentoML Integration](https://docs.bentoml.com/en/latest/examples/vllm.html) -- Inference backend comparison (MEDIUM)
- [Comparing Inference Runtimes 2025](https://www.marktechpost.com/2025/11/07/comparing-the-top-6-inference-runtimes-for-llm-serving-in-2025/) -- vLLM, TGI, TensorRT-LLM benchmarks (MEDIUM)
- [Computer Vision Models 2026](https://www.analyticsvidhya.com/blog/2025/03/computer-vision-models/) -- YOLO26, Detectron2, SAM 2 (MEDIUM)
- [YOLO Evolution Guide](https://blog.roboflow.com/guide-to-yolo-models/) -- YOLO26 architecture changes (MEDIUM)
- [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/index) -- Diffusion model framework (HIGH)
- [OpenCV 5.0 Roadmap](https://github.com/opencv/opencv/wiki/OE-5.-OpenCV-5) -- API revision, 5.0 alpha status (MEDIUM)
- [MCP - Model Context Protocol](https://modelcontextprotocol.io/) -- Open standard, SDK availability (HIGH)
- [W&B Migration from MLflow](https://medium.com/@pablop44/why-everyone-is-migrating-from-mlflow-to-weights-biases-w-b-in-2025-5926f978e03e) -- W&B adoption trends (LOW -- single source, marketing bias)

---
*Stack research for: Agent Pool v1.1.0 -- 8 new specialist agents*
*Researched: 2026-02-20*
