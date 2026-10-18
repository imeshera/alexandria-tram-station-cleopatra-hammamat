#!/bin/zsh
# Pre-commit audit: no personal/work paths or names, no scratch paths, no third-party images, no files > 50 MB.
cd "$(dirname "$0")/.."
fail=0
files=$(git ls-files --cached --others --exclude-standard)
for pat in '/Users/' 'ibrahimeshera' 'CHAOS' 'chaosinc' 'claude-502' '/private/tmp' 'scratchpad'; do
  hits=$(print -l $files | grep -v '^tools/audit.sh$' | xargs grep -Il -- "$pat" 2>/dev/null)
  [ -n "$hits" ] && { echo "FAIL pattern '$pat':"; echo "$hits"; fail=1; }
done
imgs=$(print -l $files | grep -iE '\.(jpe?g|png|gif|webp|heic|tiff?)$' | grep -v '^docs/renders/')
[ -n "$imgs" ] && { echo "FAIL images outside docs/renders:"; echo "$imgs"; fail=1; }
big=$(print -l $files | while read f; do [ -f "$f" ] && [ $(stat -f%z "$f") -gt 52428800 ] && echo "$f"; done)
[ -n "$big" ] && { echo "FAIL files > 50 MB:"; echo "$big"; fail=1; }
for f in models/*.f3d(N); do
  unzip -l "$f" | grep -iqE '\.(jpe?g|png)$' && { echo "FAIL image inside $f"; fail=1; }
done
[ $fail = 0 ] && echo "audit OK ($(print -l $files | wc -l | tr -d ' ') files)"
exit $fail
