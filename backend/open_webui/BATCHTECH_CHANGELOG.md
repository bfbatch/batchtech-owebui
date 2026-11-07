# BatchTechUI Changelog

Changes made in BatchTechUI itself. Open WebUI's own release notes are at https://github.com/open-webui/open-webui/releases.

## [1.1.0] - 2026-11-07

### Added

- 🪙 **Token Saver filter.** Installed and on for every model the first time the server starts. It asks for terse replies, resends only the last 20 messages and shrinks old long messages and tool output, which cuts cloud model spend. Tune or turn it off in Admin Panel > Functions > Token Saver (gear icon).

## [1.0.0] - 2026-11-05

### Added

- 🏷️ **BatchTechUI branding.** The name, BT logo and icons replace Open WebUI throughout the interface, and a script re-applies them after every upstream update.
- 🔢 **BatchTechUI version.** Settings > About and Admin Settings > General show the BatchTechUI version, with the Open WebUI version it is based on and, when built with one, the commit.
- 🌀 **Working-model logo.** The logo of the model that is working spins and pulses while it works.
- 💭 **Rotating thinking words.** While any model is working, the label cycles through a word list you can edit in Settings, and Settings search finds "Thinking words". It stays visible between tool calls and hides while an ask_user question is waiting for your answer.
- 💬 **Chat and Code modes.** A claude.ai-style header and greeting, with a Mode switch for chat or code work.
- 📊 **Server status panel.** A sidebar panel showing CPU, memory and the models loaded, with every metric labelled and coloured by load.
- 🤝 **Handoff chip.** Shows which model is doing the work when a cloud model hands a task to a local one.
- 🔄 **Weekly upstream sync.** A GitHub workflow merges each new Open WebUI release, re-applies the branding and opens a pull request. Nothing is deployed automatically.

- 🖼️ **Custom logos.** `batchtech/apply_assets.py` accepts `--main-logo` and `--model-logo` (a file or a URL), and the installer asks for the app name, main logo and model logo before installing. Linux gets the full install; Mac and Windows get preview installers for the chat stack.
- 🌐 **Remote access.** WebSocket support is off by default (`ENABLE_WEBSOCKET_SUPPORT=false`) so the app works through a Cloudflare tunnel. Live updates use polling.

### Changed

- 📝 **What's new.** Opens these BatchTechUI release notes in a popup, and again after each BatchTechUI release, instead of Open WebUI's.
