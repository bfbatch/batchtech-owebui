# BatchTechUI versions

BatchTechUI has its own version, separate from the Open WebUI version it is based on.

- BatchTechUI version: `backend/open_webui/BATCHTECH_VERSION` (one line, e.g. `1.0.0`). Shown in Settings > About as
  "BatchTechUI v1.0.0 (based on Open WebUI v0.13.0)".
- Open WebUI version: `package.json`. The weekly upstream sync bumps this; it never touches the BatchTechUI version.

## Cutting a release

1. Add an entry to `backend/open_webui/BATCHTECH_CHANGELOG.md` (shown in the "What's new" popup) and edit `backend/open_webui/BATCHTECH_VERSION` (patch for fixes, minor for features, major for breaking changes), then merge to `main`.
2. Tag and push: `git checkout main && git pull && git tag v1.0.1 && git push origin v1.0.1`.
   The "BatchTechUI release" workflow checks the tag matches the file and publishes a GitHub release.
3. Deploy by hand as usual. The version shown in Settings > About tells you what is running.
