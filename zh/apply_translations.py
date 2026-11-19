import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATIC = ROOT / "src" / "free_claude_code" / "api" / "admin_static"
STRINGS = pathlib.Path(__file__).resolve().parent / "strings.json"


def apply_pairs(path: pathlib.Path, pairs) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    applied = 0
    missing = 0
    for old, new in pairs:
        if new in text:
            continue
        if old in text:
            text = text.replace(old, new)
            applied += 1
        else:
            missing += 1
    path.write_text(text, encoding="utf-8")
    return applied, missing


def apply_quoted(path: pathlib.Path, pairs: dict) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    applied = 0
    missing = 0
    for en, zh in pairs.items():
        done = False
        for q in ('"', "'", "`"):
            if f"{q}{en}{q}" in text:
                text = text.replace(f"{q}{en}{q}", f"{q}{zh}{q}")
                applied += 1
                done = True
                break
        if not done:
            if f'"{zh}"' in text or f"'{zh}'" in text:
                continue  # already translated
            missing += 1
    path.write_text(text, encoding="utf-8")
    return applied, missing


EN_SENTENCE = re.compile(r'"((?:[^"\\\n]){4,140})"|`((?:[^`\\\n]){4,140})`')
CSS_LIKE = re.compile(r"[<>{}$=;/()\[\]]|noopener|username|textarea|button|input|select|use strict")


def report_untranslated() -> int:
    total = 0
    for name in ("admin.js", "code_sessions.js", "session_ui.js", "api_key_editor.js", "form_controls.js", "index.html"):
        p = STATIC / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        found = []
        for m in EN_SENTENCE.finditer(text):
            s = (m.group(1) or m.group(2) or "").strip()
            if not re.search(r"[A-Za-z]{2,}\s+[A-Za-z]{2,}", s):
                continue
            if re.search(r"[\u4e00-\u9fff]", s):
                continue
            if CSS_LIKE.search(s):
                continue
            found.append(s)
        if found:
            total += len(found)
            print(f"[待补译] {name}:")
            for s in sorted(set(found)):
                print("   ", s)
    return total


def main() -> int:
    data = json.loads(STRINGS.read_text(encoding="utf-8"))
    errors = 0

    for name, pairs in data.get("html_literals", {}).items():
        p = STATIC / name.lstrip("/")
        if p.exists():
            a, m = apply_pairs(p, pairs)
            print(f"html {name}: applied {a}, unmatched {m}")

    for name, pairs in data.get("template_literals", {}).items():
        p = STATIC / name
        if p.exists():
            a, m = apply_pairs(p, [[o, n] for o, n in pairs])
            print(f"tpl  {name}: applied {a}, unmatched {m}")

    for name, pairs in data.get("string_literals", {}).items():
        p = STATIC / name
        if p.exists():
            a, m = apply_quoted(p, pairs)
            print(f"str  {name}: applied {a}, unmatched {m}")

    left = report_untranslated()
    print(f"\n剩余疑似英文界面文案: {left}")
    return 0 if left == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
