#!/usr/bin/env bash
# ABOUTME: Packages the implementation-guide skill folder into a distributable .skill file.
# ABOUTME: Output goes to dist/implementation-guide.skill (a ZIP archive).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$SCRIPT_DIR/implementation-guide"
DIST_DIR="$SCRIPT_DIR/dist"

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "Error: SKILL.md not found in $SKILL_DIR"
    exit 1
fi

mkdir -p "$DIST_DIR"

# Remove old build
rm -f "$DIST_DIR/implementation-guide.skill"

# Package as ZIP with .skill extension
cd "$SCRIPT_DIR"
zip -r "$DIST_DIR/implementation-guide.skill" implementation-guide/ \
    -x "implementation-guide/__pycache__/*" \
    -x "implementation-guide/.DS_Store" \
    -x "implementation-guide/evals/*"

echo ""
echo "Packaged: $DIST_DIR/implementation-guide.skill"
echo "Upload this file to Claude.ai (Settings > Customize > Skills)"
echo "Or rename to .zip if your Claude version requires it."
