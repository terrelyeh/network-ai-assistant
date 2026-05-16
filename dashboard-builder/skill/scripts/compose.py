#!/usr/bin/env python3
"""compose.py — Dashboard Builder

Takes a spec JSON and produces a single self-contained HTML file.

Usage:
  python compose.py --spec path/to/spec.json --out path/to/canvas-<topic>-<TS>.html
"""

from __future__ import annotations
import argparse, json, sys, datetime
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
THEME_DIR = SKILL_ROOT / "theme"
WIDGETS_DIR = SKILL_ROOT / "widgets"
RUNTIME_DIR = SKILL_ROOT / "runtime"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def assemble_theme(variant: str = "light") -> str:
    """Assemble theme CSS. `variant` picks tokens-<variant>.css; falls back to
    tokens.css for 'light' / default."""
    tokens_file = "tokens.css" if variant == "light" else f"tokens-{variant}.css"
    tokens_path = THEME_DIR / tokens_file
    if not tokens_path.exists():
        raise FileNotFoundError(f"Theme variant '{variant}' not found: {tokens_path}")
    parts = [
        f"/* === theme/{tokens_file} === */\n" + read(tokens_path),
        f"/* === theme/base.css === */\n" + read(THEME_DIR / "base.css"),
    ]
    return "\n".join(parts)


def load_widget_assets(name: str) -> dict:
    """Read a widget HTML file and split it into style / template / script."""
    path = WIDGETS_DIR / f"{name}.html"
    if not path.exists():
        raise FileNotFoundError(f"Widget not found: {path}")
    src = read(path)
    # crude extraction; assumes one <style>, optional <template>, one <script>
    def extract(tag: str, all_tags: bool = False):
        out = []
        cursor = 0
        while True:
            start = src.find(f"<{tag}", cursor)
            if start == -1: break
            close_tag = f"</{tag}>"
            end = src.find(close_tag, start)
            if end == -1: break
            inner_start = src.find(">", start) + 1
            out.append(src[inner_start:end])
            cursor = end + len(close_tag)
            if not all_tags: break
        return out
    styles = extract("style", all_tags=True)
    templates_blob = ""
    # capture full <template>...</template> blocks (id needed)
    cursor = 0
    while True:
        s = src.find("<template", cursor)
        if s == -1: break
        e = src.find("</template>", s)
        if e == -1: break
        templates_blob += src[s:e + len("</template>")] + "\n"
        cursor = e + len("</template>")
    scripts = extract("script", all_tags=True)
    return {
        "name": name,
        "style": "\n".join(styles),
        "templates": templates_blob,
        "script": "\n".join(scripts),
    }


def deep_merge(base, override):
    """Deep merge override into base.
    - dict + dict: recursive merge, override wins per-key
    - list of {id: ...} on both sides: merge by id (override fields win)
    - equal-length list: positional merge (covers kpi items, columns, filters)
    - other list / scalar / type mismatch: override replaces
    """
    if isinstance(base, dict) and isinstance(override, dict):
        out = dict(base)
        for k, v in override.items():
            out[k] = deep_merge(out[k], v) if k in out else v
        return out
    if isinstance(base, list) and isinstance(override, list):
        # id-based merge for sections
        if (base and override
                and all(isinstance(x, dict) and "id" in x for x in base)
                and all(isinstance(x, dict) and "id" in x for x in override)):
            by_id = {x["id"]: i for i, x in enumerate(base)}
            out = [dict(x) for x in base]
            for o in override:
                if o["id"] in by_id:
                    out[by_id[o["id"]]] = deep_merge(out[by_id[o["id"]]], o)
                else:
                    out.append(o)
            return out
        # Positional merge for equal-length lists
        if len(base) == len(override):
            return [deep_merge(b, o) for b, o in zip(base, override)]
        return override
    return override


def apply_locale(spec: dict, locale: str | None) -> dict:
    """Merge `spec.locales[locale]` into spec; strip the locales key from output.
    No-op if locale is None / 'default' / not declared."""
    stripped = {k: v for k, v in spec.items() if k != "locales"}
    if not locale or locale == "default":
        return stripped
    overrides = (spec.get("locales") or {}).get(locale)
    if overrides is None:
        print(f"WARN: locale '{locale}' not declared in spec.locales; using default.", file=sys.stderr)
        return stripped
    return deep_merge(stripped, overrides)


