# xdface Logo & Brand Assets

Source of truth for the xdface logo, favicon, and brand identity.

## Logo

The xdface logo features a stylized face with:
- **Two X eyes** — representing the "xd" (x'd out eyes) + "face"
- **Asymmetric grin** — tilted 3° for attitude
- **Green-to-orange gradient** — the signature brand colors

### Variants

| Variant | File | Background | Use Case |
|---------|------|------------|----------|
| Light | `logo.svg` | White `#FFFFFF` | Light mode, print |
| Dark | `logo-dark.svg` | Dark `#13131A` | Dark mode, dark backgrounds |

### Dimensions

- **ViewBox**: `0 0 128 128`
- **Corner Radius**: `28px` (22% of size)
- **Border**: `2px` stroke, subtle

### Color Specs

#### Light Variant
| Element | Color | Token |
|---------|-------|-------|
| Background | `#FFFFFF` | `--xd-surface` (light) |
| Border | `#E5E7EB` | subtle gray |
| Left X | `#16A34A` | `--xd-action` |
| Right X | `#EA580C` | `--xd-action-end` |
| Grin | Gradient | `--xd-gradient-action` |

#### Dark Variant
| Element | Color | Token |
|---------|-------|-------|
| Background | `#13131A` | `--xd-surface` (dark) |
| Border | `rgba(255,255,255,0.1)` | subtle white |
| Left X | `#4ADE80` | `--xd-green-400` (bright) |
| Right X | `#FB923C` | `--xd-orange-400` (bright) |
| Grin | Gradient | `--xd-gradient-action` |

## Favicon

The logo files ARE the favicons. Use them directly:

| File | Use As | Purpose |
|------|--------|---------|
| `logo.svg` | `favicon.svg` | Light mode favicon |
| `logo-dark.svg` | `favicon-dark.svg` | Dark mode favicon |

### Usage in Apps

```html
<!-- Light mode -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />

<!-- Dark mode (switch with JS/CSS) -->
<img src="/favicon.svg" class="dark:hidden" />
<img src="/favicon-dark.svg" class="hidden dark:block" />
```

## Export Sizes

When exporting from the SVGs:

| Size | Use Case |
|------|----------|
| 32×32 | Browser favicon |
| 192×192 | PWA icon, Android |
| 512×512 | PWA maskable |

## Copy to Apps

The logo files are used as favicons in apps (just rename/copy):

```bash
# Site
cp logo.svg ../site/web/public/favicon.svg
cp logo-dark.svg ../site/web/public/favicon-dark.svg

# Vault
cp logo.svg ../xdface-vault/web/public/favicon.svg
cp logo-dark.svg ../xdface-vault/web/public/favicon-dark.svg
```

**Note:** `logo.svg` → `favicon.svg` (same file, different name in apps)
