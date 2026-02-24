#!/usr/bin/env bash
# validate-agents.sh — Check agent pool consistency
#
# Validates:
#   1. Required frontmatter fields in every agent file
#   2. Valid values for color, model, permissionMode
#   3. Tool lists match defined tiers
#   4. Each agent has 3 <example> blocks in description
#   5. System prompt has the three required sections
#   6. Agent names are cross-referenced in skills files
#   7. Total description context budget
#
# Usage: bash scripts/validate-agents.sh [--verbose]
# Exit codes: 0 = all checks pass, 1 = failures found

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENTS_DIR="$ROOT_DIR/agents"

VERBOSE=false
[[ "${1:-}" == "--verbose" ]] && VERBOSE=true

ERRORS=0
WARNINGS=0

# Colours for output
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m'

error() {
  echo -e "${RED}ERROR${NC}: $1"
  ERRORS=$((ERRORS + 1))
}

warn() {
  echo -e "${YELLOW}WARN${NC}: $1"
  WARNINGS=$((WARNINGS + 1))
}

info() {
  $VERBOSE && echo "  $1"
  return 0
}

# Valid values
VALID_COLORS="blue cyan green yellow magenta red"
VALID_MODELS="inherit sonnet opus haiku"
VALID_PERMISSIONS="default acceptEdits plan dontAsk bypassPermissions"

# Tool tier definitions
TIER_READONLY="Bash Glob Grep NotebookRead Read"
TIER_DOCUMENTATION="Bash Edit Glob Grep Read Write"
TIER_IMPLEMENTATION="Bash Edit Glob Grep MultiEdit NotebookEdit Read Write"
TIER_FULL="Bash Edit Glob Grep MultiEdit NotebookEdit Read TodoWrite WebFetch WebSearch Write"

sort_tools() {
  echo "$1" | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort | tr '\n' ' ' | sed 's/ $//'
}

identify_tier() {
  local sorted_tools
  sorted_tools=$(sort_tools "$1")
  if [[ "$sorted_tools" == "$TIER_READONLY" ]]; then echo "Read-only"
  elif [[ "$sorted_tools" == "$TIER_DOCUMENTATION" ]]; then echo "Documentation"
  elif [[ "$sorted_tools" == "$TIER_IMPLEMENTATION" ]]; then echo "Implementation"
  elif [[ "$sorted_tools" == "$TIER_FULL" ]]; then echo "Full access"
  else echo "unknown"
  fi
}

echo "Validating agent pool..."
echo ""

# ── Check each agent file ────────────────────────────────────────────
AGENT_COUNT=0
TOTAL_DESC_CHARS=0
AGENT_NAMES=()

