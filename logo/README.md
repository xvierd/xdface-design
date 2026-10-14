# xdface Logo

Generated from `tokens.json` (`mark`) by `build.py`. Do not edit the SVGs by hand.

The mark is two X eyes and a grin rotated −3°, green into orange.

## Files

| File | Tile | Use |
|------|------|-----|
| `logo.svg` | White `#FFFFFF`, border `#E5E7EB` | Light surfaces |
| `logo-dark.svg` | Forest `#1F2B23`, border `#F6EFE21F` | Dark surfaces. Not a copy of the light logo. |
| `logo-sepia.svg` | Sepia `#FAF3E3`, border `#DCC9A6` | Reading theme |
| `logo-mark-transparent-light.svg` | none | Light ink on a photo or pattern |
| `logo-mark-transparent-dark.svg` | none | Bright ink on forest |
| `favicon.svg` / `favicon-dark.svg` | tiled, heavier strokes | Browser icon |
| `favicon-16.svg` / `favicon-16-dark.svg` | same art at 16×16 | Small tab icon |

ViewBox is `0 0 128 128`. Tile radius is 28.

## Favicon links

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml" media="(prefers-color-scheme: light)" />
<link rel="icon" href="/favicon-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)" />
```

Sepia is an app theme, not an OS color scheme, so the favicon stays on `prefers-color-scheme`. Swap the in-page mark with `data-xd-theme` instead.

The docs site copies these files into `web/public/` when `build.py` runs.
