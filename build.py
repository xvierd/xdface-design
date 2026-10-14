#!/usr/bin/env python3
"""Generate xdface token artifacts from tokens.json.

Edit tokens.json, then run `python3 build.py`.
`python3 build.py --check` exits 1 when a generated file is stale.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "tokens.json"

GENERATED = [
    ROOT / "tokens.css",
    ROOT / "tokens.ts",
    ROOT / "tailwind.preset.js",
    ROOT / "contrast.json",
    ROOT / "logo" / "logo.svg",
    ROOT / "logo" / "logo-dark.svg",
    ROOT / "logo" / "logo-sepia.svg",
    ROOT / "logo" / "logo-mark-transparent-light.svg",
    ROOT / "logo" / "logo-mark-transparent-dark.svg",
    ROOT / "logo" / "favicon.svg",
    ROOT / "logo" / "favicon-dark.svg",
    ROOT / "logo" / "favicon-16.svg",
    ROOT / "logo" / "favicon-16-dark.svg",
    ROOT / "web" / "public" / "favicon.svg",
    ROOT / "web" / "public" / "favicon-dark.svg",
    ROOT / "web" / "public" / "favicon-16.svg",
    ROOT / "web" / "public" / "favicon-16-dark.svg",
    ROOT / "web" / "public" / "logo.svg",
    ROOT / "web" / "public" / "logo-dark.svg",
    ROOT / "web" / "public" / "logo-sepia.svg",
    ROOT / "web" / "public" / "logo-mark-transparent-light.svg",
    ROOT / "web" / "public" / "logo-mark-transparent-dark.svg",
    ROOT / "web" / "public" / "styles" / "global.css",
]

THEME_MAP = {
    "bg": ["bg", "deep"],
    "surface": ["surface", "base"],
    "raised": ["surface-2", "raised"],
    "chrome": ["chrome"],
    "fg": ["fg", "text"],
    "fg2": ["fg-2"],
    "fg3": ["fg-3", "text-muted"],
    "fg4": ["fg-4"],
    "bd": ["bd", "border", "border-subtle"],
    "bd2": ["bd-2", "border-strong"],
    "action": ["action"],
    "actionFg": ["action-fg"],
    "actionHover": ["action-hover"],
    "actionEnd": ["action-end"],
    "link": ["link"],
    "accent": ["accent"],
    "success": ["success"],
    "warning": ["warning"],
    "error": ["error"],
    "info": ["info"],
    "xp": ["xp"],
    "streak": ["streak"],
    "badge": ["badge"],
    "mustard": ["mustard"],
    "paperLine": ["paper-line"],
    "brandGreen": ["brand-green"],
    "brandOrange": ["brand-orange"],
}

XDS_ALIASES = (
    "deep",
    "base",
    "raised",
    "chrome",
    "fg",
    "fg-2",
    "fg-3",
    "fg-4",
    "bd",
    "bd-2",
)

# Unhyphenated names shipped in 0.2. Keep them until 2.0.
XDS_LEGACY = {
    "fg2": "fg-2",
    "fg3": "fg-3",
    "fg4": "fg-4",
    "bd2": "bd-2",
    "gl": "gl",
    "sidebar-bg": "sidebar-bg",
    "sidebar-sep": "sidebar-sep",
}


def camel(name: str) -> str:
    return re.sub(r"-(\w)", lambda match: match.group(1).upper(), name)


def rel_luminance(hex_color: str) -> float:
    raw = hex_color.lstrip("#")
    channels = [int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [
        channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    lighter = max(rel_luminance(a), rel_luminance(b))
    darker = min(rel_luminance(a), rel_luminance(b))
    return round((lighter + 0.05) / (darker + 0.05), 2)


def load_tokens() -> dict:
    with SOURCE.open(encoding="utf-8") as handle:
        return json.load(handle)


def svg_mark(theme: str, spec: dict, size: int = 128, tile: bool = True, simple: bool = False) -> str:
    bg, border, green, orange = spec["bg"], spec["border"], spec["green"], spec["orange"]
    stroke = 10
    grin = 8
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="{size}" height="{size}">',
        f'<defs><linearGradient id="g-{theme}" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'<stop offset="0%" stop-color="{green}"/><stop offset="100%" stop-color="{orange}"/>',
        "</linearGradient></defs>",
    ]
    if tile:
        parts.append(f'<rect width="128" height="128" rx="28" fill="{bg}"/>')
        if not simple:
            parts.append(
                f'<rect width="126" height="126" x="1" y="1" rx="27" fill="none" stroke="{border}" stroke-width="2"/>'
            )
    if simple:
        parts.append(
            f'<g transform="rotate(-3 64 64)" stroke-linecap="round" fill="none">'
            f'<path d="M26 26 L52 52 M52 26 L26 52" stroke="{green}" stroke-width="16"/>'
            f'<path d="M76 26 L102 52 M102 26 L76 52" stroke="{orange}" stroke-width="16"/>'
            f'<path d="M20 76 C 36 108 92 112 108 76" stroke="url(#g-{theme})" stroke-width="14"/>'
            "</g></svg>"
        )
    else:
        parts.append(
            f'<g transform="rotate(-3 64 64)" stroke-linecap="round" fill="none">'
            f'<line x1="28" y1="30" x2="50" y2="52" stroke="{green}" stroke-width="{stroke}"/>'
            f'<line x1="50" y1="30" x2="28" y2="52" stroke="{green}" stroke-width="{stroke}"/>'
            f'<line x1="78" y1="30" x2="100" y2="52" stroke="{orange}" stroke-width="{stroke}"/>'
            f'<line x1="100" y1="30" x2="78" y2="52" stroke="{orange}" stroke-width="{stroke}"/>'
            f'<path d="M 22 72 C 36 102 92 108 108 72" stroke="url(#g-{theme})" stroke-width="{grin}"/>'
            "</g></svg>"
        )
    return "".join(parts)


def logo_files(tok: dict) -> dict[str, str]:
    mark = tok["mark"]
    light, dark, sepia = mark["light"], mark["dark"], mark["sepia"]
    files = {
        "logo/logo.svg": svg_mark("light", light),
        "logo/logo-dark.svg": svg_mark("dark", dark),
        "logo/logo-sepia.svg": svg_mark("sepia", sepia),
        "logo/logo-mark-transparent-light.svg": svg_mark("light", light, tile=False),
        "logo/logo-mark-transparent-dark.svg": svg_mark("dark", dark, tile=False),
        "logo/favicon.svg": svg_mark("light", light, simple=True),
        "logo/favicon-dark.svg": svg_mark("dark", dark, simple=True),
        "logo/favicon-16.svg": svg_mark("light", light, size=16, simple=True),
        "logo/favicon-16-dark.svg": svg_mark("dark", dark, size=16, simple=True),
    }
    public = {
        "web/public/favicon.svg": files["logo/favicon.svg"],
        "web/public/favicon-dark.svg": files["logo/favicon-dark.svg"],
        "web/public/favicon-16.svg": files["logo/favicon-16.svg"],
        "web/public/favicon-16-dark.svg": files["logo/favicon-16-dark.svg"],
        "web/public/logo.svg": files["logo/logo.svg"],
        "web/public/logo-dark.svg": files["logo/logo-dark.svg"],
        "web/public/logo-sepia.svg": files["logo/logo-sepia.svg"],
        "web/public/logo-mark-transparent-light.svg": files["logo/logo-mark-transparent-light.svg"],
        "web/public/logo-mark-transparent-dark.svg": files["logo/logo-mark-transparent-dark.svg"],
    }
    files.update(public)
    return files


def render_css(tok: dict) -> str:
    lines = [
        "/* xdface Design System — CSS Custom Properties (Biblioteca personal divertida)",
        " * GENERATED from tokens.json by build.py — do not edit by hand",
        ' * Usage: @import \'@xdface/tokens/css\';  Theme: <html data-xd-theme="light|dark|sepia">',
        " * Legacy aliases still apply: .dark, .xd-dark, [data-theme], [data-lib-theme].",
        " */",
        "",
        ":root {",
    ]
    for key, value in tok["primitive"].items():
        lines.append(f"  --xd-{key}: {value};")
    for name, spine in tok["spine"].items():
        lines.append(f"  --xd-spine-{name}: {spine['bg']}; --xd-spine-{name}-fg: {spine['fg']};")
    for key, value in tok["font"].items():
        lines.append(f"  --xd-font-{key}: {value};")
    for key, value in tok["radius"].items():
        lines.append(f"  --xd-radius-{key}: {value};")
    for key, value in tok["space"].items():
        lines.append(f"  --xd-space-{key}: {value};")
    for key, value in tok["motion"].items():
        lines.append(f"  --xd-{key}: {value};")
    lines += [
        "  --xd-gradient-action: linear-gradient(135deg, var(--xd-brand-green) 0%, var(--xd-brand-orange) 100%);",
        "  --xd-gradient-action-hover: var(--xd-gradient-action);",
        "  --xd-gradient-grin: linear-gradient(90deg, var(--xd-brand-green), var(--xd-brand-orange));",
        "  --xd-gradient-top-accent: var(--xd-gradient-grin);",
        f"  --xd-focus-ring: {tok['interaction']['focus-ring']};",
        "  --xd-soft-ring: var(--xd-focus-ring);",
        f"  --xd-disabled-opacity: {tok['interaction']['disabled-opacity']}; /* disabled = dashed border + fg-3, not faded */",
        "  /* type scale, z-index, neutral shadows */",
    ]
    for key, value in tok["typography"].items():
        lines.append(f"  --xd-{key}: {value};")
    for key, value in tok["z-index"].items():
        lines.append(f"  --xd-z-{key}: {value};")
    for key, value in tok["shadowScale"].items():
        lines.append(f"  --xd-shadow-{key}: {value};")
    lines.append(f"  --xd-overlay-bg: {tok['interaction']['overlay-bg']};")
    lines.append("}")

    for theme, values in tok["theme"].items():
        selectors = tok["selectors"][theme]
        lines.append("")
        lines.append(f"/* theme: {theme} */")
        lines.append(",\n".join(selectors) + " {")
        for source, names in THEME_MAP.items():
            for name in names:
                lines.append(f"  --xd-{name}: {values[source]};")
        for key, value in tok["shadow"][theme].items():
            lines.append(f"  --xd-shadow-{key}: {value};")
        lines += [
            "  --xd-soft-shadow-sm: var(--xd-shadow-paper-sm);",
            "  --xd-soft-shadow-md: var(--xd-shadow-paper-md);",
            "  --xd-soft-shadow-lg: var(--xd-shadow-paper-lg);",
            "  --xd-shadow-card-hover: var(--xd-shadow-paper-md);",
            "  --xd-gl: color-mix(in srgb, var(--xd-fg) 4%, transparent);",
            "  --xd-sidebar-bg: var(--xd-chrome);",
            "  --xd-sidebar-sep: var(--xd-bd);",
            "  /* legacy --xds-* aliases (remove in 2.0) */",
        ]
        for name in XDS_ALIASES:
            lines.append(f"  --xds-{name}: var(--xd-{name});")
        for alias, target in XDS_LEGACY.items():
            lines.append(f"  --xds-{alias}: var(--xd-{target});")
        lines.append("  --xds-shadow-soft: var(--xd-soft-shadow-sm);")
        lines.append("  --xds-shadow-soft-lg: var(--xd-soft-shadow-lg);")
        lines.append("}")

    lines += [
        "",
        "/* highlight palette — carried from v0.2, pending a sticker redesign */",
        ":root {",
    ]
    for key, value in tok["highlight"].items():
        lines.append(f"  --xd-hl-{key}: {value};")
    lines.append("}")
    lines.append("")
    lines.append(UTILITIES.rstrip())
    lines.append("")
    return "\n".join(lines) + "\n"


def render_ts(tok: dict) -> str:
    payload = {
        "gradient": {
            "action": tok["semantic"]["gradient-action"],
            "grin": tok["semantic"]["gradient-grin"],
        },
        "color": {camel(key): value for key, value in tok["primitive"].items()},
        "spine": tok["spine"],
        "theme": tok["theme"],
        "font": tok["font"],
        "radius": tok["radius"],
        "space": tok["space"],
        "motion": {camel(key): value for key, value in tok["motion"].items()},
        "typography": {camel(key): value for key, value in tok["typography"].items()},
        "zIndex": tok["z-index"],
        "shadow": tok["shadow"],
    }
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    return f"""/**
 * xdface Design System -- TypeScript tokens
 * GENERATED from tokens.json by build.py — do not edit by hand
 * Usage: import {{ tokens, setTheme }} from '@xdface/tokens'
 */