for agent_file in "$AGENTS_DIR"/*.md; do
  filename=$(basename "$agent_file")
  AGENT_COUNT=$((AGENT_COUNT + 1))
  info "Checking $filename"

  # Normalise line endings (handle \r\n) and extract frontmatter
  clean_file=$(tr -d '\r' < "$agent_file")
  frontmatter=$(echo "$clean_file" | sed -n '/^---$/,/^---$/p' | sed '1d;$d')

  if [[ -z "$frontmatter" ]]; then
    error "$filename: No YAML frontmatter found"
    continue
  fi

  # Extract fields
  name=$(echo "$frontmatter" | grep -oP '^name:\s*\K\S+' || true)
  model=$(echo "$frontmatter" | grep -oP '^model:\s*\K\S+' || true)
  color=$(echo "$frontmatter" | grep -oP '^color:\s*\K\S+' || true)
  tools=$(echo "$frontmatter" | grep -oP '^tools:\s*\K.*' || true)
  permission=$(echo "$frontmatter" | grep -oP '^permissionMode:\s*\K\S+' || true)

  # Check description exists (multiline field, just check it's present)
  has_description=$(echo "$frontmatter" | grep -c '^description:' || true)

  # Required fields
  [[ -z "$name" ]] && error "$filename: Missing 'name' field"
  [[ -z "$model" ]] && error "$filename: Missing 'model' field"
  [[ -z "$color" ]] && error "$filename: Missing 'color' field"
  [[ -z "$tools" ]] && error "$filename: Missing 'tools' field"
  [[ -z "$permission" ]] && error "$filename: Missing 'permissionMode' field"
  [[ "$has_description" -eq 0 ]] && error "$filename: Missing 'description' field"

  # Valid values
  if [[ -n "$color" ]] && ! echo "$VALID_COLORS" | grep -qw "$color"; then
    error "$filename: Invalid color '$color' (expected: $VALID_COLORS)"
  fi
  if [[ -n "$model" ]] && ! echo "$VALID_MODELS" | grep -qw "$model"; then
    error "$filename: Invalid model '$model' (expected: $VALID_MODELS)"
  fi
  if [[ -n "$permission" ]] && ! echo "$VALID_PERMISSIONS" | grep -qw "$permission"; then
    error "$filename: Invalid permissionMode '$permission'"
  fi

  # Name format (kebab-case, 3-50 chars)
  if [[ -n "$name" ]]; then
    AGENT_NAMES+=("$name")
    if ! echo "$name" | grep -qP '^[a-z][a-z0-9-]{1,48}[a-z0-9]$'; then
      error "$filename: Name '$name' is not valid kebab-case (3-50 chars, lowercase letters/digits/hyphens)"
    fi
    # Check filename matches name
    expected_name=$(echo "$filename" | sed 's/^[0-9]*-//;s/\.md$//')
    if [[ "$name" != "$expected_name" ]]; then
      error "$filename: Name '$name' doesn't match filename (expected '$expected_name')"
    fi
  fi

  # Tool tier check
  if [[ -n "$tools" ]]; then
    tier=$(identify_tier "$tools")
    if [[ "$tier" == "unknown" ]]; then
      warn "$filename: Tool list doesn't match any defined tier ($(sort_tools "$tools"))"
    else
      info "  Tier: $tier"
    fi
  fi

  # Count <example> blocks
  example_count=$(echo "$clean_file" | grep -c '<example>' || true)
  if [[ "$example_count" -ne 3 ]]; then
    warn "$filename: Has $example_count <example> blocks (expected 3)"
  fi

  # Check system prompt sections (content after second ---)
  body=$(echo "$clean_file" | sed -n '/^---$/,/^---$/!p' | tail -n +1)
  if ! echo "$body" | grep -q '## Core expertise'; then
    error "$filename: Missing '## Core expertise' section in system prompt"
  fi
  if ! echo "$body" | grep -q '## Working standards'; then
    error "$filename: Missing '## Working standards' section in system prompt"
  fi
  if ! echo "$body" | grep -q '## When given a task'; then
    error "$filename: Missing '## When given a task' section in system prompt"
  fi

  # Description size for context budget
  desc_text=$(echo "$clean_file" | sed -n '/^description:/,/^[a-z]/p' | head -n -1)
  desc_chars=${#desc_text}
  TOTAL_DESC_CHARS=$((TOTAL_DESC_CHARS + desc_chars))

done

echo ""

# ── Cross-reference agents in skills ─────────────────────────────────
echo "Cross-referencing agents with skills..."

BROWSE_POOL="$ROOT_DIR/skills/browse-pool/SKILL.md"
ASSEMBLE_TEAM="$ROOT_DIR/skills/assemble-team/SKILL.md"

for name in "${AGENT_NAMES[@]}"; do
  if [[ -f "$BROWSE_POOL" ]] && ! grep -q "$name" "$BROWSE_POOL"; then
    error "Agent '$name' not found in browse-pool skill"
  fi
  if [[ -f "$ASSEMBLE_TEAM" ]] && ! grep -q "$name" "$ASSEMBLE_TEAM"; then
    error "Agent '$name' not found in assemble-team skill"
  fi
done

echo ""

# ── Context budget ───────────────────────────────────────────────────
BUDGET_LIMIT=50000
echo "Context budget: ~${TOTAL_DESC_CHARS} chars / ${BUDGET_LIMIT} limit"
if [[ "$TOTAL_DESC_CHARS" -gt "$BUDGET_LIMIT" ]]; then
  error "Total description text exceeds ${BUDGET_LIMIT} char budget"
elif [[ "$TOTAL_DESC_CHARS" -gt $((BUDGET_LIMIT * 80 / 100)) ]]; then
  warn "Description text is above 80% of budget (${TOTAL_DESC_CHARS}/${BUDGET_LIMIT})"
fi

echo ""

# ── Summary ──────────────────────────────────────────────────────────
echo "─────────────────────────────────"
echo "Agents checked: $AGENT_COUNT"
if [[ "$ERRORS" -eq 0 && "$WARNINGS" -eq 0 ]]; then
  echo -e "${GREEN}All checks passed.${NC}"
elif [[ "$ERRORS" -eq 0 ]]; then
  echo -e "${YELLOW}${WARNINGS} warning(s), 0 errors.${NC}"
else
  echo -e "${RED}${ERRORS} error(s), ${WARNINGS} warning(s).${NC}"
fi

exit $([[ "$ERRORS" -gt 0 ]] && echo 1 || echo 0)
