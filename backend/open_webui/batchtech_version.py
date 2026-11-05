# BATCHTECH: BatchTechUI's own version, separate from the upstream Open WebUI version in package.json.
# Upstream merges bump package.json only; this number changes only when a BatchTechUI release is cut.
from pathlib import Path

try:
    BATCHTECH_VERSION = (Path(__file__).parent / 'BATCHTECH_VERSION').read_text().strip() or '0.0.0'
except Exception:
    BATCHTECH_VERSION = '0.0.0'
