# CodeMentor Component Library
## Version 1.0.0 | Date: 2025-12-05

---

## Document Purpose

This document provides comprehensive specifications for all reusable UI components in the CodeMentor platform. All specifications are **machine-readable** and formatted for AI agent implementation (particularly Claude Code).

Each component includes:
1. **Visual specification** with design token references
2. **Variants** and size options
3. **States** (default, hover, active, disabled, etc.)
4. **Props/API** for implementation
5. **Accessibility requirements**
6. **Usage guidelines** and examples

---

## Table of Contents

1. [Buttons](#1-buttons)
2. [Form Inputs](#2-form-inputs)
3. [Cards](#3-cards)
4. [Navigation](#4-navigation)
5. [Badges & Tags](#5-badges--tags)
6. [Modals & Dialogs](#6-modals--dialogs)
7. [Tooltips & Popovers](#7-tooltips--popovers)
8. [Progress Indicators](#8-progress-indicators)
9. [Data Display](#9-data-display)
10. [Feedback Components](#10-feedback-components)

---

## 1. Buttons

### Button Component Specification

#### Base Button
```yaml
component: Button
description: Primary interactive element for triggering actions

baseStyles:
  display: inline-flex
  align-items: center
  justify-content: center
  gap: spacing.2 (0.5rem)
  border-radius: borderRadius.default (4px)
  font-family: typography.fontFamilies.body
  font-weight: typography.fontWeights.medium
  transition: all transitions.duration.fast transitions.timing.easeOut
  cursor: pointer
  border: none
  text-decoration: none
  user-select: none
```

#### Variants

##### Primary Button
```yaml
variant: primary
usage: Main actions, primary CTAs

default:
  background: colors.primary.500
  color: colors.text.light.inverse
  padding: spacing.3 spacing.6 (0.75rem 1.5rem)
  font-size: typography.fontSizes.base

hover:
  background: colors.primary.600
  transform: translateY(-1px)
  box-shadow: shadows.md

active:
  background: colors.primary.700
  transform: translateY(0)

focus:
  outline: none
  box-shadow: shadows.focus

disabled:
  background: colors.neutral.300
  color: colors.neutral.500
  cursor: not-allowed
  opacity: 0.6
```

##### Secondary Button
```yaml
variant: secondary
usage: Secondary actions, less emphasis

default:
  background: colors.neutral.0
  color: colors.primary.500
  border: 1px solid colors.primary.500
  padding: spacing.3 spacing.6

hover:
  background: colors.primary.50
  border-color: colors.primary.600

active:
  background: colors.primary.100
```

##### Tertiary/Ghost Button
```yaml
variant: tertiary
usage: Tertiary actions, minimal emphasis

default:
  background: transparent
  color: colors.primary.500
  padding: spacing.3 spacing.4

hover:
  background: colors.primary.50

active:
  background: colors.primary.100
```

##### Danger Button
```yaml
variant: danger
usage: Destructive actions (delete, remove)

default:
  background: colors.semantic.error.default
  color: colors.text.light.inverse
  padding: spacing.3 spacing.6

hover:
  background: colors.semantic.error.dark

active:
  background: colors.semantic.error.dark
  transform: scale(0.98)
```

#### Sizes

```yaml
size: sm
  padding: spacing.2 spacing.4 (0.5rem 1rem)
  font-size: typography.fontSizes.sm
  min-height: 2rem (32px)

size: md (default)
  padding: spacing.3 spacing.6 (0.75rem 1.5rem)
  font-size: typography.fontSizes.base
  min-height: 2.5rem (40px)

size: lg
  padding: spacing.4 spacing.8 (1rem 2rem)
  font-size: typography.fontSizes.lg
  min-height: 3rem (48px)
```

#### With Icons

```yaml
iconButton:
  leftIcon:
    margin-right: spacing.2
    font-size: 1.25em

  rightIcon:
    margin-left: spacing.2
    font-size: 1.25em

  iconOnly:
    padding: spacing.3
    min-width: 2.5rem (40px)
    aspect-ratio: 1/1
    border-radius: borderRadius.default
```

#### Loading State

```yaml
loading:
  opacity: 0.7
  cursor: wait
  position: relative

  spinner:
    position: absolute
    top: 50%
    left: 50%
    transform: translate(-50%, -50%)
    width: 1rem
    height: 1rem
    border: 2px solid currentColor
    border-right-color: transparent
    border-radius: borderRadius.full
    animation: spin 0.6s linear infinite
```

#### Props API

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  onClick?: (event: React.MouseEvent) => void;
  type?: 'button' | 'submit' | 'reset';
  ariaLabel?: string;
  children: React.ReactNode;
}
```

#### Accessibility

```yaml
accessibility:
  - Must have discernible text or aria-label
  - Minimum touch target: 44x44px (accessibility.minimumTouchTarget)
  - Keyboard accessible (focusable)
  - Visible focus indicator
  - Disabled state announced to screen readers
  - Loading state announced via aria-live
```

---

## 2. Form Inputs

### Text Input

```yaml
component: TextInput
description: Single-line text input field

baseStyles:
  display: block
  width: 100%
  padding: spacing.3 (0.75rem)
  font-size: typography.fontSizes.base
  font-family: typography.fontFamilies.body
  color: colors.text.light.primary
  background: colors.background.light.primary
  border: 1px solid colors.neutral.300
  border-radius: borderRadius.default
  transition: all transitions.duration.base transitions.timing.easeOut

states:
  default:
    border-color: colors.neutral.300

  hover:
    border-color: colors.neutral.400

  focus:
    border-color: colors.primary.500
    outline: none
    box-shadow: shadows.focus

  error:
    border-color: colors.semantic.error.default

  disabled:
    background: colors.neutral.100
    color: colors.neutral.500
    cursor: not-allowed
    opacity: 0.6

  readonly:
    background: colors.neutral.50
    cursor: default
```

#### With Label

```yaml
label:
  display: block
  font-size: typography.fontSizes.sm
  font-weight: typography.fontWeights.medium
  color: colors.text.light.primary
  margin-bottom: spacing.2

  required:
    after-content: " *"
    color: colors.semantic.error.default
```

#### Helper Text & Error Messages

```yaml
helperText:
  font-size: typography.fontSizes.xs
  color: colors.text.light.tertiary
  margin-top: spacing.1

errorText:
  font-size: typography.fontSizes.xs
  color: colors.semantic.error.default
  margin-top: spacing.1
  display: flex
  align-items: center
  gap: spacing.1

  icon:
    font-size: typography.fontSizes.sm
```

#### Input with Icon

```yaml
withLeftIcon:
  paddingLeft: spacing.10 (2.5rem)
  icon:
    position: absolute
    left: spacing.3
    top: 50%
    transform: translateY(-50%)
    color: colors.neutral.500

withRightIcon:
  paddingRight: spacing.10
  icon:
    position: absolute
    right: spacing.3
    top: 50%
    transform: translateY(-50%)
    color: colors.neutral.500
```

### Textarea

```yaml
component: Textarea
extends: TextInput

specific:
  min-height: 6rem (96px)
  resize: vertical
  line-height: typography.lineHeights.relaxed
  padding: spacing.3
```

### Checkbox

```yaml
component: Checkbox
description: Binary selection control

container:
  display: inline-flex
  align-items: center
  gap: spacing.2
  cursor: pointer

input:
  appearance: none
  width: 1.25rem (20px)
  height: 1.25rem (20px)
  border: 2px solid colors.neutral.400
  border-radius: borderRadius.sm
  cursor: pointer
  position: relative
  transition: all transitions.duration.base

  checked:
    background: colors.primary.500
    border-color: colors.primary.500

    checkmark:
      position: absolute
      content: ""
      width: 0.5rem
      height: 0.875rem
      border: solid colors.neutral.0
      border-width: 0 2px 2px 0
      transform: rotate(45deg) translate(-50%, -50%)
      top: 45%
      left: 50%

  focus:
    box-shadow: shadows.focus

  disabled:
    opacity: 0.5
    cursor: not-allowed

label:
  font-size: typography.fontSizes.base
  color: colors.text.light.primary
  cursor: pointer
  user-select: none
```

### Radio Button

```yaml
component: Radio
description: Single selection from group

input:
  appearance: none
  width: 1.25rem (20px)
  height: 1.25rem (20px)
  border: 2px solid colors.neutral.400
  border-radius: borderRadius.full
  cursor: pointer
  position: relative

  checked:
    border-color: colors.primary.500

    dot:
      position: absolute
      width: 0.625rem (10px)
      height: 0.625rem (10px)
      background: colors.primary.500
      border-radius: borderRadius.full
      top: 50%
      left: 50%
      transform: translate(-50%, -50%)

# Label similar to checkbox
```

### Select Dropdown

```yaml
component: Select
description: Dropdown selection control

trigger:
  display: flex
  align-items: center
  justify-content: space-between
  padding: spacing.3
  border: 1px solid colors.neutral.300
  border-radius: borderRadius.default
  background: colors.background.light.primary
  cursor: pointer
  min-height: 2.75rem (44px)

  hover:
    border-color: colors.neutral.400

  focus:
    border-color: colors.primary.500
    box-shadow: shadows.focus

  icon:
    transition: transform transitions.duration.base
    color: colors.neutral.500

  open:
    icon-transform: rotate(180deg)

dropdown:
  position: absolute
  top: 100%
  left: 0
  right: 0
  margin-top: spacing.2
  background: colors.background.light.primary
  border: 1px solid colors.neutral.200
  border-radius: borderRadius.default
  box-shadow: shadows.lg
  max-height: 20rem (320px)
  overflow-y: auto
  z-index: zIndex.dropdown

option:
  padding: spacing.3
  cursor: pointer
  transition: background transitions.duration.fast

  hover:
    background: colors.primary.50

  selected:
    background: colors.primary.100
    color: colors.primary.700
    font-weight: typography.fontWeights.medium

  disabled:
    color: colors.neutral.400
    cursor: not-allowed
    opacity: 0.5
```

---

## 3. Cards

### Base Card

```yaml
component: Card
description: Container for grouping related content

baseStyles:
  background: colors.background.light.primary
  border: 1px solid colors.neutral.200
  border-radius: borderRadius.lg (8px)
  padding: spacing.6 (1.5rem)
  box-shadow: shadows.default
  transition: all transitions.duration.base

variants:
  default:
    # Base styles

  elevated:
    box-shadow: shadows.lg
    border: none

  outlined:
    box-shadow: none
    border: 2px solid colors.neutral.200

  interactive:
    cursor: pointer

    hover:
      transform: translateY(-2px)
      box-shadow: shadows.lg
      border-color: colors.primary.200

    active:
      transform: translateY(0)
```

### Card Header

```yaml
cardHeader:
  display: flex
  align-items: center
  justify-content: space-between
  margin-bottom: spacing.4
  padding-bottom: spacing.4
  border-bottom: 1px solid colors.neutral.200

  title:
    font-size: typography.fontSizes.xl
    font-weight: typography.fontWeights.semibold
    color: colors.text.light.primary

  subtitle:
    font-size: typography.fontSizes.sm
    color: colors.text.light.secondary
    margin-top: spacing.1

  actions:
    display: flex
    gap: spacing.2
```

### Card Body

```yaml
cardBody:
  font-size: typography.fontSizes.base
  line-height: typography.lineHeights.relaxed
  color: colors.text.light.secondary
```

### Card Footer

```yaml
cardFooter:
  display: flex
  align-items: center
  justify-content: space-between
  margin-top: spacing.4
  padding-top: spacing.4
  border-top: 1px solid colors.neutral.200
```

---

## 4. Navigation

### Header/Navbar

```yaml
component: Header
description: Main navigation header

container:
  height: 4rem (64px)
  background: colors.background.light.primary
  border-bottom: 1px solid colors.neutral.200
  box-shadow: shadows.sm
  position: sticky
  top: 0
  z-index: zIndex.sticky

  inner:
    max-width: 1280px
    margin: 0 auto
    padding: 0 spacing.layout.container.padding.desktop
    height: 100%
    display: flex
    align-items: center
    justify-content: space-between
```

### Nav Link

```yaml
navLink:
  display: inline-flex
  align-items: center
  gap: spacing.2
  padding: spacing.2 spacing.3
  font-size: typography.fontSizes.base
  font-weight: typography.fontWeights.medium
  color: colors.text.light.secondary
  text-decoration: none
  border-radius: borderRadius.default
  transition: all transitions.duration.fast

  hover:
    color: colors.text.light.primary
    background: colors.neutral.50

  active:
    color: colors.primary.500
    background: colors.primary.50

  focus:
    outline: 2px solid colors.primary.500
    outline-offset: 2px
```

### Breadcrumbs

```yaml
component: Breadcrumbs
description: Hierarchical navigation trail

container:
  display: flex
  align-items: center
  gap: spacing.2
  font-size: typography.fontSizes.sm
  color: colors.text.light.secondary

item:
  display: inline-flex
  align-items: center
  gap: spacing.2

  link:
    color: colors.primary.500
    text-decoration: none

    hover:
      text-decoration: underline

  current:
    color: colors.text.light.primary
    font-weight: typography.fontWeights.medium

separator:
  color: colors.neutral.400
  content: "/"
  user-select: none
```

### Tabs

```yaml
component: Tabs
description: Organize content into separate views

tabList:
  display: flex
  border-bottom: 2px solid colors.neutral.200
  gap: spacing.4

tab:
  padding: spacing.4 spacing.6
  font-size: typography.fontSizes.base
  font-weight: typography.fontWeights.medium
  color: colors.text.light.secondary
  background: transparent
  border: none
  border-bottom: 2px solid transparent
  cursor: pointer
  transition: all transitions.duration.base
  margin-bottom: -2px

  hover:
    color: colors.text.light.primary

  active:
    color: colors.primary.500
    border-bottom-color: colors.primary.500

  disabled:
    color: colors.neutral.400
    cursor: not-allowed

tabPanel:
  padding: spacing.6 0
  animation: fadeIn transitions.duration.slow
```

---

## 5. Badges & Tags

### Badge

```yaml
component: Badge
description: Small status indicator or label

baseStyles:
  display: inline-flex
  align-items: center
  padding: spacing.1 spacing.2 (0.25rem 0.5rem)
  font-size: typography.fontSizes.xs
  font-weight: typography.fontWeights.medium
  border-radius: borderRadius.full
  text-transform: uppercase
  letter-spacing: typography.letterSpacing.wide

variants:
  default:
    background: colors.neutral.100
    color: colors.neutral.700

  primary:
    background: colors.primary.100
    color: colors.primary.700

  success:
    background: colors.semantic.success.light
    color: colors.neutral.0

  warning:
    background: colors.semantic.warning.light
    color: colors.neutral.900

  error:
    background: colors.semantic.error.light
    color: colors.neutral.0

  info:
    background: colors.semantic.info.light
    color: colors.neutral.0
```

### Tag

```yaml
component: Tag
description: Removable label or category

container:
  display: inline-flex
  align-items: center
  gap: spacing.2
  padding: spacing.2 spacing.3
  background: colors.primary.50
  color: colors.primary.700
  border: 1px solid colors.primary.200
  border-radius: borderRadius.default
  font-size: typography.fontSizes.sm

removeButton:
  display: flex
  align-items: center
  justify-content: center
  width: 1rem
  height: 1rem
  border: none
  background: transparent
  color: colors.primary.500
  cursor: pointer
  border-radius: borderRadius.sm

  hover:
    background: colors.primary.100
```

---

## 6. Modals & Dialogs

### Modal

```yaml
component: Modal
description: Overlay dialog for focused interaction

backdrop:
  position: fixed
  inset: 0
  background: rgba(0, 0, 0, 0.5)
  display: flex
  align-items: center
  justify-content: center
  z-index: zIndex.modalBackdrop
  animation: fadeIn transitions.duration.base

content:
  position: relative
  background: colors.background.light.primary
  border-radius: borderRadius.xl
  box-shadow: shadows.2xl
  max-width: 32rem (512px)
  width: 90%
  max-height: 90vh
  overflow-y: auto
  z-index: zIndex.modal
  animation: slideUp transitions.duration.slow

header:
  padding: spacing.6
  border-bottom: 1px solid colors.neutral.200
  display: flex
  align-items: center
  justify-content: space-between

  title:
    font-size: typography.fontSizes.2xl
    font-weight: typography.fontWeights.semibold
    color: colors.text.light.primary

  closeButton:
    width: 2rem
    height: 2rem
    display: flex
    align-items: center
    justify-content: center
    border: none
    background: transparent
    color: colors.neutral.500
    cursor: pointer
    border-radius: borderRadius.default

    hover:
      background: colors.neutral.100
      color: colors.neutral.700

body:
  padding: spacing.6

footer:
  padding: spacing.6
  border-top: 1px solid colors.neutral.200
  display: flex
  justify-content: flex-end
  gap: spacing.3
```

### Alert Dialog

```yaml
component: AlertDialog
description: Modal for confirmations

extends: Modal

specific:
  max-width: 28rem (448px)

  icon:
    width: 3rem (48px)
    height: 3rem (48px)
    border-radius: borderRadius.full
    display: flex
    align-items: center
    justify-content: center
    margin-bottom: spacing.4

    success:
      background: colors.semantic.success.light
      color: colors.neutral.0

    warning:
      background: colors.semantic.warning.light
      color: colors.neutral.900

    error:
      background: colors.semantic.error.light
      color: colors.neutral.0
```

---

## 7. Tooltips & Popovers

### Tooltip

```yaml
component: Tooltip
description: Contextual help text on hover

trigger:
  cursor: help

content:
  position: absolute
  background: colors.neutral.900
  color: colors.neutral.0
  padding: spacing.2 spacing.3
  border-radius: borderRadius.default
  font-size: typography.fontSizes.sm
  max-width: 16rem (256px)
  z-index: zIndex.tooltip
  box-shadow: shadows.lg
  animation: fadeIn transitions.duration.fast

  arrow:
    position: absolute
    width: 0.5rem
    height: 0.5rem
    background: colors.neutral.900
    transform: rotate(45deg)

placements:
  top:
    bottom: 100%
    margin-bottom: spacing.2

  bottom:
    top: 100%
    margin-top: spacing.2

  left:
    right: 100%
    margin-right: spacing.2

  right:
    left: 100%
    margin-left: spacing.2
```

---

## 8. Progress Indicators

### Progress Bar

```yaml
component: ProgressBar
description: Visual indicator of completion

container:
  width: 100%
  height: 0.5rem (8px)
  background: colors.neutral.200
  border-radius: borderRadius.full
  overflow: hidden

bar:
  height: 100%
  background: colors.primary.500
  border-radius: borderRadius.full
  transition: width transitions.duration.slow transitions.timing.easeOut

  animated:
    background-image: linear-gradient(
      45deg,
      rgba(255, 255, 255, 0.15) 25%,
      transparent 25%,
      transparent 50%,
      rgba(255, 255, 255, 0.15) 50%,
      rgba(255, 255, 255, 0.15) 75%,
      transparent 75%,
      transparent
    )
    background-size: 1rem 1rem
    animation: progressStripes 1s linear infinite
```

### Spinner/Loading

```yaml
component: Spinner
description: Loading indicator

container:
  display: inline-block
  width: 2rem (32px)
  height: 2rem (32px)
  border: 3px solid colors.neutral.200
  border-top-color: colors.primary.500
  border-radius: borderRadius.full
  animation: spin 0.6s linear infinite

sizes:
  sm:
    width: 1rem (16px)
    height: 1rem (16px)
    border-width: 2px

  md:
    width: 2rem (32px)
    height: 2rem (32px)
    border-width: 3px

  lg:
    width: 3rem (48px)
    height: 3rem (48px)
    border-width: 4px
```

### Skeleton

```yaml
component: Skeleton
description: Loading placeholder

baseStyles:
  background: linear-gradient(
    90deg,
    colors.neutral.200 0%,
    colors.neutral.100 50%,
    colors.neutral.200 100%
  )
  background-size: 200% 100%
  animation: shimmer 1.5s ease-in-out infinite
  border-radius: borderRadius.default

variants:
  text:
    height: 1rem
    margin-bottom: spacing.2

  title:
    height: 1.5rem
    width: 60%
    margin-bottom: spacing.4

  circle:
    border-radius: borderRadius.full
    aspect-ratio: 1/1

  rectangle:
    width: 100%
    height: 8rem
```

---

## 9. Data Display

### Table

```yaml
component: Table
description: Structured data display

container:
  width: 100%
  overflow-x: auto

table:
  width: 100%
  border-collapse: collapse
  font-size: typography.fontSizes.sm

thead:
  background: colors.neutral.50
  border-bottom: 2px solid colors.neutral.200

th:
  padding: spacing.3 spacing.4
  text-align: left
  font-weight: typography.fontWeights.semibold
  color: colors.text.light.primary
  white-space: nowrap

tbody:
  background: colors.background.light.primary

tr:
  border-bottom: 1px solid colors.neutral.200

  hover:
    background: colors.neutral.50

td:
  padding: spacing.3 spacing.4
  color: colors.text.light.secondary
```

### Avatar

```yaml
component: Avatar
description: User profile image or initials

container:
  display: inline-flex
  align-items: center
  justify-content: center
  border-radius: borderRadius.full
  overflow: hidden
  background: colors.primary.100
  color: colors.primary.700
  font-weight: typography.fontWeights.semibold

sizes:
  xs:
    width: 1.5rem (24px)
    height: 1.5rem (24px)
    font-size: typography.fontSizes.xs

  sm:
    width: 2rem (32px)
    height: 2rem (32px)
    font-size: typography.fontSizes.sm

  md:
    width: 2.5rem (40px)
    height: 2.5rem (40px)
    font-size: typography.fontSizes.base

  lg:
    width: 4rem (64px)
    height: 4rem (64px)
    font-size: typography.fontSizes.xl

  xl:
    width: 6rem (96px)
    height: 6rem (96px)
    font-size: typography.fontSizes.3xl

withImage:
  img:
    width: 100%
    height: 100%
    object-fit: cover
```

---

## 10. Feedback Components

### Toast/Notification

```yaml
component: Toast
description: Temporary feedback message

container:
  position: fixed
  bottom: spacing.6
  right: spacing.6
  background: colors.background.light.primary
  border-radius: borderRadius.lg
  box-shadow: shadows.xl
  padding: spacing.4
  display: flex
  align-items: flex-start
  gap: spacing.3
  min-width: 20rem (320px)
  max-width: 28rem (448px)
  z-index: zIndex.modal
  animation: slideInRight transitions.duration.slow

variants:
  success:
    border-left: 4px solid colors.semantic.success.default
    icon-color: colors.semantic.success.default

  warning:
    border-left: 4px solid colors.semantic.warning.default
    icon-color: colors.semantic.warning.default

  error:
    border-left: 4px solid colors.semantic.error.default
    icon-color: colors.semantic.error.default

  info:
    border-left: 4px solid colors.semantic.info.default
    icon-color: colors.semantic.info.default

icon:
  font-size: typography.fontSizes.xl
  flex-shrink: 0

content:
  flex: 1

  title:
    font-size: typography.fontSizes.base
    font-weight: typography.fontWeights.semibold
    color: colors.text.light.primary
    margin-bottom: spacing.1

  description:
    font-size: typography.fontSizes.sm
    color: colors.text.light.secondary

closeButton:
  flex-shrink: 0
  width: 1.5rem
  height: 1.5rem
  border: none
  background: transparent
  color: colors.neutral.500
  cursor: pointer

  hover:
    color: colors.neutral.700
```

### Alert Banner

```yaml
component: Alert
description: Prominent inline notification

container:
  padding: spacing.4
  border-radius: borderRadius.default
  display: flex
  align-items: flex-start
  gap: spacing.3

variants:
  success:
    background: colors.semantic.success.light
    color: colors.neutral.0

  warning:
    background: colors.semantic.warning.light
    color: colors.neutral.900

  error:
    background: colors.semantic.error.light
    color: colors.neutral.0

  info:
    background: colors.semantic.info.light
    color: colors.neutral.0

icon:
  font-size: typography.fontSizes.xl
  flex-shrink: 0

content:
  flex: 1
  font-size: typography.fontSizes.sm
```

---

## Component Composition Patterns

### Example: Dashboard Card with Progress

```yaml
composition:
  Card:
    variant: elevated
    children:
      - CardHeader:
          title: "Weekly Progress"
          subtitle: "7 of 10 exercises"
      - CardBody:
          - ProgressBar:
              value: 70
              animated: true
          - Text: "Great job! Keep up the streak!"
      - CardFooter:
          - Button:
              variant: primary
              size: sm
              text: "View Details"
```

---

## Animation Keyframes

```yaml
animations:
  fadeIn:
    from:
      opacity: 0
    to:
      opacity: 1

  slideUp:
    from:
      transform: translateY(20px)
      opacity: 0
    to:
      transform: translateY(0)
      opacity: 1

  slideInRight:
    from:
      transform: translateX(100%)
      opacity: 0
    to:
      transform: translateX(0)
      opacity: 1

  spin:
    from:
      transform: rotate(0deg)
    to:
      transform: rotate(360deg)

  shimmer:
    from:
      background-position: 200% 0
    to:
      background-position: -200% 0

  progressStripes:
    from:
      background-position: 0 0
    to:
      background-position: 1rem 0
```

---

## Implementation Notes for AI Agents

### Component File Structure
```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.styles.ts
│   ├── Button.types.ts
│   └── Button.test.tsx
├── Input/
│   ├── TextInput.tsx
│   ├── Textarea.tsx
│   ├── Checkbox.tsx
│   └── ...
└── ...
```

### CSS-in-JS Example (Styled Components)
```typescript
import styled from 'styled-components';
import { colors, spacing, borderRadius } from '../tokens';

export const StyledButton = styled.button<ButtonProps>`
  padding: ${spacing[3]} ${spacing[6]};
  background: ${props => colors.primary[500]};
  color: ${colors.text.light.inverse};
  border-radius: ${borderRadius.default};

  &:hover {
    background: ${colors.primary[600]};
  }
`;
```

### Design Token Import
```typescript
import tokens from '../design-tokens.json';

// Access tokens
const primaryColor = tokens.colors.primary[500];
const baseSpacing = tokens.spacing.scale[4];
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial component library documentation |

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