export const tokens = {body} as const;

export type XdTheme = 'light' | 'dark' | 'sepia';
export type Tokens = typeof tokens;
export const THEME_ATTR = 'data-xd-theme';

/** Set the canonical theme attribute. `auto` follows prefers-color-scheme. */
export function setTheme(t: XdTheme | 'auto', root: HTMLElement = document.documentElement) {{
  const r = t === 'auto' ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : t;
  root.setAttribute(THEME_ATTR, r);
}}

export default tokens;
"""


def render_preset(tok: dict) -> str:
    colors = {name: f"var(--xd-{name})" for names in THEME_MAP.values() for name in names}
    colors.update({key: f"var(--xd-{key})" for key in tok["primitive"]})
    colors.update({f"spine-{name}": f"var(--xd-spine-{name})" for name in tok["spine"]})
    colors.update({f"spine-{name}-fg": f"var(--xd-spine-{name}-fg)" for name in tok["spine"]})
    radius = {f"xd-{key}": f"var(--xd-radius-{key})" for key in tok["radius"]}
    spacing = {f"xd-{key}": f"var(--xd-space-{key})" for key in tok["space"]}
    dark = (
        '&:where([data-xd-theme="dark"], [data-xd-theme="dark"] *, '
        '.dark, .dark *, .xd-dark, .xd-dark *, '
        '[data-theme="dark"], [data-theme="dark"] *, '
        '[data-lib-theme="dark"], [data-lib-theme="dark"] *)'
    )
    color_json = json.dumps(colors, indent=8, ensure_ascii=False)
    return f"""/**
 * xdface Design System — Tailwind CSS Preset (GENERATED by build.py — do not edit by hand)
 * Tailwind v3: presets: [require('@xdface/tokens/tailwind')]
 * Tailwind v4 @custom-variant (canonical attribute + legacy aliases):
 *   @custom-variant dark (&:where([data-xd-theme=dark], [data-xd-theme=dark] *, .dark, .dark *, .xd-dark, .xd-dark *, [data-theme=dark], [data-theme=dark] *, [data-lib-theme=dark], [data-lib-theme=dark] *));
 */

