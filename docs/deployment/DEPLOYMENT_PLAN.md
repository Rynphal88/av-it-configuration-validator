# Deployment and Configuration Plan

## Selected method

Build a versioned Docker image and run it on an engineer workstation or an
internal, access-controlled host. Mount sanitized or authorized scene files and
the approved rule catalog read-only. Do not expose a public network endpoint and
do not connect the container to a live console.

## Prerequisites

- Docker Engine 24 or later, or Python 3.11 or later for direct installation
- Git for source retrieval
- Read access to candidate, baseline, and rule files
- Write access only to an external report destination when JSON is redirected

## Settings

| Variable | Default | Purpose |
|---|---:|---|
| `AV_VALIDATOR_MAX_SCENE_BYTES` | `2000000` | Rejects oversized scene inputs before parsing |
| `AV_VALIDATOR_OUTPUT_FORMAT` | `text` | Selects `text` or `json` output |

## Build and run

```bash
git clone https://github.com/Rynphal88/av-it-configuration-validator.git
cd av-it-configuration-validator
docker build -t av-it-configuration-validator:0.3.0 .
docker run --rm --read-only \
  -v "$PWD/sample-configs:/data/sample-configs:ro" \
  -v "$PWD/rules:/data/rules:ro" \
  av-it-configuration-validator:0.3.0 \
  --candidate /data/sample-configs/sanitized/candidate-drift.scn \
  --baseline /data/sample-configs/sanitized/approved-baseline.scn \
  --rules /data/rules/demo_rules.json
```

## Direct-install fallback

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

On Windows PowerShell, activate with `.\\.venv\\Scripts\\Activate.ps1`.

## Reliability controls

The tagged source revision, dependency metadata, rule-catalog hash, baseline and
candidate hashes, environment settings, and image tag together define the
deployment baseline. Pull requests and CI provide change control; test and
evaluation logs provide status accounting; release notes and tags identify the
approved build. Rollback means selecting the prior immutable image tag and its
matching approved rule catalog. Configuration changes must be reviewed and
retested before a new release is tagged.
