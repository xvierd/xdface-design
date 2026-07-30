/**
 * xdface Design System — Tailwind CSS Preset
 *
 * Maps all --xd-* tokens to Tailwind theme extensions.
 * Compatible with Tailwind v3 and v4.
 *
 * Usage:
 *   // tailwind.config.js
 *   const xdfacePreset = require('@xdface/tokens/tailwind');
 *   module.exports = { presets: [xdfacePreset], ... };
 */

/** @type {import('tailwindcss').Config} */
const xdfacePreset = {
  theme: {
    extend: {
      // ── Colors ──────────────────────────────────────────
      colors: {
        xd: {
          // Brand
          action:         'var(--xd-action)',
          'action-end':   'var(--xd-action-end)',
          'action-hover': 'var(--xd-action-hover)',
          // Gamification
          xp:     'var(--xd-xp)',
          streak: 'var(--xd-streak)',
          badge:  'var(--xd-badge)',
          // Semantic states
          error:   'var(--xd-error)',
          warning: 'var(--xd-warning)',
          info:    'var(--xd-info)',
          success: 'var(--xd-success)',
          // Primitives
          'green-400':  'var(--xd-green-400)',
          'green-500':  'var(--xd-green-500)',
          'green-600':  'var(--xd-green-600)',
          'green-700':  'var(--xd-green-700)',
          'orange-400': 'var(--xd-orange-400)',
          'orange-500': 'var(--xd-orange-500)',
          'orange-600': 'var(--xd-orange-600)',
          'blue-400':   'var(--xd-blue-400)',
          'blue-500':   'var(--xd-blue-500)',
          // Dark backgrounds
          'dark-950': 'var(--xd-dark-950)',
          'dark-900': 'var(--xd-dark-900)',
          'dark-800': 'var(--xd-dark-800)',
          'dark-700': 'var(--xd-dark-700)',
          'dark-600': 'var(--xd-dark-600)',
          // Flat theme-aware
          bg:           'var(--xd-bg)',
          surface:      'var(--xd-surface)',
          'surface-2':  'var(--xd-surface-2)',
          border:       'var(--xd-border)',
          text:         'var(--xd-text)',
          'text-muted': 'var(--xd-text-muted)',
          // App surface elevation
          deep:    'var(--xd-deep)',
          base:    'var(--xd-base)',
          raised:  'var(--xd-raised)',
          chrome:  'var(--xd-chrome)',
          fg:      'var(--xd-fg)',
          'fg-2':  'var(--xd-fg-2)',
          'fg-3':  'var(--xd-fg-3)',
          'fg-4':  'var(--xd-fg-4)',
          bd:      'var(--xd-bd)',
          'bd-2':  'var(--xd-bd-2)',
          gl:      'var(--xd-gl)',
        },
      },

      // ── Background images (gradients) ───────────────────
      backgroundImage: {
        'xd-action':       'var(--xd-gradient-action)',
        'xd-action-hover': 'var(--xd-gradient-action-hover)',
        'xd-dark-chrome':  'var(--xd-gradient-dark-chrome)',
        'xd-top-accent':   'var(--xd-gradient-top-accent)',
        'xd-sidebar':      'var(--xd-sidebar-bg)',
      },

      // ── Font families ────────────────────────────────────
      fontFamily: {
        sans: ["'Inter'", 'system-ui', '-apple-system', 'sans-serif'],
        mono: ["'JetBrains Mono'", "'Fira Code'", 'monospace'],
      },

      // ── Border radius ────────────────────────────────────
      borderRadius: {
        'xd-sm':   'var(--xd-radius-sm)',
        'xd-md':   'var(--xd-radius-md)',
        'xd-lg':   'var(--xd-radius-lg)',
        'xd-xl':   'var(--xd-radius-xl)',
        'xd-2xl':  'var(--xd-radius-2xl)',
        'xd-full': 'var(--xd-radius-full)',
      },

      // ── Spacing ──────────────────────────────────────────
      spacing: {
        'xd-1': 'var(--xd-space-1)',
        'xd-2': 'var(--xd-space-2)',
        'xd-3': 'var(--xd-space-3)',
        'xd-4': 'var(--xd-space-4)',
        'xd-5': 'var(--xd-space-5)',
        'xd-6': 'var(--xd-space-6)',
        'xd-7': 'var(--xd-space-7)',
        'xd-8': 'var(--xd-space-8)',
        'xd-9': 'var(--xd-space-9)',
      },

      // ── Box shadow ───────────────────────────────────────
      boxShadow: {
        'xd-action-sm':   'var(--xd-shadow-action-sm)',
        'xd-action-md':   'var(--xd-shadow-action-md)',
        'xd-action-glow': 'var(--xd-shadow-action-glow)',
        'xd-error':       '0 0 0 3px rgba(239, 68, 68, 0.15)',
        'xd-focus':       'var(--xd-focus-ring)',
        'xd-soft-sm':     'var(--xd-soft-shadow-sm)',
        'xd-soft-md':     'var(--xd-soft-shadow-md)',
        'xd-soft-lg':     'var(--xd-soft-shadow-lg)',
        'xd-soft-ring':   'var(--xd-soft-ring)',
        'xd-xs':          'var(--xd-shadow-xs)',
        'xd-sm':          'var(--xd-shadow-sm)',
        'xd-md':          'var(--xd-shadow-md)',
        'xd-lg':          'var(--xd-shadow-lg)',
        'xd-xl':          'var(--xd-shadow-xl)',
        'xd-card-hover':  'var(--xd-shadow-card-hover)',
      },

      // ── Transition duration ──────────────────────────────
      transitionDuration: {
        'xd-fast':   'var(--xd-duration-fast)',
        'xd-normal': 'var(--xd-duration-normal)',
        'xd-slow':   'var(--xd-duration-slow)',
        'xd-slower': 'var(--xd-duration-slower)',
      },

      // ── Transition timing ────────────────────────────────
      transitionTimingFunction: {
        'xd-default': 'var(--xd-ease-default)',
        'xd-in-out':  'var(--xd-ease-in-out)',
        'xd-spring':  'var(--xd-ease-spring)',
      },

      // ── Font size ────────────────────────────────────────
      fontSize: {
        'xd-xs':   ['var(--xd-text-xs)',   { lineHeight: 'var(--xd-leading-normal)' }],
        'xd-sm':   ['var(--xd-text-sm)',   { lineHeight: 'var(--xd-leading-normal)' }],
        'xd-base': ['var(--xd-text-base)', { lineHeight: 'var(--xd-leading-relaxed)' }],
        'xd-lg':   ['var(--xd-text-lg)',   { lineHeight: 'var(--xd-leading-relaxed)' }],
        'xd-xl':   ['var(--xd-text-xl)',   { lineHeight: 'var(--xd-leading-snug)' }],
        'xd-2xl':  ['var(--xd-text-2xl)',  { lineHeight: 'var(--xd-leading-snug)' }],
        'xd-3xl':  ['var(--xd-text-3xl)',  { lineHeight: 'var(--xd-leading-tight)' }],
        'xd-4xl':  ['var(--xd-text-4xl)',  { lineHeight: 'var(--xd-leading-tight)' }],
        'xd-5xl':  ['var(--xd-text-5xl)',  { lineHeight: 'var(--xd-leading-tight)' }],
      },

      // ── Line height ──────────────────────────────────────
      lineHeight: {
        'xd-tight':   'var(--xd-leading-tight)',
        'xd-snug':    'var(--xd-leading-snug)',
        'xd-normal':  'var(--xd-leading-normal)',
        'xd-relaxed': 'var(--xd-leading-relaxed)',
        'xd-loose':   'var(--xd-leading-loose)',
      },

      // ── Font weight ──────────────────────────────────────
      fontWeight: {
        'xd-normal':    'var(--xd-font-normal)',
        'xd-medium':    'var(--xd-font-medium)',
        'xd-semibold':  'var(--xd-font-semibold)',
        'xd-bold':      'var(--xd-font-bold)',
        'xd-extrabold': 'var(--xd-font-extrabold)',
      },

      // ── Letter spacing ───────────────────────────────────
      letterSpacing: {
        'xd-tight':  'var(--xd-tracking-tight)',
        'xd-snug':   'var(--xd-tracking-snug)',
        'xd-normal': 'var(--xd-tracking-normal)',
      },

      // ── Z-index ──────────────────────────────────────────
      zIndex: {
        'xd-dropdown': 'var(--xd-z-dropdown)',
        'xd-sticky':   'var(--xd-z-sticky)',
        'xd-fixed':    'var(--xd-z-fixed)',
        'xd-overlay':  'var(--xd-z-overlay)',
        'xd-modal':    'var(--xd-z-modal)',
        'xd-popover':  'var(--xd-z-popover)',
        'xd-toast':    'var(--xd-z-toast)',
        'xd-tooltip':  'var(--xd-z-tooltip)',
      },
    },
  },
};

module.exports = xdfacePreset;
