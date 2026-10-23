# xdface Design System

Source of truth for colors, typography, spacing, surfaces, and visual identity across all xdface apps.

**Package:** `@xdface/tokens` · **v0.4.0**

## Files

| File | Purpose | Consumers |
|------|---------|-----------|
| `tokens.json` | Canonical token definitions | Humans (edit this, then `python3 build.py`) |
| `tokens.css` | Generated CSS custom properties (`--xd-*`) + utilities | All apps via `@import '@xdface/tokens/css'` |
| `notepad.css` | Generated, minimal Notepad appearance adapter | Vendored in `notepad/src/theme-tokens.css`; package export `@xdface/tokens/notepad` |
| `tokens.ts` | Generated TypeScript constants and `setTheme()` | Vault (React), any TS code |
| `tailwind.preset.js` | Generated Tailwind theme mapping | Tailwind v3/v4 apps |
| `contrast.json` | Generated contrast report | Reviewers |
| `logo/` | Generated logo SVGs and favicons | All apps |

## Design Philosophy

The design system shares Notepad's quiet surfaces and typography. **Light · Mono** is white, black, and neutral gray; the transparent xdface mark keeps its green and orange. **Light · Color** uses pure white backgrounds and surfaces, with xdface color reserved for interface elements. Borders and shadows stay neutral. Primary buttons use solid `--xd-action` with `--xd-action-fg`. UI gradients, book spines, highlights, and status colors become neutral in Mono. Use semantic CSS variables for theme-aware UI; raw primitive colors and `tokens.gradient` remain brand references.

Apps paint UI with an **elevation surface scale** (not only flat bg/surface):

```
--xd-deep     page background
--xd-base     cards / primary surfaces
--xd-raised   elevated panels
--xd-chrome   header / sidebar
--xd-fg … --xd-fg-4   text hierarchy
--xd-bd / --xd-bd-2   border hierarchy
--xd-soft-shadow-*    layered brand-tinted shadows
```

Backward-compatible aliases: `--xds-deep`, `--xds-base`, `--xds-fg`, etc. map to the same values.

Gamification: amber XP, red streaks, purple badges.

## Themes

Theme-aware tokens flip when any of these are on `<html>` (or an ancestor):

Set one attribute:

```html
<html data-xd-theme="light">
```

`setTheme('light-mono' | 'light' | 'dark' | 'sepia' | 'auto')` writes that attribute. `auto` follows `prefers-color-scheme`. `light` uses white surfaces with colored elements and remains the package default. The showcase starts in `light-mono` and remembers an explicit choice.

Legacy selectors still match in 0.3 and go away in 2.0:

| Theme | Selectors |
|-------|-----------|
| **Light** | `:root`, `[data-xd-theme="light"]`, `[data-theme="light"]`, `[data-lib-theme="light"]` |
| **Light · Mono** | `[data-xd-theme="light-mono"]`, `[data-theme="light-mono"]`, `[data-lib-theme="light-mono"]` |
| **Dark** | `[data-xd-theme="dark"]`, `.xd-dark`, `.dark`, `[data-theme="dark"]`, `[data-lib-theme="dark"]` |
| **Sepia** | `[data-xd-theme="sepia"]`, `[data-theme="sepia"]`, `[data-lib-theme="sepia"]` |

Tailwind 4 (the preset already sets the v3 `darkMode` variant to the same list):

```css
@custom-variant dark (&:where([data-xd-theme=dark], [data-xd-theme=dark] *, .dark, .dark *, .xd-dark, .xd-dark *, [data-theme=dark], [data-theme=dark] *, [data-lib-theme=dark], [data-lib-theme=dark] *));
```

| App | How theme is set |
|-----|------------------|
| Vault | move from `.dark` to `data-xd-theme` |
| Library | `data-lib-theme` still works; prefer `data-xd-theme` |
| Site / design.xdface.net | `data-xd-theme` |
| Notepad | `data-theme="light"` → Mono; `light-color` → Color; existing `dark` remains local monochrome. `data-xd-theme` reflects the canonical theme. |

## Token naming

- `--xd-action` — solid brand green (icons, text, links)
- `--xd-gradient-action` — CTA gradient (buttons, progress)
- `--xd-gradient-action-hover` — darker gradient on hover
- `--xd-bg`, `--xd-surface`, `--xd-text` — flat theme tokens
- `--xd-deep` … `--xd-chrome` — elevation scale (preferred for apps)

## How each app consumes tokens

```css
@import '@xdface/tokens/css';
```

**Vault** (React + Tailwind 4): CSS variables + `tokens.ts` + Tailwind `@theme` mapping.

**Library** (Astro + Tailwind 4): CSS variables + soft-UI components; product tokens (highlights, pagefind) stay local.

**Site** (Astro): CSS variables in component styles.

## Adding a new token

1. Add the value to `tokens.json`
2. Run `python3 build.py` (or `make tokens`)
3. Commit the generated files. CI runs `python3 build.py --check` and fails if they are stale
4. Bump version in `package.json` and update `CHANGELOG.md`

After changing Notepad colors, run `npm --prefix ../notepad run design:sync` and commit its generated `src/theme-tokens.css`. Notepad builds independently from this repository. Run `python3 -m unittest discover -s tests` to verify AA contrast and the monochrome palette.

## Logo & brand

- **Two X eyes** + asymmetric grin (3°)
- `logo.svg` (white tile), `logo-dark.svg` (forest tile `#1F2B23`), `logo-sepia.svg`
- Transparent marks and thick-stroke favicons, including 16px
- Colors come from `tokens.json` → `mark`. See `logo/README.md`

## Adoption status

| App | Status | Notes |
|-----|--------|-------|
| Vault | Adopted | Surfaces via package; lesson-prose + ambient wash stay app-local |
| Library | Adopted | Surfaces + soft shadows from package; highlights/pagefind local |
| Site | Adopted | Brand tokens |
| Study notebook | Partial | Align when convenient |

## Utilities (tokens.css)

Buttons: `.xd-btn-action`, `.xd-btn-ghost`, `.xd-btn-subtle`, `.xd-btn-danger`, sizes  
Forms: `.xd-input`, `.xd-label`, `.xd-toggle`  
Surfaces: `.xd-card`, `.xd-soft-card`, `.xd-skeleton`  
Content: `.xd-prose`, `.xd-gradient-text`, `.xd-ambient`  
Feedback: `.xd-alert-*`, `.xd-badge-*`, `.xd-progress`
