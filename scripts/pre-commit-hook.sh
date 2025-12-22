#!/bin/bash
set -e

echo "🔍 Pre-commit checks..."

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)
if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

ERROR_COUNT=0

# Django templates
TEMPLATES=$(echo "$STAGED_FILES" | grep '\.html$' || echo "")
if [ -n "$TEMPLATES" ]; then
  echo "📝 Checking templates..."
  bash scripts/check_template_tags.sh || ((ERROR_COUNT++))
  npx htmlhint $TEMPLATES || ((ERROR_COUNT++))
  bash scripts/check-html-rules.sh || ((ERROR_COUNT++))
fi

# CSS files
CSS_FILES=$(echo "$STAGED_FILES" | grep '\.css$' | grep -v 'reset.css' || echo "")
if [ -n "$CSS_FILES" ]; then
  echo "🎨 Checking CSS..."
  npx stylelint $CSS_FILES || ((ERROR_COUNT++))
  bash scripts/check-css-rules.sh || ((ERROR_COUNT++))
fi

# JS files
JS_FILES=$(echo "$STAGED_FILES" | grep '\.js$' || echo "")
if [ -n "$JS_FILES" ]; then
  echo "⚡ Checking JavaScript..."
  npx eslint $JS_FILES || ((ERROR_COUNT++))
  bash scripts/check-js-rules.sh || ((ERROR_COUNT++))
fi

if [ $ERROR_COUNT -gt 0 ]; then
  echo "❌ Pre-commit checks FAILED! ($ERROR_COUNT errors)"
  echo "💡 Run 'npm run fix:rules' to auto-fix some issues"
  exit 1
fi

echo "✅ All pre-commit checks passed!"
exit 0




