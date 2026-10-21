#!/usr/bin/env python3
"""Check every skill: lives at skills/<category>/<name>/SKILL.md, has frontmatter
with name and description, name matches the folder, and names are unique."""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors, seen = [], {}
for f in sorted(root.glob("skills/*/*/SKILL.md")):
    name_dir = f.parent.name
    text = f.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        errors.append(f"{f}: missing frontmatter"); continue
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    if not name:
        errors.append(f"{f}: missing name")
    elif name.group(1).strip().strip("'\"") != name_dir:
        errors.append(f"{f}: name '{name.group(1).strip()}' != folder '{name_dir}'")
    if not re.search(r"^description:", fm, re.M):
        errors.append(f"{f}: missing description")
    if name_dir in seen:
        errors.append(f"{f}: duplicate name, also in {seen[name_dir]}")
    seen[name_dir] = f.parent.parent.name
stray = [p for p in root.glob("skills/**/SKILL.md") if len(p.relative_to(root).parts) != 4]
errors += [f"{p}: not at skills/<category>/<name>/SKILL.md" for p in stray]
for e in errors:
    print("ERROR", e)
print(f"{len(seen)} skills checked, {len(errors)} errors")
sys.exit(1 if errors else 0)