/** @type {{import('tailwindcss').Config}} */
const xdfacePreset = {{
  darkMode: ['variant', '{dark}'],
  theme: {{
    extend: {{
      colors: {{ xd: {color_json} }},
      fontFamily: {{
        'xd-display': ['var(--xd-font-display)'],
        'xd-sans': ['var(--xd-font-sans)'],
        'xd-hand': ['var(--xd-font-hand)'],
        'xd-mono': ['var(--xd-font-mono)'],
      }},
      borderRadius: {json.dumps(radius)},
      spacing: {json.dumps(spacing)},
      boxShadow: {{
        'xd-paper-sm': 'var(--xd-shadow-paper-sm)',
        'xd-paper-md': 'var(--xd-shadow-paper-md)',
        'xd-paper-lg': 'var(--xd-shadow-paper-lg)',
        'xd-focus': 'var(--xd-focus-ring)',
        'xd-xs': 'var(--xd-shadow-xs)',
        'xd-sm': 'var(--xd-shadow-sm)',
        'xd-md': 'var(--xd-shadow-md)',
        'xd-lg': 'var(--xd-shadow-lg)',
        'xd-xl': 'var(--xd-shadow-xl)',
      }},
      backgroundImage: {{
        'xd-gradient-action': 'var(--xd-gradient-action)',
        'xd-grin': 'var(--xd-gradient-grin)',
      }},
      transitionDuration: {{
        'xd-fast': 'var(--xd-duration-fast)',
        'xd-normal': 'var(--xd-duration-normal)',
        'xd-slow': 'var(--xd-duration-slow)',
        'xd-slower': 'var(--xd-duration-slower)',
      }},
      transitionTimingFunction: {{
        'xd-default': 'var(--xd-ease-default)',
        'xd-in-out': 'var(--xd-ease-in-out)',
        'xd-spring': 'var(--xd-ease-spring)',
      }},
      fontSize: {{
        'xd-xs': 'var(--xd-text-xs)',
        'xd-sm': 'var(--xd-text-sm)',
        'xd-base': 'var(--xd-text-base)',
        'xd-lg': 'var(--xd-text-lg)',
        'xd-xl': 'var(--xd-text-xl)',
        'xd-2xl': 'var(--xd-text-2xl)',
        'xd-3xl': 'var(--xd-text-3xl)',
        'xd-4xl': 'var(--xd-text-4xl)',
        'xd-5xl': 'var(--xd-text-5xl)',
      }},
      lineHeight: {{
        'xd-tight': 'var(--xd-leading-tight)',
        'xd-snug': 'var(--xd-leading-snug)',
        'xd-normal': 'var(--xd-leading-normal)',
        'xd-relaxed': 'var(--xd-leading-relaxed)',
        'xd-loose': 'var(--xd-leading-loose)',
      }},
      fontWeight: {{
        'xd-normal': 'var(--xd-font-normal)',
        'xd-medium': 'var(--xd-font-medium)',
        'xd-semibold': 'var(--xd-font-semibold)',
        'xd-bold': 'var(--xd-font-bold)',
        'xd-extrabold': 'var(--xd-font-extrabold)',
      }},
      letterSpacing: {{
        'xd-tight': 'var(--xd-tracking-tight)',
        'xd-snug': 'var(--xd-tracking-snug)',
        'xd-normal': 'var(--xd-tracking-normal)',
      }},
      zIndex: {{
        'xd-dropdown': 'var(--xd-z-dropdown)',
        'xd-sticky': 'var(--xd-z-sticky)',
        'xd-fixed': 'var(--xd-z-fixed)',
        'xd-overlay': 'var(--xd-z-overlay)',
        'xd-modal': 'var(--xd-z-modal)',
        'xd-popover': 'var(--xd-z-popover)',
        'xd-toast': 'var(--xd-z-toast)',
        'xd-tooltip': 'var(--xd-z-tooltip)',
      }},
    }},
  }},
}};

