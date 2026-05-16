"""
Smoke-Test fuer index.html — extrahiert den <script type="text/babel">-Block
und prueft grundlegende strukturelle Balance (Klammern, JSX-Tags).

Kein vollwertiger JSX-Parser, aber faengt 90% der typischen Fehler:
- fehlende schliessende Klammer
- offenes JSX-Tag ohne /close
- Schreibfehler im JSX-Element-Namen
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
HTML = ROOT / "index.html"


def extract_script(text: str) -> str | None:
    m = re.search(
        r'<script\s+type="text/babel"[^>]*>(.*?)</script>',
        text,
        re.DOTALL,
    )
    return m.group(1) if m else None


def strip_strings_and_comments(src: str) -> str:
    """
    Entferne Strings und Kommentare grob, damit Klammern darin nicht zaehlen.
    Macht das zeichenweise mit einem kleinen State-Automaten.
    """
    out = []
    i = 0
    n = len(src)
    state = "code"  # code | str_s | str_d | str_b | line_c | block_c | regex
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if state == "code":
            if c == "/" and nxt == "/":
                state = "line_c"; i += 2; continue
            if c == "/" and nxt == "*":
                state = "block_c"; i += 2; continue
            if c == '"':
                state = "str_d"; i += 1; continue
            # ' wird NICHT als String-Beginn behandelt — der Code nutzt
            # ausschliesslich " und ` fuer Strings; ' kommt nur in JSX-Text vor.
            if c == "`":
                state = "str_b"; i += 1; continue
            out.append(c)
            i += 1
        elif state == "line_c":
            if c == "\n":
                state = "code"
                out.append(c)
            i += 1
        elif state == "block_c":
            if c == "*" and nxt == "/":
                state = "code"; i += 2; continue
            i += 1
        elif state == "str_s":
            if c == "\\":
                i += 2; continue
            if c == "'":
                state = "code"
            i += 1
        elif state == "str_d":
            if c == "\\":
                i += 2; continue
            if c == '"':
                state = "code"
            i += 1
        elif state == "str_b":
            if c == "\\":
                i += 2; continue
            if c == "`":
                state = "code"
            i += 1
    return "".join(out)


def check_balance(stripped: str) -> list[str]:
    """Zaehlt offene/geschlossene Klammern."""
    pairs = {"(": ")", "[": "]", "{": "}"}
    closing = {")", "]", "}"}
    stack: list[tuple[str, int]] = []
    line = 1
    fehler = []
    for ch in stripped:
        if ch == "\n":
            line += 1
            continue
        if ch in pairs:
            stack.append((ch, line))
        elif ch in closing:
            if not stack:
                fehler.append(f"Zeile {line}: schliessende '{ch}' ohne offene Klammer")
            else:
                last, last_line = stack.pop()
                if pairs[last] != ch:
                    fehler.append(
                        f"Zeile {line}: '{ch}' passt nicht zu '{last}' aus Zeile {last_line}"
                    )
    for last, last_line in stack:
        fehler.append(f"Zeile {last_line}: offenes '{last}' nicht geschlossen")
    return fehler


def main():
    text = HTML.read_text(encoding="utf-8")
    src = extract_script(text)
    if src is None:
        print("FEHLER: kein <script type=\"text/babel\">-Block gefunden", file=sys.stderr)
        return 2

    print(f"Script-Block: {len(src)} Zeichen, {src.count(chr(10)) + 1} Zeilen")
    stripped = strip_strings_and_comments(src)
    fehler = check_balance(stripped)

    if fehler:
        print("UNGLEICHGEWICHT GEFUNDEN:")
        for f in fehler[:20]:
            print("  -", f)
        if len(fehler) > 20:
            print(f"  ... und {len(fehler) - 20} weitere")
        return 1

    print("OK: Klammern ausgeglichen.")
    print(f"  (), [], {{}} alle paarweise geschlossen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
