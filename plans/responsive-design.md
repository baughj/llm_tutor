# CodeMentor Responsive Design Specifications
## Version 1.0.0 | Date: 2025-12-05

---

## Document Purpose

This document provides comprehensive responsive design specifications for the CodeMentor platform. All specifications are **machine-readable** and formatted for AI agent implementation (particularly Claude Code).

This document includes:
1. **Breakpoint definitions** with design token references
2. **Responsive patterns** for common layouts
3. **Typography scaling** across device sizes
4. **Component adaptations** for mobile, tablet, and desktop
5. **Touch optimization** guidelines
6. **Performance considerations**

---

## Table of Contents

1. [Breakpoint System](#1-breakpoint-system)
2. [Grid System](#2-grid-system)
3. [Typography Scaling](#3-typography-scaling)
4. [Component Responsive Patterns](#4-component-responsive-patterns)
5. [Navigation Patterns](#5-navigation-patterns)
6. [Touch Optimization](#6-touch-optimization)
7. [Images & Media](#7-images--media)
8. [Performance Optimization](#8-performance-optimization)

---

## 1. Breakpoint System

### Breakpoint Definitions

```yaml
breakpoints:
  xs:
    min: 0px
    max: 639px
    description: Extra small devices (phones in portrait)
    typical-devices:
      - iPhone SE (375px)
      - Small Android phones (360px)
    container-width: 100%
    container-padding: spacing.4 (1rem)

  sm:
    min: 640px
    max: 767px
    description: Small devices (large phones, small tablets)
    typical-devices:
      - iPhone 12/13/14 Pro (390px)
      - Large Android phones (414px)
      - Small tablets in portrait
    container-width: 640px
    container-padding: spacing.6 (1.5rem)

  md:
    min: 768px
    max: 1023px
    description: Medium devices (tablets, small laptops)
    typical-devices:
      - iPad (768px)
      - iPad Mini (768px)
      - Small laptops (800px)
    container-width: 768px
    container-padding: spacing.8 (2rem)

  lg:
    min: 1024px
    max: 1279px
    description: Large devices (laptops, desktops)
    typical-devices:
      - iPad Pro (1024px)
      - Laptops (1280px)
      - Small desktops (1280px)
    container-width: 1024px
    container-padding: spacing.12 (3rem)

  xl:
    min: 1280px
    max: 1535px
    description: Extra large devices (large desktops)
    typical-devices:
      - Standard desktops (1920px)
      - Large monitors (1920px)
    container-width: 1280px
    container-padding: spacing.12 (3rem)

  2xl:
    min: 1536px
    max: null
    description: 2X large devices (wide monitors, 4K displays)
    typical-devices:
      - Ultra-wide monitors (2560px)
      - 4K displays (3840px)
    container-width: 1536px
    container-padding: spacing.12 (3rem)
```

### Media Query Syntax

```css
/* Mobile-first approach (min-width) */

/* Extra small (default, no media query needed) */
/* 0 - 639px */

/* Small and up */
@media (min-width: 640px) {
  /* sm breakpoint styles */
}

/* Medium and up */
@media (min-width: 768px) {
  /* md breakpoint styles */
}

/* Large and up */
@media (min-width: 1024px) {
  /* lg breakpoint styles */
}

/* Extra large and up */
@media (min-width: 1280px) {
  /* xl breakpoint styles */
}

/* 2X large and up */
@media (min-width: 1536px) {
  /* 2xl breakpoint styles */
}
```

### Breakpoint Ranges (max-width for specific ranges)

```css
/* Mobile only */
@media (max-width: 639px) {
  /* Mobile-specific styles */
}

/* Tablet only */
@media (min-width: 768px) and (max-width: 1023px) {
  /* Tablet-specific styles */
}

/* Desktop only */
@media (min-width: 1024px) {
  /* Desktop-specific styles */
}
```

---

## 2. Grid System

### Container

```yaml
container:
  description: Centered content container with max-width

  mobile (xs):
    width: 100%
    padding-left: spacing.4 (1rem)
    padding-right: spacing.4 (1rem)
    margin: 0 auto

  tablet (sm, md):
    max-width: breakpoints.md (768px)
    padding-left: spacing.6 (1.5rem)
    padding-right: spacing.6 (1.5rem)
    margin: 0 auto

  desktop (lg, xl, 2xl):
    max-width: breakpoints.xl (1280px)
    padding-left: spacing.12 (3rem)
    padding-right: spacing.12 (3rem)
    margin: 0 auto
```

### Grid Layout

```yaml
grid:
  description: 12-column responsive grid system

  mobile (xs):
    columns: 1
    gap: spacing.4 (1rem)

  small-tablet (sm):
    columns: 6
    gap: spacing.4 (1rem)

  tablet (md):
    columns: 12
    gap: spacing.6 (1.5rem)

  desktop (lg, xl, 2xl):
    columns: 12
    gap: spacing.6 (1.5rem)

column-spans:
  mobile:
    full: col-span-1 (100%)
    half: Not applicable (single column)
    third: Not applicable (single column)

  tablet:
    full: col-span-12 (100%)
    half: col-span-6 (50%)
    third: col-span-4 (33.33%)
    quarter: col-span-3 (25%)

  desktop:
    full: col-span-12 (100%)
    three-quarter: col-span-9 (75%)
    two-thirds: col-span-8 (66.67%)
    half: col-span-6 (50%)
    third: col-span-4 (33.33%)
    quarter: col-span-3 (25%)
```

### CSS Grid Implementation

```css
.grid {
  display: grid;
  gap: 1rem; /* spacing.4 */
}

/* Mobile: 1 column */
@media (min-width: 0) {
  .grid {
    grid-template-columns: repeat(1, 1fr);
  }
}

/* Tablet: 6 columns */
@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(6, 1fr);
  }
}

/* Tablet and Desktop: 12 columns */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(12, 1fr);
    gap: 1.5rem; /* spacing.6 */
  }
}
```

---

## 3. Typography Scaling

### Font Size Scaling

```yaml
typography-scaling:

  headings:
    h1:
      mobile: typography.fontSizes.2xl (1.5rem / 24px)
      tablet: typography.fontSizes.3xl (1.875rem / 30px)
      desktop: typography.fontSizes.4xl (2.25rem / 36px)

    h2:
      mobile: typography.fontSizes.xl (1.25rem / 20px)
      tablet: typography.fontSizes.2xl (1.5rem / 24px)
      desktop: typography.fontSizes.3xl (1.875rem / 30px)

    h3:
      mobile: typography.fontSizes.lg (1.125rem / 18px)
      tablet: typography.fontSizes.xl (1.25rem / 20px)
      desktop: typography.fontSizes.2xl (1.5rem / 24px)

    h4:
      mobile: typography.fontSizes.base (1rem / 16px)
      tablet: typography.fontSizes.lg (1.125rem / 18px)
      desktop: typography.fontSizes.xl (1.25rem / 20px)

    h5:
      mobile: typography.fontSizes.sm (0.875rem / 14px)
      tablet: typography.fontSizes.base (1rem / 16px)
      desktop: typography.fontSizes.lg (1.125rem / 18px)

    h6:
      mobile: typography.fontSizes.xs (0.75rem / 12px)
      tablet: typography.fontSizes.sm (0.875rem / 14px)
      desktop: typography.fontSizes.base (1rem / 16px)

  body:
    large:
      mobile: typography.fontSizes.base (1rem / 16px)
      tablet: typography.fontSizes.lg (1.125rem / 18px)
      desktop: typography.fontSizes.lg (1.125rem / 18px)

    regular:
      mobile: typography.fontSizes.sm (0.875rem / 14px)
      tablet: typography.fontSizes.base (1rem / 16px)
      desktop: typography.fontSizes.base (1rem / 16px)

    small:
      mobile: typography.fontSizes.xs (0.75rem / 12px)
      tablet: typography.fontSizes.sm (0.875rem / 14px)
      desktop: typography.fontSizes.sm (0.875rem / 14px)

  code:
    inline:
      mobile: typography.fontSizes.xs (0.75rem / 12px)
      tablet: typography.fontSizes.sm (0.875rem / 14px)
      desktop: typography.fontSizes.sm (0.875rem / 14px)

    block:
      mobile: typography.fontSizes.xs (0.75rem / 12px)
      tablet: typography.fontSizes.sm (0.875rem / 14px)
      desktop: typography.fontSizes.base (1rem / 16px)
```

### Line Height Scaling

```yaml
line-heights:
  mobile:
    headings: typography.lineHeights.tight (1.25)
    body: typography.lineHeights.normal (1.5)
    code: typography.lineHeights.relaxed (1.625)

  tablet:
    headings: typography.lineHeights.tight (1.25)
    body: typography.lineHeights.normal (1.5)
    code: typography.lineHeights.relaxed (1.625)

  desktop:
    headings: typography.lineHeights.snug (1.375)
    body: typography.lineHeights.relaxed (1.625)
    code: typography.lineHeights.relaxed (1.625)
```

### Reading Width

```yaml
reading-width:
  description: Optimal line length for readability (50-75 characters)

  mobile:
    max-width: 100% (no constraint)
    characters: ~50 chars at base size

  tablet:
    max-width: 45rem (720px)
    characters: ~65 chars at base size

  desktop:
    max-width: 60rem (960px)
    characters: ~75 chars at base size
```

---

## 4. Component Responsive Patterns

### Dashboard Layout

```yaml
dashboard:
  mobile (xs, sm):
    layout: single-column
    sidebar: hidden (accessible via menu)
    quick-stats: horizontal-scroll or stacked
    exercise-card: full-width
    recent-activity: collapsed (show 3)

  tablet (md):
    layout: two-column
    main-content: col-span-8
    sidebar: col-span-4 (collapsible)
    quick-stats: 3-column grid
    exercise-card: full-width
    recent-activity: show 5

  desktop (lg, xl, 2xl):
    layout: three-column
    main-content: col-span-8
    sidebar: col-span-4 (fixed)
    quick-stats: 4-column grid
    exercise-card: full-width in main
    recent-activity: show all (with scroll)
```

### Chat Interface

```yaml
chat:
  mobile (xs, sm):
    layout: full-screen
    messages: full-width
    message-bubble-max-width: 85%
    input-area: sticky-bottom
    code-blocks: horizontal-scroll if needed

  tablet (md):
    layout: centered with max-width
    messages: max-width 768px
    message-bubble-max-width: 70%
    input-area: sticky-bottom
    code-blocks: full-width with scroll

  desktop (lg, xl, 2xl):
    layout: centered or with sidebar
    messages: max-width 960px
    message-bubble-max-width: 70%
    input-area: fixed-bottom
    code-blocks: full-width no scroll
    sidebar: optional context panel (col-span-3)
```

### Exercise View

```yaml
exercise:
  mobile (xs, sm):
    layout: tabbed (Instructions | Code | Tests)
    instructions: full-screen tab
    code-editor: full-screen tab
    test-results: full-screen tab
    actions: sticky-bottom

  tablet (md):
    layout: split-view (50/50)
    instructions: left (col-span-6)
    code-editor: right (col-span-6)
    test-results: below code
    actions: inline with results

  desktop (lg, xl, 2xl):
    layout: three-panel (40/60 or custom)
    instructions: left (col-span-4)
    code-editor: right (col-span-8)
    test-results: below code or bottom panel
    actions: inline with results
    resizable-panels: enabled
```

### Cards

```yaml
cards:
  mobile (xs):
    width: 100%
    padding: spacing.4 (1rem)
    margin-bottom: spacing.4

  tablet (sm, md):
    width: 100% or col-span-6
    padding: spacing.6 (1.5rem)
    margin-bottom: spacing.6

  desktop (lg, xl, 2xl):
    width: varies by grid
    padding: spacing.6 (1.5rem)
    margin-bottom: spacing.6
    hover-effects: enabled (elevation)
```

### Modals

```yaml
modals:
  mobile (xs, sm):
    width: 100%
    height: 100vh (full-screen)
    border-radius: 0
    animation: slide-up from bottom

  tablet (md):
    width: 90vw
    max-width: 768px
    height: auto
    max-height: 90vh
    border-radius: borderRadius.xl
    animation: fade-in + scale

  desktop (lg, xl, 2xl):
    width: auto
    max-width: 60vw
    height: auto
    max-height: 90vh
    border-radius: borderRadius.xl
    animation: fade-in + scale
```

---

## 5. Navigation Patterns

### Header/Navigation

```yaml
header:
  mobile (xs, sm):
    layout: hamburger-menu
    logo: left
    menu-button: right
    navigation: off-canvas drawer
    user-menu: in drawer
    height: 3.5rem (56px)

  tablet (md):
    layout: collapsed-nav
    logo: left
    primary-nav: hidden (in menu)
    user-menu: right
    height: 4rem (64px)

  desktop (lg, xl, 2xl):
    layout: full-nav
    logo: left
    primary-nav: center/left
    user-menu: right
    height: 4rem (64px)
```

### Mobile Navigation Drawer

```yaml
mobile-drawer:
  width: 80vw
  max-width: 20rem (320px)
  height: 100vh
  position: fixed
  top: 0
  left: 0
  background: colors.background.light.primary
  box-shadow: shadows.2xl
  z-index: zIndex.modal
  transform: translateX(-100%)
  transition: transform transitions.duration.slow

  open:
    transform: translateX(0)

  backdrop:
    position: fixed
    inset: 0
    background: rgba(0, 0, 0, 0.5)
    z-index: zIndex.modalBackdrop
```

### Breadcrumbs

```yaml
breadcrumbs:
  mobile (xs, sm):
    show: back-button only
    style: icon + "Back"

  tablet (md):
    show: collapsed (... → Current)
    style: text with separators

  desktop (lg, xl, 2xl):
    show: full-path
    style: text with separators
```

### Tabs

```yaml
tabs:
  mobile (xs, sm):
    layout: horizontal-scroll
    tab-width: auto
    indicator: bottom-border
    scrollable: yes

  tablet (md, lg):
    layout: flex-wrap
    tab-width: auto
    indicator: bottom-border
    scrollable: no

  desktop (xl, 2xl):
    layout: flex-nowrap
    tab-width: auto
    indicator: bottom-border
    scrollable: no
```

---

## 6. Touch Optimization

### Touch Targets

```yaml
minimum-touch-target:
  size: 44x44px (accessibility.minimumTouchTarget)
  applies-to:
    - Buttons
    - Links
    - Form inputs
    - Checkboxes/radios
    - Icons (clickable)
    - Tab triggers
    - Menu items

spacing-between-targets:
  minimum: 8px
  recommended: 12px
```

### Touch-Specific Interactions

```yaml
touch-interactions:
  swipe:
    - Dismiss modals (swipe down)
    - Navigate carousel (swipe left/right)
    - Close drawer (swipe left)
    - Pull-to-refresh (swipe down on scrollable)

  long-press:
    - Context menus
    - Additional options
    - Copy text

  tap:
    - Standard button/link activation
    - Select items
    - Toggle states

  pinch-zoom:
    - Disabled on forms
    - Enabled on images
    - Enabled on code blocks (optional)
```

### Hover States on Touch Devices

```yaml
hover-adaptation:
  description: Adapt hover states for touch devices

  approach-1:
    use: @media (hover: hover)
    apply-hover-styles: only on devices with hover capability

  approach-2:
    use: active-states instead of hover on touch
    example: :active styles for immediate feedback

  approach-3:
    use: focus-visible for keyboard + touch
    example: visible focus for accessibility
```

---

## 7. Images & Media

### Responsive Images

```yaml
responsive-images:
  approach: srcset + sizes

  example:
    img:
      src: image-800w.jpg (fallback)
      srcset:
        - image-400w.jpg 400w
        - image-800w.jpg 800w
        - image-1200w.jpg 1200w
      sizes:
        - (max-width: 640px) 100vw
        - (max-width: 1024px) 50vw
        - 33vw
      alt: Descriptive text
      loading: lazy
```

### Video

```yaml
responsive-video:
  container:
    position: relative
    padding-bottom: 56.25% (16:9 aspect ratio)
    height: 0
    overflow: hidden

  iframe:
    position: absolute
    top: 0
    left: 0
    width: 100%
    height: 100%

  mobile:
    autoplay: disabled
    controls: visible
    preload: metadata

  desktop:
    autoplay: optional (user-controlled)
    controls: visible
    preload: metadata
```

### Code Blocks

```yaml
code-blocks:
  mobile (xs, sm):
    font-size: typography.fontSizes.xs
    overflow-x: scroll
    max-width: 100vw
    padding: spacing.3
    line-numbers: hidden (to save space)

  tablet (md):
    font-size: typography.fontSizes.sm
    overflow-x: auto
    max-width: 100%
    padding: spacing.4
    line-numbers: visible

  desktop (lg, xl, 2xl):
    font-size: typography.fontSizes.base
    overflow-x: auto
    max-width: 100%
    padding: spacing.6
    line-numbers: visible
    hover: show copy button
```

---

## 8. Performance Optimization

### Mobile Performance

```yaml
mobile-optimizations:
  critical-css:
    - Inline critical CSS for above-the-fold content
    - Defer non-critical stylesheets

  images:
    - Use WebP with fallback
    - Implement lazy loading
    - Serve appropriate sizes via srcset
    - Use placeholder (blur-up) technique

  fonts:
    - Use font-display: swap
    - Subset fonts (only needed glyphs)
    - Preload critical fonts
    - Limit font weights (2-3 max)

  javascript:
    - Code splitting by route
    - Lazy load non-critical components
    - Defer third-party scripts
    - Use tree shaking

  network:
    - Implement service worker for offline
    - Cache static assets
    - Compress responses (gzip/brotli)
    - Use CDN for static assets
```

### Responsive Performance Budget

```yaml
performance-budget:
  mobile (3G):
    page-weight: 1.5MB max
    time-to-interactive: 5s max
    first-contentful-paint: 2s max
    javascript: 300KB max

  tablet (4G):
    page-weight: 2.5MB max
    time-to-interactive: 3s max
    first-contentful-paint: 1.5s max
    javascript: 500KB max

  desktop (WiFi):
    page-weight: 4MB max
    time-to-interactive: 2s max
    first-contentful-paint: 1s max
    javascript: 800KB max
```

---

## Testing Responsive Design

### Device Testing Matrix

```yaml
devices-to-test:
  mobile:
    - iPhone SE (375x667)
    - iPhone 12/13/14 (390x844)
    - iPhone 12/13/14 Pro Max (428x926)
    - Samsung Galaxy S21 (360x800)
    - Google Pixel 5 (393x851)

  tablet:
    - iPad (768x1024)
    - iPad Air (820x1180)
    - iPad Pro 11" (834x1194)
    - iPad Pro 12.9" (1024x1366)

  desktop:
    - MacBook Air (1280x800)
    - MacBook Pro 13" (1440x900)
    - MacBook Pro 16" (1728x1117)
    - Desktop 1080p (1920x1080)
    - Desktop 4K (3840x2160)
```

### Browser Testing

```yaml
browsers:
  mobile:
    - Safari iOS (latest 2 versions)
    - Chrome Mobile (latest 2 versions)
    - Samsung Internet (latest)

  tablet:
    - Safari iPadOS (latest 2 versions)
    - Chrome Mobile (latest 2 versions)

  desktop:
    - Chrome (latest 2 versions)
    - Firefox (latest 2 versions)
    - Safari (latest 2 versions)
    - Edge (latest 2 versions)
```

---

## Implementation Examples

### Example: Responsive Dashboard Component

```css
/* Mobile-first base styles */
.dashboard {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
  padding: 1rem;
}

.sidebar {
  display: none; /* Hidden on mobile */
}

/* Tablet: Show sidebar as collapsible */
@media (min-width: 768px) {
  .dashboard {
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    padding: 2rem;
  }

  .sidebar {
    display: block;
  }
}

/* Desktop: Fixed sidebar */
@media (min-width: 1024px) {
  .dashboard {
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
    padding: 3rem;
  }

  .sidebar {
    position: sticky;
    top: 5rem;
    max-height: calc(100vh - 6rem);
    overflow-y: auto;
  }
}
```

### Example: Responsive Typography

```css
/* Mobile-first */
h1 {
  font-size: 1.5rem; /* 24px */
  line-height: 1.25;
}

/* Tablet */
@media (min-width: 768px) {
  h1 {
    font-size: 1.875rem; /* 30px */
  }
}

/* Desktop */
@media (min-width: 1024px) {
  h1 {
    font-size: 2.25rem; /* 36px */
    line-height: 1.375;
  }
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial responsive design specifications |

---

## Related Documents

- `design-system.md` - Design system guidelines
- `design-tokens.json` - Machine-readable design tokens
- `wireframes.md` - Screen wireframes
- `accessibility.md` - Accessibility guidelines

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-12-05
**Maintained by**: Design System Engineer (AI Agent)