module.exports = xdfacePreset;
"""


def render_contrast(tok: dict) -> str:
    ink = tok["primitive"]["ink-900"]
    cream = tok["primitive"]["paper-50"]
    spines = [(name, spine["bg"], spine["fg"], contrast(spine["bg"], spine["fg"])) for name, spine in tok["spine"].items()]
    # fg4 is quaternary (placeholders). It is recorded, and it is allowed under 4.5.
    text_keys = ["fg", "fg2", "fg3", "link", "accent", "success", "warning", "error", "info", "xp", "streak", "badge"]
    rows = []
    for theme, values in tok["theme"].items():
        for key in text_keys:
            for surface in ("bg", "surface", "raised"):
                rows.append([theme, key, surface, values[key], values[surface], contrast(values[key], values[surface])])
        rows.append([theme, "actionFg", "action", values["actionFg"], values["action"], contrast(values["actionFg"], values["action"])])
        rows.append([
            theme,
            "actionFg",
            "actionHover",
            values["actionFg"],
            values["actionHover"],
            contrast(values["actionFg"], values["actionHover"]),
        ])
        rows.append([theme, "ink", "mustard", ink, values["mustard"], contrast(ink, values["mustard"])])
    bad = [row for row in rows if row[-1] < 4.5]
    fg4 = [
        [theme, surface, contrast(values["fg4"], values[surface])]
        for theme, values in tok["theme"].items()
        for surface in ("bg", "surface", "raised")
    ]
    logo = {}
    for theme, spec in tok["mark"].items():
        logo[theme] = [contrast(spec["green"], spec["bg"]), contrast(spec["orange"], spec["bg"])]
    report = {
        "spines": spines,
        "rows": rows,
        "bad": bad,
        "fg4": fg4,
        "logo": logo,
        "tile": {
            "dark tile vs bg": contrast(tok["mark"]["dark"]["bg"], tok["theme"]["dark"]["bg"]),
        },
    }
    if bad:
        print("CONTRAST failures (text below 4.5):", file=sys.stderr)
        for row in bad:
            print(" ", row, file=sys.stderr)
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_docs_bundle(css: str) -> str:
    extra = (ROOT / "web" / "src" / "styles" / "global.css").read_text(encoding="utf-8")
    banner = "/* Generated by build.py: tokens.css + web/src/styles/global.css. Do not edit. */\n"
    return banner + css + "\n" + extra


def outputs(tok: dict) -> dict[str, str]:
    css = render_css(tok)
    files = {
        "tokens.css": css,
        "tokens.ts": render_ts(tok),
        "tailwind.preset.js": render_preset(tok),
        "contrast.json": render_contrast(tok),
        "web/public/styles/global.css": render_docs_bundle(css),
    }
    files.update(logo_files(tok))
    return files


def write_outputs(files: dict[str, str]) -> None:
    for rel, text in files.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def check_outputs(files: dict[str, str]) -> int:
    stale = []
    for rel, text in files.items():
        path = ROOT / rel
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != text:
            stale.append(rel)
            diff = difflib.unified_diff(
                current.splitlines(keepends=True),
                text.splitlines(keepends=True),
                fromfile=f"{rel} (committed)",
                tofile=f"{rel} (generated)",
                n=1,
            )
            sys.stderr.writelines(list(diff)[:80])
            sys.stderr.write("\n")
    if stale:
        print("Generated files are out of date. Run python3 build.py and commit:", file=sys.stderr)
        for rel in stale:
            print(f"  {rel}", file=sys.stderr)
        return 1
    print(f"Generated files match tokens.json ({len(files)} files).")
    return 0


UTILITIES = r"""
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0ms !important;
    animation-duration: 0ms !important;
  }
}

