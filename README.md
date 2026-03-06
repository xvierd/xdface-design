# xdface Design System

Source of truth for colors, typography, spacing, and visual identity across all xdface apps.

## Files

| File | Purpose | Consumers |
|------|---------|-----------|
| `tokens.json` | Canonical token definitions | Humans (edit this first) |
| `tokens.css` | CSS custom properties (`--xd-*`) | All apps via `@import` |
| `tokens.ts` | TypeScript constants | Vault (React), any TS code |
| `logo/` | Logo SVGs, favicon specs | All apps |

## Design Philosophy

The xdface brand is built on a **green-to-orange gradient** (`#16A34A` to `#EA580C`) used as the primary action color across all apps. This gradient appears on buttons, the top accent bar, and the logo glow effect.

Navigation and chrome surfaces use a **dark gradient** (`#0F0F1A` to `#0D0D18`) that provides depth without competing with content.

Gamification elements have dedicated colors: amber for XP, red for streaks, purple for badges.

## Token Naming

All CSS custom properties use the `--xd-` prefix to avoid conflicts with Tailwind or other frameworks:

- `--xd-action` -- primary action color (green)
- `--xd-gradient-action` -- the signature green-to-orange gradient
- `--xd-bg`, `--xd-surface`, `--xd-text` -- theme-aware tokens that flip in dark mode
- `--xd-radius-*` -- border radius scale
- `--xd-shadow-action-*` -- green-tinted shadows for action elements

## How Each App Consumes Tokens

**Vault** (React + Tailwind 4): imports both `tokens.css` (for CSS variables) and `tokens.ts` (for inline styles and JS logic).

**Site** (Astro + Tailwind 3): imports `tokens.css` and references `--xd-*` variables in component styles.

**Library** (Astro + Tailwind 4): imports `tokens.css` and references `--xd-*` variables in component styles.

## Dark Mode

Theme-aware tokens (`--xd-bg`, `--xd-surface`, `--xd-text`, etc.) automatically switch values when any of these selectors are present on `<html>`:

- `.xd-dark`
- `[data-theme="dark"]`
- `[data-xd-theme="dark"]`

Each app can use whichever selector fits its existing theme toggle mechanism.

## Adding a New Token

1. Add the value to `tokens.json` in the appropriate section
2. Add the corresponding `--xd-*` variable to `tokens.css`
3. Add the corresponding property to `tokens.ts`
4. Update consuming apps as needed

## Logo & Brand Identity

The xdface logo features:
- **Two X eyes** — representing "xd" (x'd out) + "face"
- **Asymmetric grin** — tilted 3° for attitude
- **Green-to-orange gradient** — signature brand colors

### Variants

| Variant | File | Background |
|---------|------|------------|
| Light | `logo/logo.svg` | White `#FFFFFF` |
| Dark | `logo/logo-dark.svg` | Dark `#13131A` |

### Logo Specs

- **Dimensions**: 128×128 viewBox
- **Corner Radius**: 28px (22%)
- **Border**: 2px subtle stroke

**Colors (Light):**
- Left X: `#16A34A` (green)
- Right X: `#EA580C` (orange)
- Grin: `linear-gradient(135deg, #16A34A, #EA580C)`

**Colors (Dark):**
- Left X: `#4ADE80` (bright green)
- Right X: `#FB923C` (bright orange)
- Grin: Same gradient

See `logo/README.md` for full specs and export sizes.

## Current Adoption Status

| App | Status | Notes |
|-----|--------|-------|
| Vault | Adopted | Already uses green/orange brand; will import tokens directly |
| Site | **Adopted** | Migrated to design system |
| Library | Pending | Hardcoded `#2563EB` throughout; needs migration |
