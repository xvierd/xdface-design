# Changelog

All notable changes to `@xdface/tokens` are documented here.

## [0.2.0] — 2026-07-30

### Added
- **App surface elevation scale** — `--xd-deep`, `--xd-base`, `--xd-raised`, `--xd-chrome`
- **Text hierarchy** — `--xd-fg` … `--xd-fg-4`, borders `--xd-bd` / `--xd-bd-2`, glass `--xd-gl`
- **Soft elevation shadows** — `--xd-soft-shadow-sm|md|lg`, `--xd-soft-ring`
- **Sidebar tokens** — `--xd-sidebar-bg`, `--xd-sidebar-sep`
- **Sepia reading theme** — `[data-theme="sepia"]`, `[data-lib-theme="sepia"]`
- **Highlight palette** — `--xd-hl-*` for annotation/marks
- **`--xd-gradient-action-hover`** for CTA hover states
- **`.xd-soft-card`**, **`.xd-soft-focus`**, **`.xd-ambient`** utilities
- **Backward-compat aliases** — `--xds-*` maps to surface scale (vault + library)
- Dark selector coverage: `.dark`, `[data-lib-theme="dark"]`, etc.
- `prefers-reduced-motion` on animated utilities
- Blue primitives `--xd-blue-400` / `--xd-blue-500` in CSS
- Corrected `--xd-green-700` to `#166534`

### Changed
- Light theme is now **green-tinted brand** (`#edf2ee` deep, green borders) matching vault/library products
- Flat `--xd-bg` / `--xd-surface` / `--xd-text` aligned with the new light brand
- Tailwind preset gradients use CSS vars instead of hard-coded hex
- Package version **0.2.0**

### Migration
Apps should remove local redefinitions of `--xds-*` and soft shadows; import `@xdface/tokens/css` only. Keep product-only tokens (pagefind, local highlight class names if needed).

## [0.1.0] — 2026-03-06

### Added

**Token categories**
- `motion` — duration (fast/normal/slow/slower) and easing (default/in-out/spring) tokens
- `z-index` — semantic z-index scale (dropdown → tooltip, values 10–100)
- `interaction` — focus-ring, overlay-bg, disabled-opacity
- Typography scale — `--xd-text-xs` through `--xd-text-5xl` (size), `--xd-leading-*` (line heights), `--xd-font-*` (weights), `--xd-tracking-*` (letter spacing)
- Neutral shadow scale — `--xd-shadow-xs` through `--xd-shadow-xl` (rgba black)
- `--xd-shadow-card-hover` — theme-aware card hover shadow (light: 0.08 opacity, dark: 0.3 opacity)

**Utility components (tokens.css)**
- `.xd-skeleton` + `@keyframes xd-shimmer` — shimmer loading placeholder
- `.xd-card` / `.xd-card-hover` — surface card with border, radius-lg, hover lift
- `.xd-overlay` / `.xd-backdrop` — fixed inset overlay + backdrop-filter blur
- `.xd-prose` — content typography (headings, paragraphs, lists, code, blockquotes, tables)
- `.xd-divider` — 1px border-color separator
- `.xd-kbd` — keyboard shortcut badge (mono font, subtle border/shadow)
- `.xd-gradient-text` — gradient text utility (moved to shared tokens.css)
- `.xd-fadeSlideUp` — entrance animation

**Tailwind preset (`tailwind.preset.js`)**
- Added `transitionDuration`, `transitionTimingFunction` extensions
- Added `fontSize`, `lineHeight`, `fontWeight`, `letterSpacing` extensions
- Added `zIndex` extensions
- Added neutral `boxShadow` entries (`xd-xs` through `xd-xl`, `xd-card-hover`)
- Added theme-aware color tokens (`xd.bg`, `xd.surface`, `xd.surface-2`, `xd.border`, `xd.text`, `xd.text-muted`)
- Colors now reference `var(--xd-*)` CSS custom properties

**Showcase site (design.xdface.net)**
- Fixed CSS drift: `global.css` now imports `tokens.css` instead of inlining token values
- Added sections: Motion, Typography Scale, Cards, Skeleton, Overlay, Keyboard Shortcuts
- Click-to-copy on all token pills

## [0.0.12] — 2026-03-05

### Added
- Initial design system release
- Brand palette: action green (#16A34A) → orange (#EA580C) gradient
- Semantic tokens: xp, streak, badge, error, warning, info, success
- Typography: Inter (sans) + JetBrains Mono (mono)
- Spacing scale (space-1 through space-9)
- Border radius scale (sm/md/lg/xl/full)
- Action shadows (action-sm, action-md, action-glow)
- Light/dark theme tokens
- Utility classes: `.xd-btn-action`, `.xd-btn-ghost`, `.xd-btn-subtle`, `.xd-btn-danger`, `.xd-btn-icon`
- Form components: `.xd-input`, `.xd-select`, `.xd-textarea`, `.xd-checkbox`, `.xd-toggle`
- Alerts, badges, progress bar, tabs, tooltip
- Tailwind preset (`tailwind.preset.js`)
- TypeScript constants (`tokens.ts`)
- Showcase site (design.xdface.net)