.xd-card {
  background: var(--xd-surface);
  border: 1px solid var(--xd-bd);
  border-radius: var(--xd-radius-lg);
  box-shadow: var(--xd-shadow-paper-md);
}
.xd-card-hover {
  transition: transform var(--xd-duration-normal) var(--xd-ease-in-out), box-shadow var(--xd-duration-normal) var(--xd-ease-in-out);
  cursor: pointer;
}
.xd-card-hover:hover {
  transform: translateY(-2px);
  box-shadow: var(--xd-shadow-card-hover);
}
.xd-soft-card {
  background: var(--xd-base);
  border: 1px solid var(--xd-bd);
  border-radius: var(--xd-radius-2xl);
  box-shadow: var(--xd-soft-shadow-sm);
}
.xd-soft-focus:focus-visible { outline: none; box-shadow: var(--xd-focus-ring); }

.xd-btn-action {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 20px;
  border-radius: var(--xd-radius-full);
  border: 1.5px solid var(--xd-action);
  background: var(--xd-action);
  color: var(--xd-action-fg);
  font: 600 15px/20px var(--xd-font-sans);
  cursor: pointer;
  transition: transform var(--xd-duration-fast) var(--xd-ease-spring), background var(--xd-duration-fast) var(--xd-ease-default);
}
.xd-btn-action:hover { background: var(--xd-action-hover); transform: translateY(-2px) rotate(-1deg); }
.xd-btn-action:focus-visible,
.xd-soft-focus:focus-visible { outline: none; box-shadow: var(--xd-focus-ring); }
.xd-btn-action:disabled {
  background: var(--xd-raised);
  color: var(--xd-fg-3);
  border-style: dashed;
  border-color: var(--xd-bd-2);
  cursor: not-allowed;
  transform: none;
}
.xd-btn-sm { padding: 6px 12px; font-size: 12px; border-radius: var(--xd-radius-full); }
.xd-btn-lg { padding: 14px 28px; font-size: 16px; }
.xd-btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  background: transparent;
  color: var(--xd-link);
  border: 1.5px solid var(--xd-bd-2);
  border-radius: var(--xd-radius-full);
  font: 500 14px/20px var(--xd-font-sans);
  cursor: pointer;
}
.xd-btn-ghost:hover { background: color-mix(in srgb, var(--xd-link) 8%, transparent); }
.xd-btn-subtle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  background: color-mix(in srgb, var(--xd-action) 10%, transparent);
  color: var(--xd-link);
  border: 1px solid color-mix(in srgb, var(--xd-action) 20%, transparent);
  border-radius: var(--xd-radius-full);
  font: 500 14px/20px var(--xd-font-sans);
  cursor: pointer;
}
.xd-btn-danger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--xd-error);
  color: var(--xd-paper-50);
  border: none;
  border-radius: var(--xd-radius-full);
  font: 600 14px/20px var(--xd-font-sans);
  cursor: pointer;
}
.xd-btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  color: var(--xd-fg-2);
  background: var(--xd-raised);
  border: 1px solid var(--xd-bd);
  border-radius: var(--xd-radius-md);
  cursor: pointer;
}
.xd-btn-full { width: 100%; justify-content: center; }
.xd-btn-loading { opacity: 0.7; pointer-events: none; cursor: progress; }

