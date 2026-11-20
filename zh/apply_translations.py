import ast
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATIC = ROOT / "src" / "free_claude_code" / "api" / "admin_static"
STRINGS = pathlib.Path(__file__).resolve().parent / "strings.json"
SOURCE_URL = "https://github.com/303528084/free-claude-code"


def apply_pairs(path: pathlib.Path, pairs) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    applied = 0
    missing = 0
    # 长串优先，避免短串先替换导致长串再也匹配不上
    for old, new in sorted(pairs, key=lambda p: len(p[0]), reverse=True):
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
CSS_LIKE = re.compile(
    r"[<>{}$=;/()\[\]]"
    r"|^[a-z0-9]+(?:-[a-z0-9]+)+$"      # kebab-case 类名
    r"|noopener|use strict"
)
# 有意保留英文的名称（API 类型、产品名、品牌与专有名词）
KEEP_EN = {
    "Anthropic Messages",
    "Chat Completions",
    "Claude Code",
    "Codex",
    "Free Claude Code",
    # 单词级
    "Anthropic",
    "Claude",
    "OpenAI",
    "Azure",
    "Google",
    "Vertex",
    "Bedrock",
    "Mistral",
    "NVIDIA",
    "Discord",
    "Telegram",
    "Slack",
    "Gemini",
    "Copilot",
    "FCC",
    "None",
    "Fable",
    "Opus",
    "Sonnet",
    "Haiku",
    "JetBrains",
    "DeepSeek",
    "GitHub",
    "OAuth",
    "API",
    "Token",
    "URL",
    "JSON",
    "HTTP",
    "HTTPS",
}

# 单个大写开头的英文词（按钮、字段名等短标签）
EN_WORD = re.compile(r'"([A-Z][A-Za-z\-]{2,24})"')
# 只有出现在“给用户看”的上下文里才当界面文案
UI_HINT = re.compile(
    r"textContent|innerText|innerHTML|\.label|label:|title:|setAttribute\s*\(\s*\"aria-label\""
    r"|placeholder|button\(|choice\(|heading|optionLabel|ariaLabel|document\.title"
    r"|el\(\"button\"|createElement\(\"button\""
)
# 这些单词是数据键 / 方法名 / 快捷键，不是界面文案
NOT_TEXT = {
    "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS",
    "Enter", "Escape", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
    "AbortError", "MODEL", "Default", "Auto-review",
}


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
            if all(re.fullmatch(r"[a-z0-9-]+", t) for t in s.split()):
                continue
            if s.strip() in KEEP_EN:
                continue
            found.append(s)
        for line in text.splitlines():
            if not UI_HINT.search(line):
                continue
            for m in EN_WORD.finditer(line):
                w = m.group(1)
                if w in KEEP_EN or w in NOT_TEXT:
                    continue
                if re.search(r"[<>{}$=;/()\[\]]", w):
                    continue
                found.append(w)
        if found:
            total += len(found)
            print(f"[待补译] {name}:")
            for s in sorted(set(found)):
                print("   ", s)
    return total


def quote_literal(value: str) -> str:
    if '"' in value and "'" not in value:
        return f"'{value}'"
    return '"' + value.replace('"', '\\"') + '"'


def apply_python(path: pathlib.Path, spec: dict) -> tuple[int, list]:
    """用 AST 定位字符串常量，按整段替换（可处理跨行隐式拼接与 f-string 片段）。"""
    literals = spec.get("literals", {})
    fragments = spec.get("fragments", {})
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    parent = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node

    lines = src.splitlines(keepends=True)

    def offset(lineno: int, col: int) -> int:
        return sum(len(line) for line in lines[: lineno - 1]) + col

    edits = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        joined = isinstance(parent.get(node), ast.JoinedStr)
        mapping = fragments if joined else literals
        zh = mapping.get(node.value)
        if zh is None:
            continue
        if joined:
            new_text = zh.replace("{", "{{").replace("}", "}}")
        else:
            new_text = quote_literal(zh)
        edits.append((node.lineno, node.col_offset, node.end_lineno, node.end_col_offset, new_text))

    for lineno, col, end_lineno, end_col, new_text in sorted(edits, reverse=True):
        start = offset(lineno, col)
        end = offset(end_lineno, end_col)
        src = src[:start] + new_text + src[end:]
        lines = src.splitlines(keepends=True)

    ast.parse(src)
    path.write_text(src, encoding="utf-8")

    # 复核：重新解析，看还有哪些英文常量未被替换
    leftover = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value in literals or node.value in fragments:
                leftover.append(node.value)
    return len(edits), leftover


def inject_source_link() -> bool:
    """在 Admin 页脚加"源码"链接（AGPL-3.0 §13 的源码获取入口），幂等。"""
    path = STATIC / "index.html"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if 'id="sourceLink"' in text:
        return False
    anchor = '<span id="configPath"></span>'
    if anchor not in text:
        print("footer 锚点缺失，跳过源码链接注入")
        return False
    link = (
        f"{anchor}\n          <a id=\"sourceLink\" href=\"{SOURCE_URL}\" target=\"_blank\" "
        'rel="noopener" style="color:inherit;opacity:.7;font-size:12px;text-decoration:underline">'
        "源码（AGPL-3.0）</a>"
    )
    path.write_text(text.replace(anchor, link, 1), encoding="utf-8")
    print("html index.html: 已注入页脚源码链接")
    return True


def main() -> int:
    data = json.loads(STRINGS.read_text(encoding="utf-8"))
    errors = 0

    inject_source_link()

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

    for rel, spec in data.get("python_literals", {}).items():
        p = ROOT / rel
        if p.exists():
            a, leftover = apply_python(p, spec)
            print(f"py   {rel}: applied {a}, leftover {len(leftover)}")
            for s in leftover:
                print(f"   [待补译] {s}")

    left = report_untranslated()
    print(f"\n剩余疑似英文界面文案: {left}")
    return 0 if left == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
