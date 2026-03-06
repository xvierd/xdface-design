/**
 * xdface Design System -- TypeScript tokens
 * Generated from tokens.json -- edit tokens.json, not this file
 * Usage: import { tokens } from 'path/to/tokens'
 */

export const tokens = {
  gradient: {
    action:      'linear-gradient(135deg, #16A34A 0%, #EA580C 100%)',
    actionHover: 'linear-gradient(135deg, #15803D 0%, #C2410C 100%)',
    darkChrome:  'linear-gradient(180deg, #0F0F1A 0%, #13132A 60%, #0D0D18 100%)',
    topAccent:   'linear-gradient(to right, #16A34A, #EA580C)',
  },
  color: {
    action:      '#16A34A',
    actionEnd:   '#EA580C',
    actionHover: '#15803D',
    xp:          '#F59E0B',
    streak:      '#EF4444',
    badge:       '#8B5CF6',
    dark950:     '#0D0D12',
    dark900:     '#0F0F1A',
    dark800:     '#13131A',
    dark700:     '#1A1A24',
    dark600:     '#1A1A2E',
    // Semantic state colors
    error:   '#EF4444',
    warning: '#F59E0B',
    info:    '#3B82F6',
    success: '#16A34A',
  },
  theme: {
    light: {
      bg:         '#F8F8FA',
      surface:    '#FFFFFF',
      surface2:   '#F2F2F5',
      border:     'rgba(0,0,0,0.08)',
      text:       '#111118',
      textMuted:  '#707080',
    },
    dark: {
      bg:         '#0D0D12',
      surface:    '#13131A',
      surface2:   '#1A1A24',
      border:     'rgba(255,255,255,0.07)',
      text:       '#E8E8F0',
      textMuted:  '#9898A8',
    },
  },
  font: {
    sans: "'Inter', system-ui, -apple-system, sans-serif",
    mono: "'JetBrains Mono', 'Fira Code', monospace",
  },
  radius: {
    sm:   '8px',
    md:   '12px',
    lg:   '16px',
    xl:   '20px',
    full: '9999px',
  },
  spacing: {
    space1: '4px',
    space2: '8px',
    space3: '12px',
    space4: '16px',
    space5: '24px',
    space6: '32px',
    space7: '48px',
    space8: '64px',
    space9: '96px',
  },
  shadow: {
    actionSm:   '0 4px 16px rgba(22, 163, 74, 0.25)',
    actionMd:   '0 6px 24px rgba(22, 163, 74, 0.35)',
    actionGlow: '0 0 32px rgba(22, 163, 74, 0.4)',
  },
} as const;

export type Tokens = typeof tokens;
