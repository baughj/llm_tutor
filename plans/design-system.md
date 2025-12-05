# CodeMentor Design System
## Version 1.0.0 | Date: 2025-12-05

---

## Document Purpose

This design system provides comprehensive visual and interaction guidelines for the LLM Coding Tutor Platform (CodeMentor). It is specifically formatted to be **machine-readable by AI agents**, particularly Claude Code, enabling automated implementation of designs.

All design tokens are available in structured JSON format at `design-tokens.json`.

---

## Table of Contents

1. [Design Principles](#design-principles)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Elevation & Shadows](#elevation--shadows)
6. [Border Radius](#border-radius)
7. [Motion & Transitions](#motion--transitions)
8. [Responsive Design](#responsive-design)
9. [Accessibility](#accessibility)
10. [Dark Mode](#dark-mode)

---

## Design Principles

### 1. Clarity
- **Clear visual hierarchy**: Information should be easy to scan and prioritize
- **Consistent patterns**: Similar elements should look and behave similarly
- **Purposeful design**: Every element serves a specific function

### 2. Accessibility First
- **WCAG 2.1 AA compliance**: Minimum 4.5:1 contrast ratio for normal text
- **Keyboard navigation**: All interactive elements must be keyboard accessible
- **Screen reader support**: Proper semantic HTML and ARIA labels
- **Touch targets**: Minimum 44x44px for all interactive elements

### 3. Learning Focus
- **Distraction-free**: Clean, minimalist design that emphasizes content
- **Code-centric**: Optimized for code readability with monospace fonts and syntax highlighting
- **Encouraging**: Warm, supportive visual language

### 4. Performance
- **Fast loading**: Optimized assets, lazy loading, minimal dependencies
- **Responsive**: Fluid layouts that work across all device sizes
- **Progressive enhancement**: Core functionality works without JavaScript

---

## Color System

### Primary Color - Blue
**Purpose**: Trust, learning, technology, primary actions

```
Primary 500 (Main): #0066CC
Primary 600 (Hover): #0052A3
Primary 700 (Active): #003D7A
Primary 100 (Light BG): #CCE0FF
Primary 50 (Lightest): #E6F0FF
```

**Usage**:
- Primary buttons
- Links
- Focus states
- Brand elements
- Active navigation items

### Secondary Color - Green
**Purpose**: Growth, success, achievement, positive feedback

```
Secondary 500 (Main): #00CC66
Secondary 600 (Hover): #00A352
Secondary 700 (Active): #007A3D
Secondary 100 (Light BG): #CCFFEB
```

**Usage**:
- Success states
- Achievement badges
- Completion indicators
- Positive feedback
- Learning streaks

### Accent Color - Orange
**Purpose**: Energy, highlights, calls-to-action, notifications

```
Accent 500 (Main): #FF9933
Accent 600 (Hover): #CC7A29
Accent 700 (Active): #995C1F
Accent 100 (Light BG): #FFE7CC
```

**Usage**:
- Daily exercise highlights
- Important notifications
- Hints and tips
- Special features

### Neutral Colors - Grayscale
**Purpose**: Text, backgrounds, borders, UI elements

```
Neutral 0 (White): #FFFFFF
Neutral 50: #F9FAFB
Neutral 100: #F3F4F6
Neutral 200: #E5E7EB
Neutral 300: #D1D5DB
Neutral 400: #9CA3AF
Neutral 500: #6B7280
Neutral 600: #4B5563
Neutral 700: #374151
Neutral 800: #1F2937
Neutral 900: #111827
Neutral 1000 (Black): #000000
```

**Text Usage**:
- Primary text: Neutral 900 (light mode), Neutral 50 (dark mode)
- Secondary text: Neutral 600 (light mode), Neutral 300 (dark mode)
- Tertiary text: Neutral 400 (light mode), Neutral 500 (dark mode)

**Background Usage**:
- Primary BG: Neutral 0 (light mode), Neutral 900 (dark mode)
- Secondary BG: Neutral 50 (light mode), Neutral 800 (dark mode)
- Tertiary BG: Neutral 100 (light mode), Neutral 700 (dark mode)

### Semantic Colors
**Purpose**: Communicate status and feedback

```
Success:
  - Light: #10B981
  - Default: #059669
  - Dark: #047857

Warning:
  - Light: #FBBF24
  - Default: #F59E0B
  - Dark: #D97706

Error:
  - Light: #EF4444
  - Default: #DC2626
  - Dark: #B91C1C

Info:
  - Light: #3B82F6
  - Default: #2563EB
  - Dark: #1D4ED8
```

**Usage**:
- Success: Exercise completion, test passes, successful actions
- Warning: Hints, cautions, approaching limits
- Error: Failed tests, validation errors, system errors
- Info: Tips, neutral notifications, informational messages

### Color Accessibility Guidelines

1. **Text Contrast**:
   - Normal text (< 18pt): Minimum 4.5:1 contrast ratio
   - Large text (≥ 18pt): Minimum 3.0:1 contrast ratio
   - UI components: Minimum 3.0:1 contrast ratio

2. **Never use color alone**: Always pair color with text, icons, or patterns

3. **Colorblind-friendly**: Test with colorblind simulation tools

---

## Typography

### Font Families

#### Headings & Body - Inter
```
Font Family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
Weights: 400 (Regular), 500 (Medium), 600 (Semibold), 700 (Bold)
```

**Rationale**: Inter is highly legible, has excellent Unicode support, and renders well at all sizes.

#### Code - Fira Code
```
Font Family: 'Fira Code', 'JetBrains Mono', 'SF Mono', Monaco, monospace
Weights: 400 (Regular), 500 (Medium)
Features: Programming ligatures enabled
```

**Rationale**: Fira Code has excellent programming ligatures and clear character differentiation (0 vs O, 1 vs l).

### Type Scale

```
6xl: 3.75rem (60px) - Hero headlines
5xl: 3rem (48px) - Page titles
4xl: 2.25rem (36px) - Section headings
3xl: 1.875rem (30px) - Subsection headings
2xl: 1.5rem (24px) - Card titles
xl: 1.25rem (20px) - Small headings
lg: 1.125rem (18px) - Large body
base: 1rem (16px) - Body text (default)
sm: 0.875rem (14px) - Small text
xs: 0.75rem (12px) - Captions, labels
```

### Heading Hierarchy

```
H1: font-size: 3xl (1.875rem), font-weight: 700, line-height: tight (1.25)
H2: font-size: 2xl (1.5rem), font-weight: 600, line-height: tight (1.25)
H3: font-size: xl (1.25rem), font-weight: 600, line-height: snug (1.375)
H4: font-size: lg (1.125rem), font-weight: 600, line-height: snug (1.375)
H5: font-size: base (1rem), font-weight: 600, line-height: normal (1.5)
H6: font-size: sm (0.875rem), font-weight: 600, line-height: normal (1.5)
```

### Body Text

```
Body Large: font-size: lg (1.125rem), font-weight: 400, line-height: relaxed (1.625)
Body Regular: font-size: base (1rem), font-weight: 400, line-height: normal (1.5)
Body Small: font-size: sm (0.875rem), font-weight: 400, line-height: normal (1.5)
Caption: font-size: xs (0.75rem), font-weight: 400, line-height: normal (1.5)
```

### Code Text

```
Code Inline: font-family: Fira Code, font-size: 0.875em, background: Neutral 100, padding: 0.125rem 0.25rem, border-radius: sm
Code Block: font-family: Fira Code, font-size: sm (0.875rem), line-height: relaxed (1.625), background: Neutral 900, color: Neutral 50
```

### Typography Rules

1. **Line length**: 50-75 characters per line for optimal readability
2. **Paragraph spacing**: 1.5rem (24px) between paragraphs
3. **Heading margins**: 2rem top, 1rem bottom
4. **Font loading**: Use font-display: swap for web fonts

---

## Spacing & Layout

### Spacing Scale
**Base unit**: 4px (0.25rem)

```
0: 0
0.5: 0.125rem (2px)
1: 0.25rem (4px)
2: 0.5rem (8px)
3: 0.75rem (12px)
4: 1rem (16px)
5: 1.25rem (20px)
6: 1.5rem (24px)
8: 2rem (32px)
10: 2.5rem (40px)
12: 3rem (48px)
16: 4rem (64px)
20: 5rem (80px)
24: 6rem (96px)
32: 8rem (128px)
```

### Component Spacing

**Padding** (internal spacing):
```
xs: 0.5rem (8px)
sm: 0.75rem (12px)
md: 1rem (16px)
lg: 1.5rem (24px)
xl: 2rem (32px)
```

**Gap** (spacing between elements):
```
xs: 0.25rem (4px)
sm: 0.5rem (8px)
md: 1rem (16px)
lg: 1.5rem (24px)
xl: 2rem (32px)
```

### Layout Spacing

**Section spacing** (vertical rhythm):
```
xs: 2rem (32px)
sm: 3rem (48px)
md: 4rem (64px)
lg: 6rem (96px)
xl: 8rem (128px)
```

**Container padding**:
```
Mobile: 1rem (16px)
Tablet: 2rem (32px)
Desktop: 3rem (48px)
```

### Layout Patterns

#### Container
```
max-width: 1280px
margin: 0 auto
padding: responsive (see container padding above)
```

#### Grid System
```
Columns: 12-column grid
Gutter: 1.5rem (24px)
Mobile: 1 column
Tablet: 6 columns
Desktop: 12 columns
```

#### Card Spacing
```
Padding: lg (1.5rem / 24px)
Gap between cards: md (1rem / 16px)
```

---

## Elevation & Shadows

### Shadow Scale

```
none: No shadow
sm: Subtle lift (0 1px 2px rgba(0,0,0,0.05))
default: Light lift (0 1px 3px rgba(0,0,0,0.1))
md: Moderate lift (0 4px 6px rgba(0,0,0,0.1))
lg: High lift (0 10px 15px rgba(0,0,0,0.1))
xl: Floating (0 20px 25px rgba(0,0,0,0.1))
2xl: Modal/overlay (0 25px 50px rgba(0,0,0,0.25))
```

### Usage Guidelines

```
Flat surfaces: shadow-none or shadow-sm
Cards: shadow-default
Dropdowns/Popovers: shadow-lg
Modals: shadow-2xl
Focus states: Custom shadow (0 0 0 3px rgba(0,102,204,0.4))
```

### Z-Index Scale

```
dropdown: 1000
sticky: 1020
fixed: 1030
modalBackdrop: 1040
modal: 1050
popover: 1060
tooltip: 1070
```

---

## Border Radius

### Radius Scale

```
none: 0
sm: 0.125rem (2px)
default: 0.25rem (4px)
md: 0.375rem (6px)
lg: 0.5rem (8px)
xl: 0.75rem (12px)
2xl: 1rem (16px)
3xl: 1.5rem (24px)
full: 9999px (circular)
```

### Usage Guidelines

```
Buttons: default (4px) or md (6px)
Input fields: default (4px)
Cards: lg (8px)
Modals: xl (12px)
Avatars: full (circular)
Badges: full (pill-shaped)
```

---

## Motion & Transitions

### Duration

```
fast: 150ms - Hover states, simple transitions
base: 200ms - Default transitions
slow: 300ms - Complex animations, page transitions
slower: 500ms - Page loads, major state changes
```

### Timing Functions

```
easeIn: cubic-bezier(0.4, 0, 1, 1) - Elements entering
easeOut: cubic-bezier(0, 0, 0.2, 1) - Elements exiting
easeInOut: cubic-bezier(0.4, 0, 0.2, 1) - Elements moving
sharp: cubic-bezier(0.4, 0, 0.6, 1) - Quick, snappy movements
```

### Common Transitions

```
Hover state: transition: all 150ms ease-out
Button click: transition: transform 100ms ease-in
Modal appear: transition: opacity 300ms ease-out, transform 300ms ease-out
Page transition: transition: opacity 500ms ease-in-out
```

### Animation Principles

1. **Purposeful**: Animations should guide attention or provide feedback
2. **Subtle**: Avoid distracting or overwhelming animations
3. **Fast**: Keep animations under 500ms
4. **Accessible**: Respect prefers-reduced-motion setting

---

## Responsive Design

### Breakpoints

```
xs: 0px - Extra small devices (phones in portrait)
sm: 640px - Small devices (phones in landscape, small tablets)
md: 768px - Medium devices (tablets)
lg: 1024px - Large devices (laptops, desktops)
xl: 1280px - Extra large devices (large desktops)
2xl: 1536px - 2X large devices (wide monitors)
```

### Responsive Patterns

#### Mobile First
Build for mobile first, then enhance for larger screens.

```css
/* Mobile: base styles */
.container { padding: 1rem; }

/* Tablet and up */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container { padding: 3rem; }
}
```

#### Responsive Typography

```
Mobile (< 640px):
  - H1: 2xl (1.5rem)
  - Body: base (1rem)
  - Code: sm (0.875rem)

Tablet (640px - 1024px):
  - H1: 3xl (1.875rem)
  - Body: base (1rem)
  - Code: sm (0.875rem)

Desktop (> 1024px):
  - H1: 4xl (2.25rem)
  - Body: lg (1.125rem)
  - Code: base (1rem)
```

#### Responsive Grids

```
Mobile: 1 column
Tablet: 2 columns
Desktop: 3-4 columns
```

#### Touch Targets
Minimum touch target: 44x44px on mobile devices

---

## Accessibility

### WCAG 2.1 AA Compliance

#### Color Contrast
- Normal text: Minimum 4.5:1 contrast ratio
- Large text (18pt+): Minimum 3.0:1 contrast ratio
- UI components: Minimum 3.0:1 contrast ratio

#### Focus Indicators
```
Focus style:
  - outline: 2px solid #0066CC
  - outline-offset: 2px
  - border-radius: default (4px)
```

#### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Tab order must follow logical flow
- Skip links for main content
- Visible focus indicators

#### Screen Reader Support
- Semantic HTML elements
- ARIA labels where needed
- Alt text for all images
- Form labels for all inputs
- Live regions for dynamic content

#### Touch Targets
- Minimum size: 44x44px
- Spacing between targets: 8px minimum

#### Motion
- Respect prefers-reduced-motion
- Provide alternative for auto-playing content
- Allow pause/stop controls

### Accessibility Checklist

- [ ] Color contrast meets WCAG AA standards
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible
- [ ] ARIA labels are present where needed
- [ ] Form inputs have associated labels
- [ ] Images have descriptive alt text
- [ ] Touch targets are at least 44x44px
- [ ] Motion respects user preferences
- [ ] Content is readable at 200% zoom
- [ ] Headings follow logical hierarchy

---

## Dark Mode

### Implementation Strategy

Use CSS custom properties (variables) for easy theme switching:

```css
:root {
  --color-bg-primary: #FFFFFF;
  --color-text-primary: #111827;
}

[data-theme="dark"] {
  --color-bg-primary: #111827;
  --color-text-primary: #F9FAFB;
}
```

### Dark Mode Color Adjustments

#### Backgrounds
```
Light Mode → Dark Mode
Neutral 0 (#FFFFFF) → Neutral 900 (#111827)
Neutral 50 (#F9FAFB) → Neutral 800 (#1F2937)
Neutral 100 (#F3F4F6) → Neutral 700 (#374151)
```

#### Text
```
Light Mode → Dark Mode
Neutral 900 (#111827) → Neutral 50 (#F9FAFB)
Neutral 600 (#4B5563) → Neutral 300 (#D1D5DB)
Neutral 400 (#9CA3AF) → Neutral 500 (#6B7280)
```

#### Shadows
Reduce shadow opacity in dark mode:
```
Light Mode: rgba(0, 0, 0, 0.1)
Dark Mode: rgba(0, 0, 0, 0.3)
```

#### Code Blocks
```
Light Mode:
  - Background: Neutral 900
  - Text: Neutral 50

Dark Mode:
  - Background: Neutral 1000 (black)
  - Text: Neutral 100
```

### Dark Mode Guidelines

1. **Reduce brightness**: Use softer whites (Neutral 50 instead of pure white)
2. **Increase contrast**: Ensure text remains readable
3. **Adjust colors**: Reduce saturation slightly in dark mode
4. **Test thoroughly**: Verify all UI states in both modes
5. **Respect preference**: Use prefers-color-scheme media query

---

## Implementation Notes for AI Agents

### JSON Structure
All design tokens are available in `design-tokens.json` with the following structure:
- `colors`: All color values organized by purpose
- `typography`: Font families, sizes, weights, line heights
- `spacing`: Spacing scale and semantic spacing values
- `borderRadius`: Radius values for rounded corners
- `shadows`: Shadow definitions for elevation
- `breakpoints`: Responsive breakpoint values
- `zIndex`: Stacking order values
- `transitions`: Animation durations and timing functions
- `accessibility`: WCAG compliance values

### CSS Variable Naming Convention
```
--{category}-{property}-{variant}

Examples:
--color-primary-500
--font-size-xl
--spacing-4
--shadow-lg
--radius-default
```

### Component Implementation
When implementing components, reference design tokens:
```
Button:
  - Background: colors.primary.500
  - Padding: spacing.component.padding.md
  - Border radius: borderRadius.default
  - Font size: typography.fontSizes.base
  - Transition: transitions.duration.fast + transitions.timing.easeOut
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial design system documentation |

---

## Related Documents

- `design-tokens.json` - Machine-readable design tokens
- `wireframes.md` - Screen wireframes
- `components.md` - Component library specifications
- `user-flows.md` - User journey diagrams
- `accessibility.md` - Detailed accessibility guidelines

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-12-05
**Maintained by**: Design System Engineer (AI Agent)
