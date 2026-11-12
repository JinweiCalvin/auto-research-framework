#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
I2P_URL="https://github.com/AgentAlphaAGI/Idea2Paper.git"
ARIS_URL="https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git"
I2P_COMMIT="64170d4d9ca9068b26bd561648ce5c576bf1a2fb"
ARIS_COMMIT="ed593c72011936adaef2d6e6cc57f98ce80f8b4e"
ARIS_SKILLS="$(tr '\n' ',' < "$(dirname "${BASH_SOURCE[0]}")/config/aris-skills.txt" | sed 's/,$//')"

for command in git python3; do
  command -v "$command" >/dev/null 2>&1 || { echo "Missing required command: $command" >&2; exit 1; }
done

clone_pinned() {
  local url="$1" path="$2" commit="$3"
  if [[ -e "$path" ]]; then
    if [[ -d "$path/.git" ]] && [[ "$(git -C "$path" remote get-url origin 2>/dev/null || true)" == "$url" ]] \
      && [[ "$(git -C "$path" rev-parse HEAD 2>/dev/null || true)" == "$commit" ]]; then
      echo "Pinned dependency already present: $path"
      return
    fi
    echo "Existing path is not the expected pinned checkout; leaving it untouched: $path" >&2
    exit 1
  fi
  git clone --depth 1 --filter=blob:none "$url" "$path"
  git -C "$path" checkout --detach "$commit"
}

cd "$ROOT"
clone_pinned "$I2P_URL" "$ROOT/idea2paper" "$I2P_COMMIT"
mkdir -p "$ROOT/aris"
clone_pinned "$ARIS_URL" "$ROOT/aris/auto-claude-code-research-in-sleep" "$ARIS_COMMIT"

I2P_APP="$ROOT/idea2paper/frontend/server/app.py"
APP_OVERLAY="$ROOT/patches/idea2paper/frontend/server/app.py"
if ! cmp -s "$I2P_APP" "$APP_OVERLAY"; then
  if ! git -C "$ROOT/idea2paper" diff HEAD --quiet -- frontend/server/app.py; then
    echo "Refusing to overwrite a locally modified Idea2Paper app.py: $I2P_APP" >&2
    exit 1
  fi
  cp "$APP_OVERLAY" "$I2P_APP"
  echo "Applied the version-pinned local workspace dashboard adapter."
fi

if [[ ! -f "$ROOT/idea2paper/.env" ]]; then
  cp "$ROOT/idea2paper/.env.example" "$ROOT/idea2paper/.env"
  echo "Created idea2paper/.env; add your API credentials locally before running Idea2Paper."
fi

mkdir -p "$ROOT/research-projects"

if command -v codex >/dev/null 2>&1; then
  bash "$ROOT/aris/auto-claude-code-research-in-sleep/tools/install_aris_codex.sh" \
    "$ROOT" \
    --aris-repo "$ROOT/aris/auto-claude-code-research-in-sleep" \
    --skills "$ARIS_SKILLS" \
    --skip-new --quiet --no-doc
else
  echo "Codex CLI is not installed; ARIS skills were not installed. Install Codex and rerun setup.sh when ready."
fi

cat <<'EOF'

Framework setup is complete.
Next:
1. Read docs/DEPLOYMENT_CN.md and add API credentials to idea2paper/.env.
2. Create a project with tools/create_research_project.py.
3. Use `/anti-defensive-writing` when drafting or revising research text.
4. Follow docs/WORKFLOW_CN.md; do not start a long experiment before reviewing its plan.
EOF
