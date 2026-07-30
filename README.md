# xdface Design System

Source of truth for colors, typography, spacing, surfaces, and visual identity across all xdface apps.

**Package:** `@xdface/tokens` · **v0.2.0**

## Files

| File | Purpose | Consumers |
|------|---------|-----------|
| `tokens.json` | Canonical token definitions | Humans (edit this first) |
| `tokens.css` | CSS custom properties (`--xd-*`) + utilities | All apps via `@import '@xdface/tokens/css'` |
| `tokens.ts` | TypeScript constants | Vault (React), any TS code |
| `tailwind.preset.js` | Tailwind theme mapping | Tailwind v3/v4 apps |
| `logo/` | Logo SVGs, favicon specs | All apps |

## Design Philosophy

The xdface brand is built on a **green-to-orange gradient** (`#16A34A` → `#EA580C`) for primary actions. Navigation and chrome use elevated surfaces with a dark chrome gradient when needed.

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

| Theme | Selectors |
|-------|-----------|
| **Light** (default / brand green-tint) | `:root`, `[data-lib-theme="light"]` |
| **Dark** | `.xd-dark`, `.dark`, `[data-theme="dark"]`, `[data-xd-theme="dark"]`, `[data-lib-theme="dark"]` |
| **Sepia** (reading) | `[data-theme="sepia"]`, `[data-xd-theme="sepia"]`, `[data-lib-theme="sepia"]` |

| App | How theme is set |
|-----|------------------|
| Vault | `.dark` class on `<html>` |
| Library | `data-lib-theme="dark\|light\|sepia"` |
| Site / design.xdface.net | `data-theme` / `.xd-dark` |

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
2. Add the corresponding `--xd-*` variable to `tokens.css`
3. Add the corresponding property to `tokens.ts`
4. Extend `tailwind.preset.js` if needed
5. Bump version in `package.json` and update `CHANGELOG.md`

## Logo & brand

- **Two X eyes** + asymmetric grin (3°)
- Light / dark SVG variants in `logo/`
- See `logo/README.md` for export sizes

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
