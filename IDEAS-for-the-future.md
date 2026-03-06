# Agent Pool — Future Agent Ideas

Non-development agents that leverage Claude Code's toolset (file I/O, Bash, web search, multimodal vision, MCP servers) for tasks beyond app building.

## Visual Media

| Agent | What it does | Tools / APIs |
|-------|-------------|--------------|
| **Diagram Author** | Mermaid, D2, PlantUML, SVG generation from descriptions | Pure file output, no API |
| **Image Director** | Prompt engineering for image generation, manages outputs and styles | Gemini Imagen, OpenAI DALL-E, HF Diffusion models |
| **Video Producer** | Remotion compositions, scene orchestration, rendering to MP4 | Remotion MCP + Bash |
| **Screenshot Analyst** | Reads screenshots/mockups, produces structured feedback or bug reports | Claude multimodal vision (Read tool) |
| **Asset Generator** | SVG icons, CSS illustrations, favicons, OG images as HTML/CSS | Pure file output |

The **Image Director** owns the model selection decision: Imagen for photorealism, DALL-E for illustration, SDXL for maximum control. Manages API costs, aspect ratios, and seed consistency across regenerations.

## Audio & TTS

| Agent | What it does | Tools / APIs |
|-------|-------------|--------------|
| **Voice Producer** | Calls TTS APIs, writes SSML markup, manages voice settings | ElevenLabs, OpenAI TTS, Piper (local) |
| **Audio Engineer** | Trim, concatenate, convert, normalize, add silence | ffmpeg via Bash (no API needed) |
| **Podcast Producer** | Multi-voice scripts with stage directions, orchestrates TTS + ffmpeg stitching | Combines Voice Producer + Audio Engineer |

The **Audio Engineer** is the easiest win — pure ffmpeg, no API keys, no cost, immediately useful.

## Pentesting & Offensive Security

| Agent | What it does | Tools |
|-------|-------------|-------|
| **Recon Specialist** | nmap, whois, DNS enumeration, subdomain discovery, OSINT | Bash (full access) |
| **Web App Pentester** | nikto, sqlmap, gobuster, OWASP ZAP CLI against authorised targets | Bash (full access) |
| **CTF Player** | Binary analysis, crypto puzzles, steganography, web exploitation | Bash (full access) |

Key distinction from the existing **security-auditor**: the auditor reads code passively with read-only tools. These agents actively *run* attacks against authorised infrastructure. Different tool tier, different permission model.

## Infrastructure & Ops

| Agent | What it does | Tools |
|-------|-------------|-------|
| **Sysadmin** | nginx configs, systemd units, log analysis, cron jobs, server troubleshooting | Bash (full access) |
| **Network Diagnostician** | DNS, firewall rules, SSL certs, connectivity debugging | Bash (full access) |
| **Incident Responder** | Structured postmortems, timeline reconstruction from logs, action items | Documentation tier |

The **Sysadmin** is immediately useful for anyone deploying things via Claude Code.

## Research & Analysis

| Agent | What it does | Tools |
|-------|-------------|-------|
| **Researcher** | Web search, source synthesis, literature reviews, competitive analysis | WebSearch, WebFetch |
| **Data Analyst** | CSV/JSON wrangling, pandas scripts, summary reports (no ML) | Bash, Write, NotebookEdit |

## Writing & Content

| Agent | What it does | Tools |
|-------|-------------|-------|
| **Copywriter** | Marketing copy, landing pages, email sequences, product descriptions | Documentation tier |
| **Translator / Localiser** | i18n JSON files, locale management, translation consistency checks | Implementation tier |

## Governance & Compliance

| Agent | What it does | Tools |
|-------|-------------|-------|
| **License Auditor** | Dependency scanning for GPL/AGPL conflicts, SBOM generation, license compatibility | Read-only tier |
| **Accessibility Auditor** | WCAG compliance beyond code — content structure, alt text, reading level | Read-only tier |

## Project & Process

| Agent | What it does | Tools |
|-------|-------------|-------|
| **Project Planner** | Breaking work into phases, writing specs, risk assessment, dependency mapping | Documentation tier |

## Priority Order

Build first (highest immediate value):
1. **Sysadmin** — practical for anyone deploying
2. **Audio Engineer** — pure ffmpeg, zero cost, no API keys
3. **Researcher** — WebSearch makes it a genuinely different capability
4. **Video Producer** — Remotion MCP already wired up
5. **Image Director** — HuggingFace MCP already available
6. **Web App Pentester** — unique contrast with existing security-auditor