def validate_spec(spec: dict) -> None:
    if "title" not in spec:
        raise ValueError("spec.title required")
    if not spec.get("sections"):
        raise ValueError("spec.sections must be non-empty")
    live_aliases = set((spec.get("live_data") or {}).keys())
    for i, s in enumerate(spec["sections"]):
        w = s.get("widget")
        if not w:
            raise ValueError(f"sections[{i}].widget required")
        path = WIDGETS_DIR / f"{w}.html"
        if not path.exists():
            raise ValueError(f"sections[{i}].widget '{w}' not found at {path}")


def compose(spec: dict, theme: str = "light", locale: str | None = None) -> str:
    # `_html_lang` is the lang attribute on <html>; default zh-TW unless overridden
    html_lang_default = spec.get("html_lang", "zh-TW")
    spec = apply_locale(spec, locale)
    html_lang = spec.get("html_lang", html_lang_default)
    validate_spec(spec)
    title = spec.get("title", "Dashboard")
    subtitle = spec.get("subtitle", "")
    live_data = spec.get("live_data", {})
    sections = spec["sections"]
    footer = spec.get("footer", {})

    # Theme + runtime
    theme_css = assemble_theme(theme)
    runtime_js = read(RUNTIME_DIR / "runtime.js")

    # Collect widget assets, deduped by widget name
    seen = set()
    widget_assets = []
    for s in sections:
        if s["widget"] in seen: continue
        seen.add(s["widget"])
        widget_assets.append(load_widget_assets(s["widget"]))

    widget_styles = "\n".join(f"/* === widget {w['name']} === */\n{w['style']}" for w in widget_assets)
    widget_templates = "\n".join(w["templates"] for w in widget_assets if w["templates"])
    widget_scripts = "\n".join(f"/* === widget {w['name']} === */\n{w['script']}" for w in widget_assets)

    # Mount points for sections
    body_sections = []
    for s in sections:
        sid = s.get("id") or s["widget"]
        # Some widgets (alert, kpi_grid, chip_strip) are inline; cards/tables/tree are <div class="card">
        body_sections.append(f'<div data-widget-id="{sid}" data-widget="{s["widget"]}" style="margin-bottom: 20px;"></div>')

    # Build final HTML
    spec_for_runtime = {
        "live_data": live_data,
        "sections": sections,
    }

    # Inline compute functions can be supplied per-spec via `compute_fns`
    # (a JS string that runs BEFORE Dashboard.init, so it can extend computeFns).
    inline_compute_fns = spec.get("compute_fns", "")

    footer_ops = " + ".join(footer.get("ops_used", [])) if footer.get("ops_used") else ""
    footer_html = f"""
  <div class="db-footnote">
    <div>Generated by dashboard-builder · auto-refresh every 5s</div>
    <div class="skills">{footer_ops}</div>
  </div>
""" if footer else ""

    html = f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{theme_css}

{widget_styles}
</style>
</head>
<body>

<header class="db-hdr">
  <div class="db-hdr-inner">
    <div class="db-hdr-left">
      <img class="db-brand-logo" src="assets/engenius-logo.png" alt="EnGenius Cloud" />
      <div class="db-hdr-titles">
        <h1>{title}</h1>
        <div class="crumb">{subtitle}</div>
      </div>
    </div>
    <div class="db-hdr-right">
      <button class="btn" id="db-refresh" title="重新抓取所有資料"><span class="ic">↻</span> Refresh</button>
      <div class="live-dot">Live</div>
      <div class="updated" id="db-updated">—</div>
    </div>
  </div>
</header>

<main class="db-wrap">
{chr(10).join(body_sections)}
{footer_html}
</main>

{widget_templates}

<script>
{runtime_js}
</script>

<script>
{widget_scripts}
</script>

<script>
/* === inline compute_fns from spec === */
{inline_compute_fns}
</script>

<script>
Dashboard.init({json.dumps(spec_for_runtime, ensure_ascii=False)});
</script>

</body>
</html>
"""
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="Path to spec JSON file")
    ap.add_argument("--out", required=True, help="Output HTML path")
    ap.add_argument("--theme", default="light", help="Theme variant: 'light' (default) or 'dark' (uses tokens-dark.css)")
    ap.add_argument("--locale", default=None, help="Locale override; merges spec.locales[<locale>] into base spec. Example: --locale en or --locale ja")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    try:
        html = compose(spec, theme=args.theme, locale=args.locale)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