.xd-grin-underline { background: var(--xd-gradient-grin) bottom / 100% 3px no-repeat; padding-bottom: 4px; }
.xd-gradient-text, .gradient-text {
  background: var(--xd-gradient-grin);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.xd-label { display: block; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--xd-fg-2); margin-bottom: 8px; }
.xd-input, .xd-select, .xd-textarea {
  display: block;
  width: 100%;
  font: 400 15px/1.5 var(--xd-font-sans);
  color: var(--xd-text);
  background: var(--xd-surface);
  border: 1.5px solid var(--xd-bd);
  border-radius: var(--xd-radius-md);
  padding: 12px 14px;
  outline: none;
}
.xd-input:focus, .xd-select:focus, .xd-textarea:focus { border-color: var(--xd-accent); box-shadow: var(--xd-focus-ring); }
.xd-input:disabled, .xd-select:disabled, .xd-textarea:disabled {
  background: var(--xd-raised);
  color: var(--xd-fg-3);
  border-style: dashed;
  border-color: var(--xd-bd-2);
  cursor: not-allowed;
}
.xd-input-error, .xd-input-error:focus { border-color: var(--xd-error) !important; box-shadow: 0 0 0 3px color-mix(in srgb, var(--xd-error) 18%, transparent) !important; }
.xd-helper { display: block; margin-top: 6px; font-size: 12px; color: var(--xd-text-muted); }
.xd-error-text { display: block; margin-top: 6px; font-size: 12px; font-weight: 600; color: var(--xd-error); }
.xd-textarea { min-height: 96px; resize: vertical; }

