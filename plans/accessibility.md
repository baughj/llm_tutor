# CodeMentor Accessibility Guidelines
## WCAG 2.1 Level AA Compliance
## Version 1.0.0 | Date: 2025-12-05

---

## Document Purpose

This document provides comprehensive accessibility guidelines for the CodeMentor platform to ensure **WCAG 2.1 Level AA compliance**. All guidelines are **machine-readable** and formatted for AI agent implementation (particularly Claude Code).

This document covers:
1. **WCAG 2.1 AA requirements** and implementation
2. **Perceivable** guidelines (visual and auditory accessibility)
3. **Operable** guidelines (keyboard and interaction accessibility)
4. **Understandable** guidelines (clarity and predictability)
5. **Robust** guidelines (compatibility and reliability)
6. **Testing procedures** and checklists

---

## Table of Contents

1. [WCAG 2.1 AA Overview](#1-wcag-21-aa-overview)
2. [Perceivable](#2-perceivable)
3. [Operable](#3-operable)
4. [Understandable](#4-understandable)
5. [Robust](#5-robust)
6. [Component-Specific Guidelines](#6-component-specific-guidelines)
7. [Testing & Validation](#7-testing--validation)

---

## 1. WCAG 2.1 AA Overview

### Success Criteria Summary

```yaml
wcag-level: AA
version: 2.1
compliance-target: All components and pages

principle-summary:
  1-perceivable:
    description: Information and UI must be presentable to users in ways they can perceive
    criteria-count: 22

  2-operable:
    description: UI components and navigation must be operable
    criteria-count: 20

  3-understandable:
    description: Information and UI operation must be understandable
    criteria-count: 17

  4-robust:
    description: Content must be robust enough for assistive technologies
    criteria-count: 3
```

### Conformance Levels

```yaml
conformance:
  level-a:
    description: Minimum level (must meet all Level A criteria)
    status: Required

  level-aa:
    description: Mid-level (must meet all Level A + AA criteria)
    status: Required (our target)

  level-aaa:
    description: Highest level
    status: Optional (enhanced features)
```

---

## 2. Perceivable

### 2.1 Text Alternatives (WCAG 1.1)

#### 1.1.1 Non-text Content (Level A)

```yaml
guideline: Provide text alternatives for non-text content

images:
  decorative:
    alt: "" (empty string)
    aria-hidden: true
    example: Background patterns, dividers

  informative:
    alt: Descriptive text explaining the image
    example: "Graph showing user progress over 30 days"

  functional:
    alt: Description of function
    example: "Close modal" for X button

  complex:
    alt: Brief description
    aria-describedby: ID of detailed description
    example: Charts, diagrams, infographics

icons:
  decorative:
    aria-hidden: true

  functional:
    aria-label: Description of action
    example:
      <button aria-label="Search">
        <svg aria-hidden="true">...</svg>
      </button>

code-examples:
  # Decorative image
  <img src="divider.svg" alt="" aria-hidden="true" />

  # Informative image
  <img src="progress-chart.png" alt="Bar chart showing 70% completion rate" />

  # Functional icon button
  <button aria-label="Close dialog">
    <svg aria-hidden="true">
      <use href="#icon-close" />
    </svg>
  </button>
```

### 2.2 Adaptable (WCAG 1.3)

#### 1.3.1 Info and Relationships (Level A)

```yaml
guideline: Ensure information structure is preserved

semantic-html:
  headings:
    - Use h1-h6 in hierarchical order
    - Only one h1 per page
    - Don't skip heading levels
    example: h1 → h2 → h3 (correct)
    not: h1 → h3 (incorrect)

  lists:
    ordered: <ol> for sequential steps
    unordered: <ul> for non-sequential items
    description: <dl> for term-definition pairs

  tables:
    structure:
      - <table> for tabular data only
      - <thead>, <tbody>, <tfoot> for structure
      - <th> for headers with scope attribute
      - <caption> for table description
    example:
      <table>
        <caption>User progress summary</caption>
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">Exercises</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2025-12-01</td>
            <td>3</td>
          </tr>
        </tbody>
      </table>

  forms:
    labels:
      - Every input must have associated label
      - Use <label for="id"> or aria-label
      - Group related inputs with <fieldset> and <legend>
    example:
      <fieldset>
        <legend>Contact Information</legend>
        <label for="email">Email</label>
        <input id="email" type="email" />
      </fieldset>

  landmarks:
    - <header> or role="banner"
    - <nav> or role="navigation"
    - <main> or role="main"
    - <aside> or role="complementary"
    - <footer> or role="contentinfo"
```

#### 1.3.2 Meaningful Sequence (Level A)

```yaml
guideline: Ensure logical reading order

reading-order:
  - DOM order matches visual order
  - Flexbox/Grid: Use order property carefully
  - Tabindex: Don't create illogical tab order
  - Screen readers: Follow DOM order

css-caution:
  position-absolute: Can disrupt reading order
  flexbox-order: Changes visual not DOM order
  float: Can create confusion
```

#### 1.3.3 Sensory Characteristics (Level A)

```yaml
guideline: Don't rely solely on sensory characteristics

avoid:
  - "Click the red button" (color only)
  - "Use the button on the right" (position only)
  - "Click the round icon" (shape only)

instead:
  - "Click the red Submit button"
  - "Use the Save button (located in the top right)"
  - "Click the round Settings icon (gear shape)"
```

### 2.3 Distinguishable (WCAG 1.4)

#### 1.4.3 Contrast (Minimum) (Level AA)

```yaml
guideline: Ensure sufficient color contrast

minimum-contrast:
  normal-text:
    ratio: 4.5:1
    applies-to: Text < 18pt or < 14pt bold
    example:
      text: colors.neutral.900 (#111827)
      background: colors.neutral.0 (#FFFFFF)
      ratio: 16.1:1 ✓

  large-text:
    ratio: 3.0:1
    applies-to: Text ≥ 18pt or ≥ 14pt bold
    example:
      text: colors.neutral.700 (#374151)
      background: colors.neutral.0 (#FFFFFF)
      ratio: 10.8:1 ✓

  ui-components:
    ratio: 3.0:1
    applies-to: Borders, icons, focus indicators
    example:
      border: colors.neutral.300 (#D1D5DB)
      background: colors.neutral.0 (#FFFFFF)
      ratio: 4.6:1 ✓

exceptions:
  - Disabled states (no contrast requirement)
  - Logos
  - Decorative elements (no information conveyed)

color-combinations:
  approved:
    - primary-500 on white: 7.5:1 ✓
    - neutral-900 on white: 16.1:1 ✓
    - neutral-700 on white: 10.8:1 ✓
    - white on primary-500: 7.5:1 ✓

  avoid:
    - neutral-300 text on white: 2.1:1 ✗
    - primary-200 on white: 1.9:1 ✗
```

#### 1.4.4 Resize Text (Level AA)

```yaml
guideline: Text can be resized up to 200% without loss of content or functionality

implementation:
  - Use relative units (rem, em) not px
  - Test at 200% zoom
  - Ensure no horizontal scrolling
  - Content doesn't overlap

  base-font-size: 16px
  scaling:
    100%: 1rem = 16px
    150%: 1rem = 24px
    200%: 1rem = 32px

  breakpoints:
    - Adjust breakpoints if needed at 200% zoom
    - Ensure mobile breakpoint at desktop 200% zoom
```

#### 1.4.5 Images of Text (Level AA)

```yaml
guideline: Use actual text rather than images of text

exceptions:
  - Logos (brand identity)
  - Graphs/charts (if alt text provides same info)
  - Screenshots (for documentation)

preferred:
  # Use styled HTML text
  <h1 style="font-family: custom-font;">Heading</h1>

avoid:
  # Image of text
  <img src="heading.png" alt="Heading" />
```

#### 1.4.10 Reflow (Level AA)

```yaml
guideline: Content reflows without horizontal scrolling at 320px width

requirements:
  - No horizontal scrolling at 320x256 CSS pixels
  - Responsive design required
  - Mobile-first approach

exceptions:
  - Data tables (may scroll horizontally)
  - Code editors
  - Toolbars with many icons

implementation:
  - Use responsive breakpoints
  - Flexible grid layouts
  - Avoid fixed widths
  - Test at 400% zoom (equivalent to 320px wide)
```

#### 1.4.11 Non-text Contrast (Level AA)

```yaml
guideline: UI components and graphics have 3:1 contrast ratio

applies-to:
  - Graphical objects (icons, charts)
  - User interface components (buttons, inputs, focus indicators)
  - States (hover, focus, active)

examples:
  button-border:
    color: colors.primary.500
    background: colors.neutral.0
    ratio: 7.5:1 ✓

  input-border:
    color: colors.neutral.300
    background: colors.neutral.0
    ratio: 4.6:1 ✓

  focus-indicator:
    color: colors.primary.500
    background: colors.neutral.0
    ratio: 7.5:1 ✓
```

#### 1.4.12 Text Spacing (Level AA)

```yaml
guideline: No loss of content when users adjust text spacing

user-adjustments:
  line-height: 1.5× font size
  paragraph-spacing: 2× font size
  letter-spacing: 0.12× font size
  word-spacing: 0.16× font size

implementation:
  - Don't use absolute positioning for text
  - Allow text to expand
  - Test with text spacing bookmarklet
  - Ensure no overlapping content
```

#### 1.4.13 Content on Hover or Focus (Level AA)

```yaml
guideline: Hovering/focusing reveals additional content with proper controls

requirements:
  dismissible: User can dismiss without moving pointer/focus (ESC key)
  hoverable: Pointer can move over revealed content without it disappearing
  persistent: Content remains visible until dismissed or no longer relevant

examples:
  tooltip:
    trigger: hover or focus
    dismiss: ESC key or click outside
    hover: Pointer can move over tooltip
    delay: 200ms before showing, 500ms before hiding

  dropdown:
    trigger: click or Enter key
    dismiss: ESC key or click outside
    hover: Can navigate within dropdown
    keyboard: Arrow keys for navigation
```

---

## 3. Operable

### 3.1 Keyboard Accessible (WCAG 2.1)

#### 2.1.1 Keyboard (Level A)

```yaml
guideline: All functionality available via keyboard

keyboard-navigation:
  tab: Move forward through interactive elements
  shift-tab: Move backward
  enter: Activate buttons, links
  space: Activate buttons, checkboxes, toggle states
  arrow-keys: Navigate within components (tabs, dropdowns, radios)
  escape: Close modals, dismiss menus, cancel actions
  home: Jump to first item in list
  end: Jump to last item in list

focusable-elements:
  native:
    - <a href="...">
    - <button>
    - <input>
    - <select>
    - <textarea>

  custom:
    - Add tabindex="0" for custom interactive elements
    - Use role attribute (button, link, etc.)
    - Implement keyboard event handlers

  avoid:
    - tabindex > 0 (creates illogical tab order)
    - <div onclick> without keyboard support

example:
  # Custom button
  <div
    role="button"
    tabindex="0"
    onClick={handleClick}
    onKeyDown={(e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        handleClick();
      }
    }}
  >
    Click me
  </div>
```

#### 2.1.2 No Keyboard Trap (Level A)

```yaml
guideline: Keyboard focus can always be moved away from any component

requirements:
  - User can navigate out of all components
  - No infinite loops in tab order
  - Modals: ESC key to close
  - Custom widgets: Provide exit mechanism

modal-pattern:
  open:
    - Move focus to first focusable element in modal
    - Trap focus within modal (loop tab order)
    - ESC key to close
  close:
    - Return focus to trigger element
    - Remove focus trap
```

#### 2.1.4 Character Key Shortcuts (Level A)

```yaml
guideline: If single character shortcuts exist, provide controls

requirements:
  - Can be turned off
  - Can be remapped
  - Only active when component has focus

example:
  # Good: Only active in code editor
  code-editor:
    shortcuts:
      "/": Toggle comment (only when editor focused)
      "ctrl+s": Save (modifier key required)

  # Avoid: Global single-key shortcuts
  avoid:
    "s": Search (conflicts with typing)
```

### 3.2 Enough Time (WCAG 2.2)

#### 2.2.1 Timing Adjustable (Level A)

```yaml
guideline: Provide user control over time limits

requirements:
  - Turn off time limit
  - Adjust time limit (minimum 10× original)
  - Extend before expiration (at least 20 seconds warning)

implementation:
  session-timeout:
    default: 30 minutes
    warning: 2 minutes before timeout
    actions:
      - Extend session
      - Log out
      - Return to work (auto-extend)

  exercise-timer:
    default: No time limit
    optional: User can set personal timer
    dismissible: Can be turned off
```

#### 2.2.2 Pause, Stop, Hide (Level A)

```yaml
guideline: User can control moving, blinking, scrolling, or auto-updating content

requirements:
  moving/blinking/scrolling:
    - Auto-starts
    - Lasts more than 5 seconds
    - Presented in parallel with other content
    - Must provide pause, stop, or hide mechanism

  auto-updating:
    - Auto-starts
    - Presented in parallel with other content
    - Must provide pause, stop, hide, or frequency control

examples:
  chat-messages:
    auto-scroll: Yes (new messages)
    control: User can scroll up (disables auto-scroll)
    resume: Scroll to bottom re-enables auto-scroll

  loading-spinner:
    duration: < 5 seconds (no control needed)

  progress-updates:
    auto-update: Yes
    control: Pause button available
```

### 3.3 Navigable (WCAG 2.4)

#### 2.4.1 Bypass Blocks (Level A)

```yaml
guideline: Provide mechanism to bypass repeated content

skip-links:
  placement: First focusable element on page
  destination: Main content area
  visibility: Visible on focus
  keyboard: Tab to access, Enter to activate

example:
  <a href="#main-content" class="skip-link">
    Skip to main content
  </a>

  <main id="main-content" tabindex="-1">
    <!-- Main content -->
  </main>

landmarks:
  - Use HTML5 semantic elements
  - Screen readers can navigate by landmark
  - Provides implicit skip functionality
```

#### 2.4.2 Page Titled (Level A)

```yaml
guideline: Pages have descriptive titles

format: "{Specific} - {General} - CodeMentor"

examples:
  - "Binary Search Exercise - Python - CodeMentor"
  - "Dashboard - CodeMentor"
  - "Profile Settings - CodeMentor"
  - "Chat with Tutor - CodeMentor"

implementation:
  <title>{pageTitle} - CodeMentor</title>

  # Update on route change (SPA)
  useEffect(() => {
    document.title = `${pageTitle} - CodeMentor`;
  }, [pageTitle]);
```

#### 2.4.3 Focus Order (Level A)

```yaml
guideline: Focus order preserves meaning and operability

rules:
  - Tab order follows logical reading order
  - Related items grouped together
  - Primary actions before secondary
  - Don't use tabindex > 0

example:
  form-order:
    1. First name input
    2. Last name input
    3. Email input
    4. Submit button
    5. Cancel button

  modal-order:
    1. Close button (×)
    2. Modal content
    3. Primary action button
    4. Secondary action button
```

#### 2.4.4 Link Purpose (In Context) (Level A)

```yaml
guideline: Link purpose is clear from link text or context

good:
  - "Read our Privacy Policy"
  - "View exercise details"
  - "Edit profile"

avoid:
  - "Click here"
  - "Read more"
  - "Learn more"

context-example:
  # If "click here" is used, surrounding text provides context
  <p>
    To improve your coding skills, complete daily exercises.
    <a href="/exercises">Start learning</a>.
  </p>
```

#### 2.4.5 Multiple Ways (Level AA)

```yaml
guideline: Provide multiple ways to locate pages

implementations:
  - Main navigation menu
  - Search functionality
  - Site map
  - Breadcrumbs
  - Related links

example:
  finding-exercises:
    - Navigation: Dashboard → Exercises
    - Search: "Binary search exercise"
    - Breadcrumbs: Home → Python → Algorithms → Binary Search
    - Recent: "Continue from yesterday"
```

#### 2.4.6 Headings and Labels (Level AA)

```yaml
guideline: Headings and labels describe topic or purpose

headings:
  - Descriptive and unique
  - Logical hierarchy
  - Indicate structure

labels:
  - Clear and concise
  - Describe purpose of input
  - Associated with input (for attribute)

examples:
  headings:
    good: "Daily Python Exercise"
    avoid: "Exercise"

  labels:
    good: <label for="email">Email Address</label>
    avoid: <label for="email">Input</label>
```

#### 2.4.7 Focus Visible (Level AA)

```yaml
guideline: Keyboard focus indicator is visible

requirements:
  - Visual indicator when element has focus
  - Sufficient contrast (3:1 minimum)
  - Clear differentiation from other states

implementation:
  default-focus:
    outline: 2px solid colors.primary.500
    outline-offset: 2px
    border-radius: borderRadius.sm

  button-focus:
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.4)
    outline: none (replaced by box-shadow)

  input-focus:
    border-color: colors.primary.500
    box-shadow: shadows.focus

css-example:
  *:focus-visible {
    outline: 2px solid #0066CC;
    outline-offset: 2px;
  }

  button:focus-visible {
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.4);
  }
```

### 3.4 Input Modalities (WCAG 2.5)

#### 2.5.1 Pointer Gestures (Level A)

```yaml
guideline: Functionality doesn't require path-based or multipoint gestures

avoid:
  - Swipe gestures without alternative
  - Pinch-to-zoom without + / - buttons
  - Complex paths (drawing shapes)

provide:
  - Simple clicks/taps
  - Single-point activation
  - Alternative controls

example:
  carousel:
    swipe: Optional gesture
    alternative: Prev/Next buttons
```

#### 2.5.2 Pointer Cancellation (Level A)

```yaml
guideline: Prevent accidental activation

requirements:
  - Click event on mouse up, not down
  - Ability to abort (move pointer away before release)
  - Undo mechanism for irreversible actions

implementation:
  onClick: Fires on mouse up
  onMouseDown: Avoid for critical actions

exception:
  - Piano keyboard app (needs mousedown)
  - Drag and drop (different interaction)
```

#### 2.5.3 Label in Name (Level A)

```yaml
guideline: Accessible name includes visible text label

rule: If there's visible text, it should be in the accessible name

good:
  <button aria-label="Search">Search</button>
  <button>Search</button>

avoid:
  # Visible "Search" but aria-label doesn't include it
  <button aria-label="Find">Search</button>

implementation:
  - Use visible text as aria-label
  - Or let browser use visible text
  - If adding to visible text, include it
```

#### 2.5.4 Motion Actuation (Level A)

```yaml
guideline: Functionality operated by motion can also be operated by UI

requirements:
  - Don't require device motion (shake, tilt)
  - Provide UI alternative
  - Allow disabling motion activation

example:
  shake-to-undo:
    motion: Shake device to undo
    alternative: Undo button in UI
    settings: Option to disable shake
```

---

## 4. Understandable

### 4.1 Readable (WCAG 3.1)

#### 3.1.1 Language of Page (Level A)

```yaml
guideline: Set page language

implementation:
  <html lang="en">

  # If content in multiple languages
  <html lang="en">
    <p>English content</p>
    <p lang="es">Contenido en español</p>
  </html>
```

#### 3.1.2 Language of Parts (Level AA)

```yaml
guideline: Identify language changes within content

implementation:
  <p>
    This is English.
    <span lang="fr">Ceci est en français.</span>
    Back to English.
  </p>
```

### 4.2 Predictable (WCAG 3.2)

#### 3.2.1 On Focus (Level A)

```yaml
guideline: Receiving focus doesn't trigger unexpected changes

avoid:
  - Auto-submit on focus
  - Open modal on focus
  - Navigate to new page on focus

allowed:
  - Show tooltip on focus
  - Highlight related content
  - Display helper text
```

#### 3.2.2 On Input (Level A)

```yaml
guideline: Changing input doesn't cause unexpected changes

avoid:
  - Auto-submit on change
  - Auto-navigate on select
  - Auto-delete on typing

allowed:
  - Show password strength
  - Filter results as typing
  - Update preview

provide:
  - Explicit submit button
  - Warning before navigation
  - Clear indication of auto-actions
```

#### 3.2.3 Consistent Navigation (Level AA)

```yaml
guideline: Navigation is in same order across pages

requirements:
  - Navigation menu in same order
  - Same relative position on pages
  - Same structure and labels

implementation:
  header-nav:
    order:
      - Logo (left)
      - Dashboard
      - Community
      - Mentorship
      - User Menu (right)

  # Same order on all pages
```

#### 3.2.4 Consistent Identification (Level AA)

```yaml
guideline: Components with same function have consistent labels

examples:
  search-icon:
    - Always labeled "Search"
    - Same icon across all pages
    - Same behavior everywhere

  save-button:
    - Always labeled "Save" or "Save Changes"
    - Not "Submit" on one page, "Save" on another
```

### 4.3 Input Assistance (WCAG 3.3)

#### 3.3.1 Error Identification (Level A)

```yaml
guideline: Clearly identify input errors

requirements:
  - Error message in text
  - Identify which field has error
  - Explain the error

implementation:
  <label for="email">Email Address</label>
  <input
    id="email"
    type="email"
    aria-invalid="true"
    aria-describedby="email-error"
  />
  <span id="email-error" role="alert">
    Please enter a valid email address
  </span>

styling:
  border-color: colors.semantic.error.default
  icon: Error icon (with aria-hidden="true")
  text-color: colors.semantic.error.default
```

#### 3.3.2 Labels or Instructions (Level A)

```yaml
guideline: Provide labels or instructions for user input

requirements:
  - Every input has label
  - Complex inputs have instructions
  - Required fields indicated

examples:
  simple:
    <label for="name">Name</label>
    <input id="name" required />

  complex:
    <label for="password">Password</label>
    <span id="password-help">
      Must be at least 12 characters with mixed case,
      numbers, and symbols
    </span>
    <input
      id="password"
      type="password"
      required
      aria-describedby="password-help"
    />

  required:
    <label for="email">
      Email Address <span aria-label="required">*</span>
    </label>
```

#### 3.3.3 Error Suggestion (Level AA)

```yaml
guideline: Suggest corrections for input errors

examples:
  email-format:
    error: "Email must be in format: user@example.com"
    suggestion: "Did you mean: user@gmail.com?"

  password-strength:
    error: "Password is too weak"
    suggestion: "Add numbers and symbols to strengthen"

  date-format:
    error: "Invalid date format"
    suggestion: "Use format: MM/DD/YYYY"
```

#### 3.3.4 Error Prevention (Legal, Financial, Data) (Level AA)

```yaml
guideline: Prevent errors in critical transactions

requirements:
  - Reversible: User can undo
  - Checked: Data is validated
  - Confirmed: User confirms before final submission

implementation:
  delete-account:
    step-1: Click "Delete Account"
    step-2: Show confirmation modal
    step-3: Type "DELETE" to confirm
    step-4: Final confirmation button
    step-5: Send confirmation email

  payment:
    step-1: Enter payment details
    step-2: Review order summary
    step-3: Confirm purchase
    step-4: Email receipt
```

---

## 5. Robust

### 5.1 Compatible (WCAG 4.1)

#### 4.1.2 Name, Role, Value (Level A)

```yaml
guideline: All UI components have accessible name, role, and value

requirements:
  name: Accessible name (label, aria-label, aria-labelledby)
  role: Semantic HTML or ARIA role
  value: Current state (checked, selected, expanded)

examples:
  button:
    <button aria-label="Close">×</button>
    # name: "Close", role: "button"

  checkbox:
    <input type="checkbox" id="agree" checked />
    <label for="agree">I agree</label>
    # name: "I agree", role: "checkbox", value: "checked"

  custom-toggle:
    <div
      role="switch"
      aria-checked="true"
      aria-label="Enable notifications"
      tabindex="0"
    >
      ...
    </div>
    # name: "Enable notifications"
    # role: "switch"
    # value: "checked"
```

#### 4.1.3 Status Messages (Level AA)

```yaml
guideline: Status messages are programmatically determinable

requirements:
  - Use role="status" for status messages
  - Use role="alert" for important messages
  - Use aria-live for dynamic updates

examples:
  success-message:
    <div role="status" aria-live="polite">
      Exercise completed successfully!
    </div>

  error-message:
    <div role="alert" aria-live="assertive">
      Failed to save. Please try again.
    </div>

  loading:
    <div role="status" aria-live="polite" aria-busy="true">
      Loading...
    </div>
```

---

## 6. Component-Specific Guidelines

### Buttons

```yaml
button-accessibility:
  semantic: Use <button> element
  label: Clear, descriptive text
  focus: Visible focus indicator
  keyboard: Activates with Enter or Space
  disabled: aria-disabled="true" + visual indication
  loading: aria-busy="true" + loading text

  icon-only:
    aria-label: Required
    example: <button aria-label="Close">×</button>
```

### Forms

```yaml
form-accessibility:
  labels:
    - Every input has associated label
    - Use <label for="id"> or aria-label
    - Labels are visible (not placeholder-only)

  fieldsets:
    - Group related inputs
    - Use <legend> to describe group

  validation:
    - Real-time validation with aria-invalid
    - Error messages with aria-describedby
    - Success indication

  required:
    - Visual indicator (*)
    - aria-required="true"
    - HTML required attribute

example:
  <form>
    <fieldset>
      <legend>Personal Information</legend>

      <label for="name">
        Name <span aria-label="required">*</span>
      </label>
      <input
        id="name"
        required
        aria-required="true"
        aria-invalid="false"
      />

      <label for="email">
        Email <span aria-label="required">*</span>
      </label>
      <input
        id="email"
        type="email"
        required
        aria-required="true"
        aria-invalid="false"
        aria-describedby="email-help"
      />
      <span id="email-help">
        We'll never share your email
      </span>
    </fieldset>

    <button type="submit">Submit</button>
  </form>
```

### Modals

```yaml
modal-accessibility:
  role: dialog or alertdialog
  aria-labelledby: ID of modal title
  aria-describedby: ID of modal description
  focus-trap: Tab loops within modal
  initial-focus: First focusable element
  close: ESC key + close button
  return-focus: Return to trigger on close

example:
  <div
    role="dialog"
    aria-labelledby="modal-title"
    aria-describedby="modal-description"
    aria-modal="true"
  >
    <h2 id="modal-title">Confirm Delete</h2>
    <p id="modal-description">
      Are you sure you want to delete this exercise?
    </p>
    <button onClick={handleDelete}>Delete</button>
    <button onClick={handleClose}>Cancel</button>
  </div>
```

### Navigation

```yaml
navigation-accessibility:
  semantic: <nav> or role="navigation"
  aria-label: Describe purpose
  current-page: aria-current="page"
  keyboard: Tab and arrow keys

example:
  <nav aria-label="Main navigation">
    <ul>
      <li>
        <a href="/dashboard" aria-current="page">
          Dashboard
        </a>
      </li>
      <li>
        <a href="/community">Community</a>
      </li>
    </ul>
  </nav>
```

### Tables

```yaml
table-accessibility:
  caption: Describe table purpose
  headers: <th> with scope attribute
  complex: Use headers and id for complex tables

example:
  <table>
    <caption>User exercise completion rates</caption>
    <thead>
      <tr>
        <th scope="col">User</th>
        <th scope="col">Completed</th>
        <th scope="col">Rate</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">John Doe</th>
        <td>42</td>
        <td>84%</td>
      </tr>
    </tbody>
  </table>
```

---

## 7. Testing & Validation

### Automated Testing Tools

```yaml
tools:
  axe-core:
    description: Accessibility testing engine
    usage: Browser extension or CI/CD integration
    coverage: ~57% of WCAG issues

  WAVE:
    description: Web accessibility evaluation tool
    usage: Browser extension
    coverage: Visual representation of issues

  Lighthouse:
    description: Chrome DevTools audit
    usage: Built into Chrome
    coverage: Basic accessibility checks

  Pa11y:
    description: Command-line accessibility tester
    usage: CI/CD integration
    coverage: Automated testing

command-line:
  # Run axe-core in CI
  npm install --save-dev axe-core
  npm run test:a11y

  # Run Pa11y
  npm install --save-dev pa11y
  pa11y https://example.com
```

### Manual Testing Checklist

```yaml
keyboard-testing:
  - [ ] Tab through all interactive elements
  - [ ] Activate buttons with Enter and Space
  - [ ] Navigate dropdowns with arrow keys
  - [ ] Close modals with ESC
  - [ ] Use skip links
  - [ ] Verify focus visible on all elements
  - [ ] Ensure no keyboard traps

screen-reader-testing:
  - [ ] Test with NVDA (Windows) or JAWS
  - [ ] Test with VoiceOver (macOS/iOS)
  - [ ] Test with TalkBack (Android)
  - [ ] Verify all images have alt text
  - [ ] Confirm form labels are announced
  - [ ] Check heading structure
  - [ ] Verify ARIA labels

visual-testing:
  - [ ] Check color contrast (all text and UI)
  - [ ] Test at 200% zoom
  - [ ] Verify focus indicators visible
  - [ ] Test with grayscale (color-blind simulation)
  - [ ] Check text spacing adjustments
  - [ ] Verify no horizontal scrolling at 320px

cognitive-testing:
  - [ ] Consistent navigation across pages
  - [ ] Clear error messages
  - [ ] Predictable interactions
  - [ ] No auto-playing content
  - [ ] Time limits adjustable
```

### Browser Extensions

```yaml
recommended-extensions:
  axe-devtools:
    browser: Chrome, Firefox, Edge
    features:
      - Automated scans
      - Intelligent guided tests
      - Issue highlighting

  wave:
    browser: Chrome, Firefox, Edge
    features:
      - Visual feedback
      - Color contrast analyzer
      - Structure visualization

  accessibility-insights:
    browser: Chrome, Edge
    features:
      - Fast Pass assessment
      - Tab stops visualization
      - Assessment workflow
```

### Compliance Checklist

```yaml
wcag-2.1-aa-checklist:
  perceivable:
    - [ ] Alt text for all images
    - [ ] Captions for video
    - [ ] Color contrast ≥ 4.5:1
    - [ ] Text resize up to 200%
    - [ ] Reflow at 320px
    - [ ] Non-text contrast ≥ 3:1
    - [ ] Text spacing adjustable
    - [ ] Hover/focus content dismissible

  operable:
    - [ ] All functionality keyboard accessible
    - [ ] No keyboard trap
    - [ ] Character key shortcuts controllable
    - [ ] Timing adjustable
    - [ ] Pause auto-updating content
    - [ ] Skip links present
    - [ ] Page titles descriptive
    - [ ] Focus order logical
    - [ ] Link purpose clear
    - [ ] Multiple ways to find pages
    - [ ] Headings and labels descriptive
    - [ ] Focus visible
    - [ ] Pointer gestures have alternatives
    - [ ] Pointer cancellation implemented
    - [ ] Label in name
    - [ ] Motion actuation has alternatives

  understandable:
    - [ ] Page language set
    - [ ] Language of parts set
    - [ ] No unexpected changes on focus
    - [ ] No unexpected changes on input
    - [ ] Consistent navigation
    - [ ] Consistent identification
    - [ ] Error identification clear
    - [ ] Labels or instructions provided
    - [ ] Error suggestions offered
    - [ ] Error prevention for critical actions

  robust:
    - [ ] Valid HTML
    - [ ] Name, role, value for all components
    - [ ] Status messages announced
```

---

## Implementation Workflow

### For Developers

```yaml
development-workflow:
  1-before-coding:
    - Review component accessibility requirements
    - Plan keyboard interaction
    - Choose semantic HTML

  2-during-coding:
    - Use semantic HTML elements
    - Add ARIA when needed (not as replacement)
    - Implement keyboard support
    - Add focus indicators
    - Test as you build

  3-testing:
    - Run automated tools (axe, Pa11y)
    - Keyboard-only navigation
    - Screen reader testing
    - Color contrast check
    - Manual review

  4-before-commit:
    - Accessibility tests pass
    - Manual review complete
    - Documentation updated
```

---

## Resources

```yaml
official-specifications:
  - https://www.w3.org/WAI/WCAG21/quickref/
  - https://www.w3.org/TR/wai-aria-1.2/
  - https://www.w3.org/TR/wai-aria-practices-1.2/

testing-tools:
  - https://www.deque.com/axe/
  - https://wave.webaim.org/
  - https://pa11y.org/

learning-resources:
  - https://webaim.org/
  - https://a11yproject.com/
  - https://www.accessibility-developer-guide.com/
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial accessibility guidelines |

---

## Related Documents

- `design-system.md` - Design system guidelines
- `design-tokens.json` - Machine-readable design tokens
- `components.md` - Component specifications
- `responsive-design.md` - Responsive design specs

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-12-05
**Maintained by**: Design System Engineer (AI Agent)
**WCAG Version**: 2.1 Level AA
