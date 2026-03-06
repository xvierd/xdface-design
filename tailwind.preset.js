/**
 * xdface Design System — Tailwind CSS Preset
 *
 * Maps all --xd-* tokens to Tailwind theme extensions.
 * Compatible with Tailwind v3 and v4.
 *
 * Usage:
 *   // tailwind.config.js
 *   const xdfacePreset = require('./tailwind.preset.js');
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
          action:       '#16A34A',
          'action-end': '#EA580C',
          'action-hover': '#15803D',
          // Gamification
          xp:     '#F59E0B',
          streak: '#EF4444',
          badge:  '#8B5CF6',
          // Semantic states
          error:   '#EF4444',
          warning: '#F59E0B',
          info:    '#3B82F6',
          success: '#16A34A',
          // Primitives
          'green-400': '#4ade80',
          'green-500': '#16A34A',
          'green-600': '#15803D',
          'orange-400': '#fb923c',
          'orange-500': '#EA580C',
          'orange-600': '#C2410C',
          'blue-400':  '#60A5FA',
          'blue-500':  '#3B82F6',
          // Dark backgrounds
          'dark-950': '#0D0D12',
          'dark-900': '#0F0F1A',
          'dark-800': '#13131A',
          'dark-700': '#1A1A24',
          'dark-600': '#1A1A2E',
        },
      },

      // ── Background images (gradients) ───────────────────
      backgroundImage: {
        'xd-action':       'linear-gradient(135deg, #16A34A 0%, #EA580C 100%)',
        'xd-action-hover': 'linear-gradient(135deg, #15803D 0%, #C2410C 100%)',
        'xd-dark-chrome':  'linear-gradient(180deg, #0F0F1A 0%, #13132A 60%, #0D0D18 100%)',
        'xd-top-accent':   'linear-gradient(to right, #16A34A, #EA580C)',
      },

      // ── Font families ────────────────────────────────────
      fontFamily: {
        sans: ["'Inter'", 'system-ui', '-apple-system', 'sans-serif'],
        mono: ["'JetBrains Mono'", "'Fira Code'", 'monospace'],
      },

      // ── Border radius ────────────────────────────────────
      borderRadius: {
        'xd-sm':   '8px',
        'xd-md':   '12px',
        'xd-lg':   '16px',
        'xd-xl':   '20px',
        'xd-full': '9999px',
      },

      // ── Spacing ──────────────────────────────────────────
      spacing: {
        'xd-1': '4px',
        'xd-2': '8px',
        'xd-3': '12px',
        'xd-4': '16px',
        'xd-5': '24px',
        'xd-6': '32px',
        'xd-7': '48px',
        'xd-8': '64px',
        'xd-9': '96px',
      },

      // ── Box shadow ───────────────────────────────────────
      boxShadow: {
        'xd-action-sm':   '0 4px 16px rgba(22, 163, 74, 0.25)',
        'xd-action-md':   '0 6px 24px rgba(22, 163, 74, 0.35)',
        'xd-action-glow': '0 0 32px rgba(22, 163, 74, 0.4)',
        'xd-error':       '0 0 0 3px rgba(239, 68, 68, 0.15)',
        'xd-focus':       '0 0 0 3px rgba(22, 163, 74, 0.15)',
      },
    },
  },
};

module.exports = xdfacePreset;