.xd-alert { display: flex; gap: 0.75rem; padding: 0.875rem 1rem; border-radius: var(--xd-radius-md); border: 1.5px solid; font-size: 0.875rem; }
.xd-alert-success { background: color-mix(in srgb, var(--xd-success) 10%, transparent); border-color: color-mix(in srgb, var(--xd-success) 35%, transparent); color: var(--xd-success); }
.xd-alert-warning { background: color-mix(in srgb, var(--xd-warning) 12%, transparent); border-color: color-mix(in srgb, var(--xd-warning) 35%, transparent); color: var(--xd-warning); }
.xd-alert-error { background: color-mix(in srgb, var(--xd-error) 10%, transparent); border-color: color-mix(in srgb, var(--xd-error) 35%, transparent); color: var(--xd-error); }
.xd-alert-info { background: color-mix(in srgb, var(--xd-info) 10%, transparent); border-color: color-mix(in srgb, var(--xd-info) 35%, transparent); color: var(--xd-info); }

.xd-badge { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: var(--xd-radius-full); font-size: 11px; font-weight: 600; }
.xd-badge-success { background: color-mix(in srgb, var(--xd-success) 12%, transparent); color: var(--xd-success); }
.xd-badge-warning { background: color-mix(in srgb, var(--xd-warning) 14%, transparent); color: var(--xd-warning); }
.xd-badge-error { background: color-mix(in srgb, var(--xd-error) 12%, transparent); color: var(--xd-error); }
.xd-badge-info { background: color-mix(in srgb, var(--xd-info) 12%, transparent); color: var(--xd-info); }

