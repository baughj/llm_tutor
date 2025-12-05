# CodeMentor Wireframes
## Version 1.0.0 | Date: 2025-12-05

---

## Document Purpose

This document contains ASCII/text-based wireframes for all key screens in the CodeMentor MVP. These wireframes are designed to be **machine-readable by AI agents** (particularly Claude Code) while remaining human-readable.

Each wireframe includes:
1. **Screen layout** in ASCII art
2. **Component specifications** with design token references
3. **Interaction notes** for dynamic behavior
4. **Responsive variations** for mobile, tablet, and desktop

---

## Table of Contents

1. [Dashboard](#1-dashboard)
2. [Chat Interface](#2-chat-interface)
3. [Exercise View](#3-exercise-view)
4. [Profile Page](#4-profile-page)
5. [Authentication Screens](#5-authentication-screens)
6. [Onboarding Interview](#6-onboarding-interview)
7. [Community Page](#7-community-page)
8. [Settings](#8-settings)

---

## 1. Dashboard

### Desktop Layout (> 1024px)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [HEADER]                                                                    │
│ ┌─────────┬───────────────────────────────────────────────────┬─────────┐  │
│ │ Logo    │  Dashboard  Community  Mentorship               │  [User] │  │
│ └─────────┴───────────────────────────────────────────────────┴─────────┘  │
├─────────────────────────────────────────────────────────────────────────────┤
│ [MAIN CONTENT AREA]                                                         │
│                                                                             │
│ ┌─────────────────────────────────┬─────────────────────────────────────┐  │
│ │ [LEFT: PRIMARY CONTENT]         │ [RIGHT: SIDEBAR]                    │  │
│ │                                 │                                     │  │
│ │ ┌─────────────────────────────┐ │ ┌─────────────────────────────────┐ │  │
│ │ │ Daily Exercise Card         │ │ │ Quick Stats                     │ │  │
│ │ │                             │ │ │ ┌─────────┬─────────┬─────────┐ │ │  │
│ │ │ 🎯 Today's Challenge        │ │ │ │ Streak  │ Total   │ Time    │ │ │  │
│ │ │                             │ │ │ │  7 🔥  │  42     │ 12h     │ │ │  │
│ │ │ [Exercise Title]            │ │ │ └─────────┴─────────┴─────────┘ │ │  │
│ │ │ Python • Intermediate       │ │ │                                 │ │  │
│ │ │                             │ │ │ ┌─────────────────────────────┐ │ │  │
│ │ │ [Brief Description...]      │ │ │ │ Progress This Week          │ │ │  │
│ │ │                             │ │ │ │ ███████░░░░░░░░░░  70%     │ │ │  │
│ │ │ [Start Exercise Button]     │ │ │ │ 7 of 10 exercises completed │ │ │  │
│ │ │                             │ │ │ └─────────────────────────────┘ │ │  │
│ │ └─────────────────────────────┘ │ │                                 │ │  │
│ │                                 │ │ ┌─────────────────────────────┐ │ │  │
│ │ ┌─────────────────────────────┐ │ │ │ Current Skill Levels        │ │ │  │
│ │ │ Continue Learning           │ │ │ │                             │ │ │  │
│ │ │                             │ │ │ │ Python:      ████████░░ 80% │ │ │  │
│ │ │ 📚 Recent Activity          │ │ │ │ Algorithms:  ██████░░░░ 60% │ │ │  │
│ │ │                             │ │ │ │ Data Struct: █████░░░░░ 50% │ │ │  │
│ │ │ • Yesterday: Completed      │ │ │ │                             │ │ │  │
│ │ │   "Binary Search Tree"      │ │ │ └─────────────────────────────┘ │ │  │
│ │ │                             │ │ │                                 │ │  │
│ │ │ • 2 days ago: Completed     │ │ │ ┌─────────────────────────────┐ │ │  │
│ │ │   "Linked Lists"            │ │ │ │ Recent Achievements         │ │ │  │
│ │ │                             │ │ │ │                             │ │ │  │
│ │ │ [View All]                  │ │ │ │ 🏆 7-Day Streak             │ │ │  │
│ │ └─────────────────────────────┘ │ │ │ 🎯 10 Exercises             │ │ │  │
│ │                                 │ │ │ ⭐ First Code Review        │ │ │  │
│ │ ┌─────────────────────────────┐ │ │ │                             │ │ │  │
│ │ │ Quick Actions               │ │ │ │ [View All Achievements]     │ │ │  │
│ │ │                             │ │ │ └─────────────────────────────┘ │ │  │
│ │ │ [💬 Chat with Tutor    ]    │ │ └─────────────────────────────────┘ │  │
│ │ │ [🔍 Browse Community   ]    │ │                                     │  │
│ │ │ [📊 View Progress      ]    │ │                                     │  │
│ │ │ [🎓 Find a Mentor      ]    │ │                                     │  │
│ │ └─────────────────────────────┘ │                                     │  │
│ │                                 │                                     │  │
│ └─────────────────────────────────┴─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Header
```yaml
container:
  height: 4rem (64px)
  padding: 0 spacing.layout.container.padding.desktop
  background: colors.background.light.primary
  border-bottom: 1px solid colors.neutral.200
  shadow: shadows.sm

logo:
  height: 2rem (32px)

navigation:
  display: flex
  gap: spacing.6 (1.5rem)

  link:
    font-size: typography.fontSizes.base
    font-weight: typography.fontWeights.medium
    color: colors.text.light.secondary
    padding: spacing.2 spacing.3
    border-radius: borderRadius.default

  link-active:
    color: colors.primary.500
    background: colors.primary.50

user-menu:
  avatar:
    size: 2.5rem (40px)
    border-radius: borderRadius.full
```

#### Daily Exercise Card
```yaml
card:
  background: colors.background.light.primary
  border: 1px solid colors.neutral.200
  border-radius: borderRadius.lg
  padding: spacing.layout.container.padding.desktop
  shadow: shadows.default

icon:
  font-size: typography.fontSizes.2xl

title:
  font-size: typography.fontSizes.2xl
  font-weight: typography.fontWeights.bold
  color: colors.text.light.primary
  margin-bottom: spacing.2

metadata:
  font-size: typography.fontSizes.sm
  color: colors.text.light.secondary
  display: flex
  gap: spacing.2

description:
  font-size: typography.fontSizes.base
  color: colors.text.light.secondary
  line-height: typography.lineHeights.relaxed
  margin: spacing.4 0

button:
  background: colors.primary.500
  color: colors.text.light.inverse
  padding: spacing.3 spacing.6
  border-radius: borderRadius.default
  font-size: typography.fontSizes.base
  font-weight: typography.fontWeights.medium
  transition: transitions.duration.fast transitions.timing.easeOut

  hover:
    background: colors.primary.600
    transform: translateY(-1px)
```

#### Quick Stats Widget
```yaml
container:
  background: colors.background.light.primary
  border: 1px solid colors.neutral.200
  border-radius: borderRadius.lg
  padding: spacing.6

stats-grid:
  display: grid
  grid-template-columns: repeat(3, 1fr)
  gap: spacing.4

stat-item:
  text-align: center

  value:
    font-size: typography.fontSizes.2xl
    font-weight: typography.fontWeights.bold
    color: colors.primary.500

  label:
    font-size: typography.fontSizes.sm
    color: colors.text.light.secondary
    margin-top: spacing.1
```

### Mobile Layout (< 640px)

```
┌─────────────────────────────┐
│ [HEADER - Collapsed]        │
│ ┌───┬───────────────┬─────┐ │
│ │☰  │ CodeMentor    │ 👤  │ │
│ └───┴───────────────┴─────┘ │
├─────────────────────────────┤
│ [MAIN CONTENT]              │
│                             │
│ ┌─────────────────────────┐ │
│ │ Quick Stats             │ │
│ │ ┌─────┬─────┬─────────┐ │ │
│ │ │🔥 7 │📚 42│⏱️ 12h  │ │ │
│ │ └─────┴─────┴─────────┘ │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ Today's Exercise        │ │
│ │                         │ │
│ │ 🎯 Binary Search        │ │
│ │ Python • Intermediate   │ │
│ │                         │ │
│ │ [Description...]        │ │
│ │                         │ │
│ │ [Start Exercise]        │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ Quick Actions           │ │
│ │ [💬 Chat with Tutor  ] │ │
│ │ [🔍 Browse Community ] │ │
│ │ [📊 View Progress    ] │ │
│ └─────────────────────────┘ │
│                             │
│ [Navigation tabs at bottom] │
└─────────────────────────────┘
```

### Interaction Notes

1. **Daily Exercise Card**:
   - Appears collapsed if user has already started
   - Shows "Continue" instead of "Start" if in progress
   - Displays completion checkmark when complete

2. **Quick Stats**:
   - Streak counter animates when incremented
   - Clicking stat opens detailed progress view

3. **Recent Activity**:
   - Loads most recent 3 items
   - "View All" opens full history

4. **Quick Actions**:
   - Each button navigates to respective feature
   - Visual hover states on all buttons

---

## 2. Chat Interface

### Desktop Layout (> 1024px)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [HEADER - Same as Dashboard]                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ [CHAT INTERFACE]                                                            │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Chat with Your Tutor                                         [⚙️ Options]│ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ [MESSAGE AREA - Scrollable]                                             │ │
│ │                                                                         │ │
│ │ ┌───────────────────────────────────────────────────────────┐           │ │
│ │ │ 🤖 Tutor                                          10:23 AM │           │ │
│ │ │ Hello! I'm excited to help you learn coding today. What   │           │ │
│ │ │ would you like to work on?                                │           │ │
│ │ └───────────────────────────────────────────────────────────┘           │ │
│ │                                                                         │ │
│ │           ┌───────────────────────────────────────────────┐             │ │
│ │           │ 👤 You                             10:24 AM   │             │ │
│ │           │ I'm working on today's exercise about binary  │             │ │
│ │           │ search. Can you help me understand the logic? │             │ │
│ │           └───────────────────────────────────────────────┘             │ │
│ │                                                                         │ │
│ │ ┌───────────────────────────────────────────────────────────┐           │ │
│ │ │ 🤖 Tutor                                          10:24 AM │           │ │
│ │ │ Of course! Let's think about it step by step. What's the  │           │ │
│ │ │ main idea behind binary search?                           │           │ │
│ │ │                                                           │           │ │
│ │ │ Think about how you would find a word in a dictionary.    │           │ │
│ │ └───────────────────────────────────────────────────────────┘           │ │
│ │                                                                         │ │
│ │           ┌───────────────────────────────────────────────┐             │ │
│ │           │ 👤 You                             10:25 AM   │             │ │
│ │           │ Here's my code so far:                        │             │ │
│ │           │                                               │             │ │
│ │           │ ```python                                     │             │ │
│ │           │ def binary_search(arr, target):               │             │ │
│ │           │     left, right = 0, len(arr) - 1             │             │ │
│ │           │     # Not sure what to do next                │             │ │
│ │           │ ```                                           │             │ │
│ │           └───────────────────────────────────────────────┘             │ │
│ │                                                                         │ │
│ │ ┌───────────────────────────────────────────────────────────┐           │ │
│ │ │ 🤖 Tutor                                  Typing... 💬     │           │ │
│ │ └───────────────────────────────────────────────────────────┘           │ │
│ │                                                                         │ │
│ │                                                                         │ │
│ │                                                                         │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ [INPUT AREA]                                                            │ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ Type your message...                                         [📎]   │ │ │
│ │ │                                                              [💾]   │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ │ [Send Button]                                                           │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Message Bubble - Tutor
```yaml
container:
  max-width: 70%
  background: colors.primary.50
  border-radius: borderRadius.lg
  padding: spacing.4
  margin-bottom: spacing.4
  align-self: flex-start

header:
  display: flex
  align-items: center
  gap: spacing.2
  margin-bottom: spacing.2

  avatar:
    font-size: typography.fontSizes.xl

  name:
    font-size: typography.fontSizes.sm
    font-weight: typography.fontWeights.semibold
    color: colors.primary.700

  timestamp:
    font-size: typography.fontSizes.xs
    color: colors.text.light.tertiary
    margin-left: auto

content:
  font-size: typography.fontSizes.base
  line-height: typography.lineHeights.relaxed
  color: colors.text.light.primary
```

#### Message Bubble - User
```yaml
container:
  max-width: 70%
  background: colors.neutral.100
  border-radius: borderRadius.lg
  padding: spacing.4
  margin-bottom: spacing.4
  align-self: flex-end

# Header and content specs similar to tutor bubble
# but aligned right
```

#### Code Block in Message
```yaml
container:
  background: colors.neutral.900
  border-radius: borderRadius.md
  padding: spacing.3
  margin: spacing.2 0
  overflow-x: auto

code:
  font-family: typography.fontFamilies.code.name
  font-size: typography.fontSizes.sm
  line-height: typography.lineHeights.relaxed
  color: colors.neutral.50

# Syntax highlighting applied via Prism.js or similar
```

#### Input Area
```yaml
container:
  border-top: 1px solid colors.neutral.200
  padding: spacing.4
  background: colors.background.light.primary

textarea:
  width: 100%
  min-height: 4rem
  padding: spacing.3
  border: 1px solid colors.neutral.300
  border-radius: borderRadius.default
  font-size: typography.fontSizes.base
  resize: vertical

  focus:
    border-color: colors.primary.500
    outline: none
    box-shadow: shadows.focus

actions:
  display: flex
  gap: spacing.2
  margin-top: spacing.2

button-send:
  background: colors.primary.500
  color: colors.text.light.inverse
  padding: spacing.2 spacing.6
  border-radius: borderRadius.default
  font-weight: typography.fontWeights.medium
```

### Mobile Layout

```
┌─────────────────────────────┐
│ [HEADER]                    │
│ [< Back] Chat with Tutor    │
├─────────────────────────────┤
│ [MESSAGE AREA]              │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🤖 Tutor      10:23 AM  │ │
│ │ Hello! What would you   │ │
│ │ like to work on?        │ │
│ └─────────────────────────┘ │
│                             │
│     ┌───────────────────┐   │
│     │ 👤 You   10:24 AM │   │
│     │ I need help with  │   │
│     │ binary search.    │   │
│     └───────────────────┘   │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🤖 Tutor      10:24 AM  │ │
│ │ Let's think step by     │ │
│ │ step...                 │ │
│ └─────────────────────────┘ │
│                             │
│                             │
├─────────────────────────────┤
│ [INPUT]                     │
│ ┌─────────────────────┬───┐ │
│ │ Type message...     │ ➤ │ │
│ └─────────────────────┴───┘ │
└─────────────────────────────┘
```

### Interaction Notes

1. **Auto-scroll**: Message area auto-scrolls to latest message
2. **Typing indicator**: Shows when tutor is generating response
3. **Code formatting**: Automatic syntax highlighting for code blocks
4. **Copy button**: Appears on hover over code blocks
5. **File attachment**: Upload code files or images (planned feature)

---

## 3. Exercise View

### Desktop Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [HEADER]                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ [EXERCISE VIEW]                                                             │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ [< Back to Dashboard]                        [🎯 Python • Intermediate] │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │                                                                         │ │
│ │ Implement Binary Search Algorithm                                      │ │
│ │ ═══════════════════════════════════════════════════════════════════     │ │
│ │                                                                         │ │
│ │ ┌─────────────────────────────┬─────────────────────────────────────┐  │ │
│ │ │ [LEFT: INSTRUCTIONS]        │ [RIGHT: WORKSPACE]                  │  │ │
│ │ │                             │                                     │  │ │
│ │ │ ## Problem Description      │ Your Solution:                      │  │ │
│ │ │                             │                                     │  │ │
│ │ │ Implement a binary search   │ ┌─────────────────────────────────┐ │  │ │
│ │ │ algorithm that finds the    │ │ ```python                       │ │  │ │
│ │ │ position of a target value  │ │ def binary_search(arr, target): │ │  │ │
│ │ │ in a sorted array.          │ │     # Your code here            │ │  │ │
│ │ │                             │ │                                 │ │  │ │
│ │ │ **Requirements:**           │ │                                 │ │  │ │
│ │ │ • Time complexity: O(log n) │ │                                 │ │  │ │
│ │ │ • Return index if found     │ │                                 │ │  │ │
│ │ │ • Return -1 if not found    │ │                                 │ │  │ │
│ │ │                             │ │                                 │ │  │ │
│ │ │ ## Examples                 │ │                                 │ │  │ │
│ │ │                             │ │                                 │ │  │ │
│ │ │ Input: [1,2,3,4,5], 3       │ │                                 │ │  │ │
│ │ │ Output: 2                   │ │                                 │ │  │ │
│ │ │                             │ │                                 │ │  │ │
│ │ │ Input: [1,2,3,4,5], 6       │ │                                 │ │  │ │
│ │ │ Output: -1                  │ │                                 │ │  │ │
│ │ │                             │ │                                 │ │  │ │
│ │ │ ## Hints (Click to reveal)  │ └─────────────────────────────────┘ │  │ │
│ │ │ [💡 Hint 1: Getting Started]│                                     │  │ │
│ │ │ [💡 Hint 2: Edge Cases]     │ [Run Tests] [Submit Solution]       │  │ │
│ │ │ [💡 Hint 3: Optimization]   │                                     │  │ │
│ │ │                             │ ┌─────────────────────────────────┐ │  │ │
│ │ │ [Ask Tutor for Help]        │ │ Test Results:                   │ │  │ │
│ │ │                             │ │                                 │ │  │ │
│ │ │                             │ │ ✓ Test 1: Passed                │ │  │ │
│ │ │                             │ │ ✓ Test 2: Passed                │ │  │ │
│ │ │                             │ │ ✗ Test 3: Failed                │ │  │ │
│ │ │                             │ │   Expected: 4                   │ │  │ │
│ │ │                             │ │   Got: -1                       │ │  │ │
│ │ │                             │ └─────────────────────────────────┘ │  │ │
│ │ └─────────────────────────────┴─────────────────────────────────────┘  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Exercise Header
```yaml
container:
  background: colors.background.light.secondary
  padding: spacing.6
  border-bottom: 1px solid colors.neutral.200

back-button:
  color: colors.primary.500
  font-size: typography.fontSizes.sm
  display: flex
  align-items: center
  gap: spacing.2

title:
  font-size: typography.fontSizes.4xl
  font-weight: typography.fontWeights.bold
  color: colors.text.light.primary
  margin: spacing.4 0

metadata-badge:
  display: inline-flex
  align-items: center
  gap: spacing.2
  background: colors.primary.100
  color: colors.primary.700
  padding: spacing.2 spacing.4
  border-radius: borderRadius.full
  font-size: typography.fontSizes.sm
```

#### Instructions Panel
```yaml
container:
  padding: spacing.6
  background: colors.background.light.primary
  overflow-y: auto

heading:
  font-size: typography.fontSizes.xl
  font-weight: typography.fontWeights.semibold
  color: colors.text.light.primary
  margin-bottom: spacing.3

paragraph:
  font-size: typography.fontSizes.base
  line-height: typography.lineHeights.relaxed
  color: colors.text.light.secondary
  margin-bottom: spacing.4

code-inline:
  font-family: typography.fontFamilies.code.name
  font-size: 0.875em
  background: colors.neutral.100
  padding: spacing.1 spacing.2
  border-radius: borderRadius.sm

hint-button:
  background: colors.accent.50
  border: 1px solid colors.accent.200
  color: colors.accent.700
  padding: spacing.3 spacing.4
  border-radius: borderRadius.default
  margin-bottom: spacing.2
  width: 100%
  text-align: left

  hover:
    background: colors.accent.100
```

#### Code Editor
```yaml
container:
  background: colors.neutral.900
  border-radius: borderRadius.lg
  overflow: hidden
  min-height: 400px

editor:
  font-family: typography.fontFamilies.code.name
  font-size: typography.fontSizes.base
  line-height: typography.lineHeights.relaxed
  padding: spacing.4
  color: colors.neutral.50

# Use Monaco Editor or CodeMirror for syntax highlighting
```

#### Test Results
```yaml
container:
  background: colors.background.light.secondary
  border-radius: borderRadius.lg
  padding: spacing.4
  margin-top: spacing.4

result-item:
  display: flex
  align-items: center
  gap: spacing.2
  padding: spacing.2 0
  font-size: typography.fontSizes.sm

  success:
    color: colors.semantic.success.default

  failure:
    color: colors.semantic.error.default
```

### Mobile Layout

```
┌─────────────────────────────┐
│ [< Back] Binary Search      │
│ Python • Intermediate       │
├─────────────────────────────┤
│ [TABS]                      │
│ [Instructions] [Code] [Test]│
├─────────────────────────────┤
│                             │
│ [TAB CONTENT - Switchable]  │
│                             │
│ Instructions Tab:           │
│ ┌─────────────────────────┐ │
│ │ ## Problem Description  │ │
│ │ Implement binary search │ │
│ │ ...                     │ │
│ │                         │ │
│ │ [💡 Hints]              │ │
│ │ [Ask Tutor]             │ │
│ └─────────────────────────┘ │
│                             │
│ Code Tab:                   │
│ ┌─────────────────────────┐ │
│ │ def binary_search(...): │ │
│ │     # Your code here    │ │
│ │                         │ │
│ └─────────────────────────┘ │
│ [Run Tests] [Submit]        │
│                             │
│ Test Tab:                   │
│ ┌─────────────────────────┐ │
│ │ ✓ Test 1: Passed        │ │
│ │ ✓ Test 2: Passed        │ │
│ │ ✗ Test 3: Failed        │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

### Interaction Notes

1. **Hints**: Click to reveal, expandable sections
2. **Run Tests**: Executes code against test cases
3. **Submit**: Marks exercise complete, stores solution
4. **Ask Tutor**: Opens chat with current exercise context
5. **Auto-save**: Solution saved every 30 seconds

---

## 4. Profile Page

### Desktop Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [HEADER]                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ [PROFILE PAGE]                                                              │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ [PROFILE HEADER]                                                        │ │
│ │ ┌───────┐                                                               │ │
│ │ │ [AVA] │  John Doe                                                     │ │
│ │ │ [TAR] │  @johndoe                                                     │ │
│ │ └───────┘  Member since Jan 2025                                        │ │
│ │            [Edit Profile]                                               │ │
│ │                                                                         │ │
│ │ 🎯 Goal: Become a Full-Stack Developer                                 │ │
│ │ 💻 Learning: Python, JavaScript, React                                 │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ [TABS]                                                                  │ │
│ │ ┌──────────┬──────────┬──────────┬──────────┬──────────┐               │ │
│ │ │ Overview │ Progress │ Achievem │ Activity │ Settings │               │ │
│ │ └──────────┴──────────┴──────────┴──────────┴──────────┘               │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ [TAB CONTENT: Overview]                                                     │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Stats Overview                                                          │ │
│ │ ┌───────────────┬───────────────┬───────────────┬───────────────┐      │ │
│ │ │ 🔥 Streak     │ 📚 Exercises  │ ⏱️ Time Spent │ 🏆 Achievements│      │ │
│ │ │    7 days     │     42        │    24.5 hrs   │      12       │      │ │
│ │ └───────────────┴───────────────┴───────────────┴───────────────┘      │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────┬─────────────────────────────────────┐  │
│ │ Skill Levels                    │ Recent Activity                     │  │
│ │                                 │                                     │  │
│ │ Python                          │ Today                               │  │
│ │ ████████████░░░░░ 75%           │ • Completed "Binary Search"         │  │
│ │                                 │                                     │  │
│ │ JavaScript                      │ Yesterday                           │  │
│ │ ████████░░░░░░░░░ 50%           │ • Started "Merge Sort"              │  │
│ │                                 │ • Earned "7-Day Streak" badge       │  │
│ │ Algorithms                      │                                     │  │
│ │ ██████████░░░░░░░ 60%           │ 2 days ago                          │  │
│ │                                 │ • Code review on "Portfolio Site"   │  │
│ │ Data Structures                 │                                     │  │
│ │ ████████░░░░░░░░░ 50%           │ [View All Activity]                 │  │
│ │                                 │                                     │  │
│ │ [View All Skills]               │                                     │  │
│ └─────────────────────────────────┴─────────────────────────────────────┘  │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Exercise History                                                        │ │
│ │ ┌─────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ [Chart: Exercises completed over time - Line graph]                 │ │ │
│ │ │                                                                      │ │ │
│ │ │  50 │                                                    ●          │ │ │
│ │ │  40 │                                          ●───●               │ │ │
│ │ │  30 │                                ●───●                         │ │ │
│ │ │  20 │                      ●───●                                   │ │ │
│ │ │  10 │            ●───●                                             │ │ │
│ │ │   0 └────────────────────────────────────────────────────────────  │ │ │
│ │ │     Jan    Feb    Mar    Apr    May    Jun    Jul                 │ │ │
│ │ └─────────────────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Profile Header
```yaml
container:
  background: linear-gradient(135deg, colors.primary.500, colors.primary.700)
  color: colors.text.light.inverse
  padding: spacing.8

avatar:
  width: 6rem (96px)
  height: 6rem (96px)
  border-radius: borderRadius.full
  border: 4px solid colors.neutral.0

name:
  font-size: typography.fontSizes.3xl
  font-weight: typography.fontWeights.bold
  margin-bottom: spacing.1

username:
  font-size: typography.fontSizes.lg
  opacity: 0.9

meta-info:
  font-size: typography.fontSizes.sm
  opacity: 0.8
  margin-top: spacing.2

edit-button:
  background: colors.neutral.0
  color: colors.primary.500
  padding: spacing.2 spacing.4
  border-radius: borderRadius.default
  font-size: typography.fontSizes.sm
  margin-top: spacing.4
```

#### Tabs
```yaml
container:
  background: colors.background.light.primary
  border-bottom: 2px solid colors.neutral.200

tab:
  padding: spacing.4 spacing.6
  font-size: typography.fontSizes.base
  font-weight: typography.fontWeights.medium
  color: colors.text.light.secondary
  border-bottom: 2px solid transparent
  margin-bottom: -2px

  hover:
    color: colors.text.light.primary

  active:
    color: colors.primary.500
    border-bottom-color: colors.primary.500
```

#### Stat Card
```yaml
container:
  text-align: center
  padding: spacing.6
  background: colors.background.light.primary
  border: 1px solid colors.neutral.200
  border-radius: borderRadius.lg

icon:
  font-size: typography.fontSizes.3xl
  margin-bottom: spacing.2

value:
  font-size: typography.fontSizes.3xl
  font-weight: typography.fontWeights.bold
  color: colors.primary.500

label:
  font-size: typography.fontSizes.sm
  color: colors.text.light.secondary
  margin-top: spacing.1
```

#### Skill Progress Bar
```yaml
container:
  margin-bottom: spacing.4

label:
  font-size: typography.fontSizes.sm
  font-weight: typography.fontWeights.medium
  color: colors.text.light.primary
  margin-bottom: spacing.2

bar-background:
  height: 0.5rem (8px)
  background: colors.neutral.200
  border-radius: borderRadius.full
  overflow: hidden

bar-fill:
  height: 100%
  background: colors.primary.500
  border-radius: borderRadius.full
  transition: width transitions.duration.slow transitions.timing.easeOut

percentage:
  font-size: typography.fontSizes.xs
  color: colors.text.light.tertiary
  margin-left: spacing.2
```

### Mobile Layout

```
┌─────────────────────────────┐
│ [PROFILE HEADER]            │
│ ┌───┐ John Doe              │
│ │AVA│ @johndoe              │
│ └───┘ Member since Jan 2025 │
│       [Edit Profile]        │
├─────────────────────────────┤
│ [TABS - Horizontal Scroll]  │
│ Overview │ Progress │ ...   │
├─────────────────────────────┤
│ ┌─────────────────────────┐ │
│ │ 🔥 7  📚 42  ⏱️ 24h     │ │
│ └─────────────────────────┘ │
│                             │
│ Skill Levels                │
│ Python       ████████ 75%   │
│ JavaScript   ████░░░░ 50%   │
│ [View All]                  │
│                             │
│ Recent Activity             │
│ • Completed exercise        │
│ • Earned badge              │
│ [View All]                  │
└─────────────────────────────┘
```

---

## 5. Authentication Screens

### Registration

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              [LOGO - CodeMentor]                            │
│                                                             │
│         Start Your Coding Journey Today                     │
│         Learn to code with personalized AI tutoring         │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Create Your Account                                   │  │
│  │                                                       │  │
│  │ [Full Name                                        ]   │  │
│  │                                                       │  │
│  │ [Email Address                                    ]   │  │
│  │                                                       │  │
│  │ [Password                                         ]   │  │
│  │ ●●●●●●●●                                           │  │
│  │ ℹ️ At least 12 characters, mixed case, numbers      │  │
│  │                                                       │  │
│  │ [Confirm Password                                 ]   │  │
│  │                                                       │  │
│  │ ☐ I agree to the Terms of Service and Privacy Policy│  │
│  │                                                       │  │
│  │ [          Create Account          ]                 │  │
│  │                                                       │  │
│  │ ─────────────── OR ───────────────                   │  │
│  │                                                       │  │
│  │ [   🐙 Continue with GitHub    ]                     │  │
│  │ [   🔍 Continue with Google    ]                     │  │
│  │                                                       │  │
│  │ Already have an account? [Sign In]                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Login

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              [LOGO - CodeMentor]                            │
│                                                             │
│              Welcome Back!                                  │
│              Continue your learning journey                 │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Sign In                                               │  │
│  │                                                       │  │
│  │ [Email Address                                    ]   │  │
│  │                                                       │  │
│  │ [Password                                         ]   │  │
│  │                                                       │  │
│  │ ☐ Remember me        [Forgot password?]              │  │
│  │                                                       │  │
│  │ [          Sign In          ]                         │  │
│  │                                                       │  │
│  │ ─────────────── OR ───────────────                   │  │
│  │                                                       │  │
│  │ [   🐙 Continue with GitHub    ]                     │  │
│  │ [   🔍 Continue with Google    ]                     │  │
│  │                                                       │  │
│  │ Don't have an account? [Create Account]              │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Auth Form Container
```yaml
container:
  max-width: 28rem (448px)
  margin: 0 auto
  padding: spacing.8
  background: colors.background.light.primary
  border-radius: borderRadius.xl
  box-shadow: shadows.lg

logo:
  text-align: center
  margin-bottom: spacing.8

heading:
  font-size: typography.fontSizes.3xl
  font-weight: typography.fontWeights.bold
  text-align: center
  color: colors.text.light.primary
  margin-bottom: spacing.2

subheading:
  font-size: typography.fontSizes.base
  text-align: center
  color: colors.text.light.secondary
  margin-bottom: spacing.8
```

#### Form Input
```yaml
label:
  font-size: typography.fontSizes.sm
  font-weight: typography.fontWeights.medium
  color: colors.text.light.primary
  margin-bottom: spacing.2

input:
  width: 100%
  padding: spacing.3
  border: 1px solid colors.neutral.300
  border-radius: borderRadius.default
  font-size: typography.fontSizes.base

  focus:
    border-color: colors.primary.500
    outline: none
    box-shadow: shadows.focus

  error:
    border-color: colors.semantic.error.default

helper-text:
  font-size: typography.fontSizes.xs
  color: colors.text.light.tertiary
  margin-top: spacing.1

error-text:
  font-size: typography.fontSizes.xs
  color: colors.semantic.error.default
  margin-top: spacing.1
```

#### OAuth Buttons
```yaml
button:
  width: 100%
  display: flex
  align-items: center
  justify-content: center
  gap: spacing.2
  padding: spacing.3
  border: 1px solid colors.neutral.300
  border-radius: borderRadius.default
  background: colors.background.light.primary
  color: colors.text.light.primary
  font-size: typography.fontSizes.base
  margin-bottom: spacing.2

  hover:
    background: colors.neutral.50
    border-color: colors.neutral.400
```

---

## 6. Onboarding Interview

### Step 1: Language Selection

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│         Let's personalize your learning experience          │
│                                                             │
│         ●──○──○──○──○                                       │
│         Step 1 of 5                                         │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ What programming language would you like to learn?    │  │
│  │                                                       │  │
│  │ ┌─────────────┬─────────────┬─────────────┐          │  │
│  │ │   🐍        │    JS       │    ☕       │          │  │
│  │ │  Python     │ JavaScript  │   Java      │          │  │
│  │ │             │             │             │          │  │
│  │ │ [  Select ] │ [  Select ] │ [  Select ] │          │  │
│  │ └─────────────┴─────────────┴─────────────┘          │  │
│  │                                                       │  │
│  │ ┌─────────────┬─────────────┬─────────────┐          │  │
│  │ │   C++       │    Go       │   Rust      │          │  │
│  │ │             │             │             │          │  │
│  │ │ [  Select ] │ [  Select ] │ [  Select ] │          │  │
│  │ └─────────────┴─────────────┴─────────────┘          │  │
│  │                                                       │  │
│  │ ℹ️ Don't worry, you can learn multiple languages later │  │
│  │                                                       │  │
│  │                           [Next →]                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│              [← Skip for now]                               │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Skill Level

```
┌─────────────────────────────────────────────────────────────┐
│         Let's personalize your learning experience          │
│                                                             │
│         ●──●──○──○──○                                       │
│         Step 2 of 5                                         │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ What's your current Python skill level?               │  │
│  │                                                       │  │
│  │ ◯ Beginner                                            │  │
│  │   I'm just starting out                               │  │
│  │                                                       │  │
│  │ ◯ Intermediate                                        │  │
│  │   I know the basics and want to improve              │  │
│  │                                                       │  │
│  │ ◯ Advanced                                            │  │
│  │   I'm comfortable with complex concepts               │  │
│  │                                                       │  │
│  │                    [← Back]  [Next →]                 │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Progress Indicator
```yaml
container:
  display: flex
  align-items: center
  justify-content: center
  gap: spacing.2
  margin-bottom: spacing.6

step-circle:
  width: 0.75rem (12px)
  height: 0.75rem (12px)
  border-radius: borderRadius.full

  completed:
    background: colors.primary.500

  current:
    background: colors.primary.500
    box-shadow: 0 0 0 4px colors.primary.100

  upcoming:
    background: colors.neutral.300

connector:
  width: 2rem (32px)
  height: 2px
  background: colors.neutral.300
```

#### Language Selection Card
```yaml
card:
  border: 2px solid colors.neutral.200
  border-radius: borderRadius.lg
  padding: spacing.6
  text-align: center
  cursor: pointer

  hover:
    border-color: colors.primary.300
    background: colors.primary.50

  selected:
    border-color: colors.primary.500
    background: colors.primary.50

icon:
  font-size: typography.fontSizes.4xl
  margin-bottom: spacing.3

label:
  font-size: typography.fontSizes.lg
  font-weight: typography.fontWeights.semibold
  color: colors.text.light.primary
```

---

## 7. Community Page

### Desktop Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [HEADER]                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ [COMMUNITY PAGE]                                                            │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ Study Groups & Community                          [Search rooms...]  🔍 │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ [Filter: All | Python | JavaScript | Algorithms | Projects]            │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ [ROOM LIST - Left Sidebar]                                              │ │
│ │                                                                         │ │
│ │ ┌─────────────────────────────────────────┐                            │ │
│ │ │ 🐍 Python Learners                      │ [Active Chat Window]       │ │
│ │ │ 142 members • 23 online                 │                            │ │
│ │ │ Last message: 2 min ago                 │ Python Learners            │ │
│ │ └─────────────────────────────────────────┘ ━━━━━━━━━━━━━━━━━━         │ │
│ │                                             │                          │ │
│ │ ┌─────────────────────────────────────────┐ │ Messages...              │ │
│ │ │ 🚀 Beginner's Corner                    │ │                          │ │
│ │ │ 89 members • 15 online                  │ │ [User messages here]     │ │
│ │ │ Last message: 5 min ago                 │ │                          │ │
│ │ └─────────────────────────────────────────┘ │                          │ │
│ │                                             │                          │ │
│ │ ┌─────────────────────────────────────────┐ │                          │ │
│ │ │ 🧮 Algorithms Study Group               │ │                          │ │
│ │ │ 56 members • 8 online                   │ │                          │ │
│ │ │ Last message: 12 min ago                │ │                          │ │
│ │ └─────────────────────────────────────────┘ ━━━━━━━━━━━━━━━━━━         │ │
│ │                                             │ [Input message...]       │ │
│ │ [Show more rooms...]                        └──────────────────────────┘ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Room Card
```yaml
card:
  padding: spacing.4
  border: 1px solid colors.neutral.200
  border-radius: borderRadius.lg
  margin-bottom: spacing.3
  cursor: pointer

  hover:
    background: colors.neutral.50
    border-color: colors.neutral.300

  active:
    background: colors.primary.50
    border-color: colors.primary.500

icon:
  font-size: typography.fontSizes.xl
  margin-right: spacing.3

title:
  font-size: typography.fontSizes.lg
  font-weight: typography.fontWeights.semibold
  color: colors.text.light.primary
  margin-bottom: spacing.1

metadata:
  font-size: typography.fontSizes.sm
  color: colors.text.light.secondary
  display: flex
  gap: spacing.2
  align-items: center
```

---

## 8. Settings

### Settings Page

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [HEADER]                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ [SETTINGS]                                                                  │
│                                                                             │
│ ┌─────────────────────┬─────────────────────────────────────────────────┐  │
│ │ [SIDEBAR MENU]      │ [SETTINGS CONTENT]                              │  │
│ │                     │                                                 │  │
│ │ Profile             │ Profile Settings                                │  │
│ │ Account             │                                                 │  │
│ │ Preferences         │ [Avatar Upload]                                 │  │
│ │ Notifications       │ ┌─────┐                                         │  │
│ │ Privacy             │ │ AVA │ [Change Photo]                          │  │
│ │ Appearance          │ └─────┘                                         │  │
│ │                     │                                                 │  │
│ │                     │ Full Name                                       │  │
│ │                     │ [John Doe                                    ]  │  │
│ │                     │                                                 │  │
│ │                     │ Bio                                             │  │
│ │                     │ [                                             ] │  │
│ │                     │ [                                             ] │  │
│ │                     │                                                 │  │
│ │                     │ Learning Goals                                  │  │
│ │                     │ [Become a full-stack developer               ]  │  │
│ │                     │                                                 │  │
│ │                     │ Preferred Languages                             │  │
│ │                     │ ☑ Python  ☑ JavaScript  ☐ Java                │  │
│ │                     │                                                 │  │
│ │                     │ [Save Changes]  [Cancel]                        │  │
│ └─────────────────────┴─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Responsive Design Notes

### Mobile-First Approach
All layouts are designed mobile-first with progressive enhancement for larger screens.

### Breakpoint Strategy
- **Mobile (< 640px)**: Single column, stacked elements, collapsed navigation
- **Tablet (640px - 1024px)**: 2-column grid where appropriate, expanded navigation
- **Desktop (> 1024px)**: Full layout with sidebars, multi-column grids

### Touch Optimization
- All interactive elements minimum 44x44px
- Adequate spacing between clickable elements (8px minimum)
- Swipe gestures for navigation on mobile
- Pull-to-refresh on mobile

---

## Accessibility Notes

### Screen Reader Support
- All interactive elements have proper ARIA labels
- Landmarks defined (header, main, nav, aside, footer)
- Skip links for keyboard navigation
- Live regions for dynamic content updates

### Keyboard Navigation
- Tab order follows visual flow
- All interactive elements keyboard accessible
- Visible focus indicators
- Escape key closes modals/dropdowns

### Color Contrast
- All text meets WCAG 2.1 AA standards (4.5:1 minimum)
- UI components meet 3.0:1 contrast minimum
- Color never used as sole indicator

---

## Implementation Notes for AI Agents

### Component Hierarchy
```
Dashboard
├── Header
│   ├── Logo
│   ├── Navigation
│   └── UserMenu
├── MainContent
│   ├── DailyExerciseCard
│   ├── ContinueLearning
│   └── QuickActions
└── Sidebar
    ├── QuickStats
    ├── ProgressWidget
    ├── SkillLevels
    └── Achievements
```

### State Management
Each screen requires state for:
- User data (profile, progress, preferences)
- Loading states (skeleton screens)
- Error states (error messages with retry)
- Empty states (helpful guidance)

### Data Fetching
- Initial page load: Fetch all necessary data
- Lazy load: Activity feed, exercise history
- Real-time: Chat messages, notifications
- Cache: User profile, achievements

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial wireframe documentation |

---

## Related Documents

- `design-system.md` - Design system guidelines
- `design-tokens.json` - Machine-readable design tokens
- `components.md` - Component library specifications
- `user-flows.md` - User journey diagrams

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-12-05
**Maintained by**: Design System Engineer (AI Agent)