.xd-progress { width: 100%; height: 8px; background: var(--xd-paper-line); border-radius: var(--xd-radius-full); overflow: hidden; }
.xd-progress-bar { height: 100%; background: var(--xd-gradient-grin); border-radius: var(--xd-radius-full); }

.xd-tab-list { display: flex; gap: 0.25rem; border-bottom: 1.5px solid var(--xd-border); }
.xd-tab { padding: 0.5rem 1rem; font: 500 0.875rem/1.4 var(--xd-font-sans); color: var(--xd-text-muted); border: none; background: none; cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -1.5px; }
.xd-tab:hover { color: var(--xd-text); }
.xd-tab-active { color: var(--xd-link) !important; border-bottom-color: var(--xd-link) !important; }

[data-tooltip] { position: relative; }
[data-tooltip]::before {
  content: attr(data-tooltip);
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--xd-fg);
  color: var(--xd-bg);
  padding: 0.3rem 0.625rem;
  border-radius: var(--xd-radius-sm);
  font: 500 0.7rem/1.3 var(--xd-font-sans);
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  z-index: var(--xd-z-tooltip);
}
[data-tooltip]:hover::before { opacity: 1; }

@keyframes xd-shimmer {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
.xd-skeleton {
  border-radius: var(--xd-radius-sm);
  background: linear-gradient(90deg, var(--xd-surface) 25%, var(--xd-raised) 50%, var(--xd-surface) 75%);
  background-size: 800px 100%;
  animation: xd-shimmer 1.4s ease-in-out infinite;
}
.xd-overlay, .xd-backdrop {
  position: fixed;
  inset: 0;
  background: var(--xd-overlay-bg);
  z-index: var(--xd-z-overlay);
  display: flex;
  align-items: center;
  justify-content: center;
}
.xd-backdrop { backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
.xd-kbd {
  display: inline-flex;
  align-items: center;
  padding: 0.15rem 0.45rem;
  font: 500 0.7rem/1.4 var(--xd-font-mono);
  color: var(--xd-fg-2);
  background: var(--xd-surface);
  border: 1px solid var(--xd-bd);
  border-bottom-width: 2px;
  border-radius: var(--xd-radius-sm);
  box-shadow: var(--xd-shadow-xs);
}
.xd-prose { color: var(--xd-text); font-family: var(--xd-font-sans); font-size: var(--xd-text-base); line-height: var(--xd-leading-relaxed); max-width: 68ch; }
.xd-prose h1, .xd-prose h2, .xd-prose h3, .xd-prose h4 { font-family: var(--xd-font-display); line-height: var(--xd-leading-tight); color: var(--xd-text); }
.xd-prose a { color: var(--xd-link); }
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate token artifacts from tokens.json")
    parser.add_argument("--check", action="store_true", help="Fail if generated files differ")
    args = parser.parse_args()
    files = outputs(load_tokens())
    removed = ("--xd-dark-", "--xd-gradient-dark-chrome", "--xd-blue-")
    css = files["tokens.css"]
    leaked = [name for name in removed if name in css]
    if leaked:
        print("Generator emitted removed variables:", ", ".join(leaked), file=sys.stderr)
        return 1
    if args.check:
        return check_outputs(files)
    write_outputs(files)
    print(f"Wrote {len(files)} files from tokens.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
