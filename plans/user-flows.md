# CodeMentor User Flows
## Version 1.0.0 | Date: 2025-12-05

---

## Document Purpose

This document contains comprehensive user flow diagrams for the CodeMentor platform. All flows are represented in **text-based/ASCII format** to be machine-readable by AI agents (particularly Claude Code) while remaining human-readable.

Each flow includes:
1. **Flow diagram** in ASCII art
2. **Decision points** and branching logic
3. **Success and error paths**
4. **Screen transitions**
5. **Data requirements**

---

## Table of Contents

1. [New User Registration & Onboarding Flow](#1-new-user-registration--onboarding-flow)
2. [Daily Exercise Flow](#2-daily-exercise-flow)
3. [GitHub Code Review Flow](#3-github-code-review-flow)
4. [Mentor Request Flow](#4-mentor-request-flow)
5. [Community Engagement Flow](#5-community-engagement-flow)
6. [Progress Tracking Flow](#6-progress-tracking-flow)

---

## Flow Notation Legend

```
┌─────────┐
│ Screen  │  = User interface screen/page
└─────────┘

[Decision]  = Decision point/conditional logic

→  = Flow direction (single path)
⇒  = Alternative flow
↓  = Continuation downward
↑  = Return/loop back

{Action}  = System action/background process
<Input>   = User input required
✓  = Success path
✗  = Error/failure path
```

---

## 1. New User Registration & Onboarding Flow

### Complete Flow Diagram

```
                              [START]
                                 ↓
                                 ↓
                         ┌───────────────┐
                         │  Landing Page │
                         └───────────────┘
                                 ↓
                    [User clicks "Sign Up"]
                                 ↓
                         ┌───────────────┐
                         │ Registration  │
                         │     Page      │
                         └───────────────┘
                                 ↓
              ┌──────────────────┼──────────────────┐
              ↓                  ↓                  ↓
      <Email/Password>    <GitHub OAuth>    <Google OAuth>
              ↓                  ↓                  ↓
    {Validate Password}   {OAuth Redirect}  {OAuth Redirect}
              ↓                  ↓                  ↓
    {Create Account}      {Create Account}  {Create Account}
              ↓                  ↓                  ↓
              └──────────────────┼──────────────────┘
                                 ↓
                    [Email Verification Required?]
                          ↓             ↓
                         Yes            No (OAuth)
                          ↓             ↓
              ┌─────────────────┐      │
              │ Email Sent      │      │
              │ Check Inbox     │      │
              └─────────────────┘      │
                       ↓               │
              <Click Email Link>       │
                       ↓               │
              {Verify Email Token}     │
                       ↓               │
                       └───────────────┘
                                 ↓
                         ┌───────────────┐
                         │ Onboarding    │
                         │ Interview     │
                         │ Step 1/5      │
                         └───────────────┘
                                 ↓
                    <Select Programming Language>
                                 ↓
                         {Save to Profile}
                                 ↓
                         ┌───────────────┐
                         │ Onboarding    │
                         │ Step 2/5      │
                         └───────────────┘
                                 ↓
                      <Select Skill Level>
                                 ↓
                         {Save to Profile}
                                 ↓
                         ┌───────────────┐
                         │ Onboarding    │
                         │ Step 3/5      │
                         └───────────────┘
                                 ↓
                       <Enter Career Goals>
                                 ↓
                         {Save to Profile}
                                 ↓
                         ┌───────────────┐
                         │ Onboarding    │
                         │ Step 4/5      │
                         └───────────────┘
                                 ↓
                   <Select Learning Preferences>
                                 ↓
                         {Save to Profile}
                                 ↓
                         ┌───────────────┐
                         │ Onboarding    │
                         │ Step 5/5      │
                         └───────────────┘
                                 ↓
                    <Time Commitment Per Day>
                                 ↓
                         {Save to Profile}
                                 ↓
                   {Generate First Exercise}
                                 ↓
                         ┌───────────────┐
                         │   Dashboard   │
                         │ (First Visit) │
                         └───────────────┘
                                 ↓
                      [Show Product Tour?]
                          ↓         ↓
                        Yes         No
                          ↓         ↓
                   ┌──────────┐    │
                   │ Tutorial │    │
                   │ Overlay  │    │
                   └──────────┘    │
                          ↓        │
                          └────────┘
                                 ↓
                         ┌───────────────┐
                         │   Dashboard   │
                         │   (Ready)     │
                         └───────────────┘
                                 ↓
                              [END]
```

### Decision Points

#### Password Validation
```
Password Requirements:
  - Minimum 12 characters: ✓ or ✗
  - Mixed case: ✓ or ✗
  - Numbers: ✓ or ✗
  - Special characters: ✓ or ✗

All must be ✓ to proceed
```

#### Email Verification
```
OAuth users: Skip verification (email pre-verified)
Email/password users: Require verification
  - Send verification email
  - User must click link within 24 hours
  - Resend option available
```

### Alternative Flows

#### Error: Email Already Exists
```
Registration → {Check Email} → [Email Exists?]
                                      ↓
                                     Yes
                                      ↓
                              ┌─────────────┐
                              │ Error: Email│
                              │ in use      │
                              └─────────────┘
                                      ↓
                              [Offer Sign In]
                                   or
                              [Forgot Password]
```

#### User Abandons Onboarding
```
Any Onboarding Step → [User Closes Browser]
                              ↓
                      {Save Progress}
                              ↓
Next Login → [Onboarding Complete?]
                    ↓
                   No
                    ↓
            [Resume Onboarding]
                    ↓
            Last Completed Step
```

### Data Collected

```yaml
registration:
  - email: string
  - password_hash: string
  - oauth_provider: string (optional)
  - oauth_id: string (optional)
  - created_at: timestamp

onboarding:
  - programming_language: string
  - skill_level: enum (beginner, intermediate, advanced)
  - career_goals: text
  - learning_style: enum (visual, hands-on, reading, video)
  - time_commitment: number (minutes per day)
  - completed: boolean
  - completed_at: timestamp
```

---

## 2. Daily Exercise Flow

### Complete Flow Diagram

```
                              [START]
                                 ↓
                         ┌───────────────┐
                         │   Dashboard   │
                         └───────────────┘
                                 ↓
                    [Daily Exercise Available?]
                          ↓              ↓
                         Yes             No
                          ↓              ↓
                  ┌─────────────┐  {Generate New}
                  │ Show Daily  │        ↓
                  │  Exercise   │  ┌─────────────┐
                  │    Card     │  │  Exercise   │
                  └─────────────┘  │  Generated  │
                          ↓        └─────────────┘
                          └────────────┼─────────┘
                                      ↓
                          [User Clicks "Start"]
                                      ↓
                              ┌───────────────┐
                              │   Exercise    │
                              │     View      │
                              └───────────────┘
                                      ↓
                    [User Reads Instructions]
                                      ↓
                              ┌───────────────┐
                              │ User Works on │
                              │   Solution    │
                              └───────────────┘
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    ↓                 ↓                 ↓
            [Request Hint]    [Ask Tutor]     [Submit Solution]
                    ↓                 ↓                 ↓
            {Generate Hint}   ┌─────────────┐  {Analyze Code}
                    ↓         │ Chat Opens  │          ↓
            ┌─────────────┐   │ with Tutor  │  {Run Tests}
            │ Show Hint   │   └─────────────┘          ↓
            │ (Collapsed) │           ↓        [All Tests Pass?]
            └─────────────┘           ↓         ↓            ↓
                    ↓         [Get Guidance]   Yes           No
                    ↓                 ↓         ↓            ↓
                    └─────────────────┼─────────┘     ┌──────────┐
                                      ↓               │ Show     │
                              [Continue Working]      │ Failed   │
                                      ↓               │ Tests    │
                                      ↑               └──────────┘
                                      │                     ↓
                                      └─────────────────────┘
                                                            ↓
                                                   [Fix and Retry]
                                                            ↓
                                                            ↑
                                                            │
                                    ┌───────────────────────┘
                                    ↓
                            [All Tests Pass]
                                    ↓
                          {Generate Feedback}
                                    ↓
                            ┌───────────────┐
                            │ Show Feedback │
                            │  & Analysis   │
                            └───────────────┘
                                    ↓
                        [User Marks Complete]
                                    ↓
                            {Update Progress}
                            {Check Streak}
                            {Award Achievements}
                                    ↓
                          [Achievement Unlocked?]
                                ↓         ↓
                               Yes        No
                                ↓         ↓
                        ┌─────────────┐  │
                        │ Show Badge  │  │
                        │ Celebration │  │
                        └─────────────┘  │
                                ↓        │
                                └────────┘
                                    ↓
                            {Adjust Difficulty}
                                    ↓
                          [Performance Good?]
                                ↓         ↓
                          Good (3+)   Struggling
                                ↓         ↓
                       {Increase}   {Decrease}
                       {Difficulty} {Difficulty}
                                ↓         ↓
                                └────┬────┘
                                     ↓
                             ┌───────────────┐
                             │   Dashboard   │
                             │   (Updated)   │
                             └───────────────┘
                                     ↓
                                  [END]
```

### Decision Points

#### Test Results Analysis
```
Tests Execution:
  - Run all test cases
  - Collect results: pass/fail
  - Measure execution time
  - Check memory usage

Pass Criteria:
  - All test cases pass: ✓
  - Any test fails: ✗ (show specific failures)
  - Timeout: ✗ (optimization needed)
  - Error: ✗ (syntax or runtime error)
```

#### Difficulty Adjustment Logic
```
Track Recent Performance (last 5 exercises):
  - Completed without hints: +2 points
  - Completed with hints: +1 point
  - Struggled (>30 min): 0 points
  - Skipped: -1 point

Adjustment Rules:
  - Total ≥ 9 points: Increase difficulty
  - Total ≤ 3 points: Decrease difficulty
  - Else: Maintain current level
```

### Alternative Flows

#### User Skips Exercise
```
Exercise View → [User Clicks "Skip"]
                        ↓
                [Confirm Skip?]
                  ↓        ↓
                Yes        No
                  ↓        ↓
         {Log Skip}    [Return]
                  ↓
         [Skip Limit Reached?]
           ↓              ↓
          Yes             No
           ↓              ↓
    ┌──────────┐    Dashboard
    │ Warning: │
    │ 2/2 Used │
    └──────────┘
           ↓
       Dashboard
```

#### Chat with Tutor During Exercise
```
Exercise View → [Click "Ask Tutor"]
                        ↓
                ┌──────────────┐
                │ Chat Sidebar │
                │ Opens        │
                └──────────────┘
                        ↓
        {Inject Exercise Context}
                        ↓
                <User Asks Question>
                        ↓
            {Tutor Provides Guidance}
            (Socratic method - no direct answers)
                        ↓
                <User Continues>
                        ↓
         [Chat Open While Working]
                        ↓
                [User Closes Chat]
                        ↓
          [Continue Exercise Flow]
```

### Data Tracked

```yaml
exercise_attempt:
  - exercise_id: string
  - user_id: string
  - started_at: timestamp
  - completed_at: timestamp (optional)
  - status: enum (in_progress, completed, skipped)
  - hints_requested: number
  - chat_messages: number
  - test_results: array[object]
  - time_spent: number (seconds)
  - code_submitted: text

performance_metrics:
  - difficulty_level: number (1-10)
  - consecutive_successes: number
  - consecutive_struggles: number
  - adjustment_triggered: boolean
```

---

## 3. GitHub Code Review Flow

### Complete Flow Diagram

```
                              [START]
                                 ↓
                         ┌───────────────┐
                         │   Dashboard   │
                         │      or       │
                         │     Chat      │
                         └───────────────┘
                                 ↓
                    [User Mentions GitHub]
                         or
                [Clicks "Review My Code"]
                                 ↓
                         ┌───────────────┐
                         │  GitHub Link  │
                         │     Input     │
                         └───────────────┘
                                 ↓
                      <Paste Repository URL>
                                 ↓
                        {Validate URL}
                                 ↓
                         [Valid GitHub URL?]
                          ↓              ↓
                         Yes             No
                          ↓              ↓
                    [Public/Private?]  ┌──────────┐
                      ↓         ↓      │ Error:   │
                  Public    Private    │ Invalid  │
                      ↓         ↓      │ URL      │
                      │    [OAuth     └──────────┘
                      │    Granted?]        ↓
                      │      ↓    ↓     [Retry]
                      │     Yes   No         ↓
                      │      ↓    ↓          ↑
                      │      │  ┌──────────┐ │
                      │      │  │ Request  │─┘
                      │      │  │ GitHub   │
                      │      │  │ Access   │
                      │      │  └──────────┘
                      │      │      ↓
                      │      │  <User Grants>
                      │      │      ↓
                      │      └──────┘
                      ↓         ↓
                      └────┬────┘
                           ↓
                    {Clone Repository}
                           ↓
                    [Repo Size Check]
                           ↓
                  [Size < 500MB?]
                     ↓          ↓
                    Yes         No
                     ↓          ↓
                     │    ┌──────────────┐
                     │    │ Ask User to  │
                     │    │ Specify Files│
                     │    └──────────────┘
                     │          ↓
                     │    <Select Files>
                     │          ↓
                     └─────┬────┘
                           ↓
                  {Parse Repository}
                  {Extract Code Files}
                           ↓
                    [Show Progress]
                           ↓
                    {Analyze with LLM}
                    - Code structure
                    - Potential bugs
                    - Best practices
                    - Performance
                           ↓
                  {Generate Review}
                           ↓
                  ┌───────────────┐
                  │ Code Review   │
                  │ Results Page  │
                  └───────────────┘
                           ↓
              [Display Review Sections:]
              - Overall Assessment
              - Strengths
              - Issues Found
              - Suggestions
              - Code Examples
                           ↓
          [User Reviews Feedback]
                           ↓
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
    [Ask Questions]  [Request     [Mark as
     in Chat]         Re-Review]   Reviewed]
          ↓                ↓                ↓
    ┌──────────┐    {Save Request}  {Update Count}
    │ Chat     │           ↓                ↓
    │ with LLM │    [Schedule]        Dashboard
    └──────────┘           ↓                ↓
          ↓         {Notify User}        [END]
          │         when Ready
          │                ↓
          │          [END]
          │
          ↓
    [Continue Discussion]
          ↓
    [Implement Fixes]
          ↓
    [Optional: Submit
     Updated Repo]
          ↓
       [END]
```

### Decision Points

#### Repository Access
```
Public Repository:
  - Direct access via GitHub API
  - No authentication needed
  - Proceed to cloning

Private Repository:
  - Check if user has granted OAuth access
  - If no: Redirect to GitHub OAuth flow
  - If yes: Use access token to clone
  - Store token securely (encrypted)
```

#### Size Limitations
```
Repository Size:
  < 100MB: Analyze entire repo
  100MB - 500MB: Ask user to select key files/directories
  > 500MB: Error - too large
    - Suggest: Create smaller repo
    - Or: Select specific files to review
```

### Alternative Flows

#### Error: Repository Not Found
```
Clone Attempt → {GitHub API Call}
                        ↓
                   [Repo Exists?]
                        ↓
                       No
                        ↓
                ┌──────────────┐
                │ Error: Repo  │
                │ not found or │
                │ no access    │
                └──────────────┘
                        ↓
              [Check URL & Permissions]
                        ↓
                  [Retry Input]
```

#### User Requests Re-Review After Changes
```
Review Complete → [User Updates Code]
                        ↓
                  [Clicks "Re-Review"]
                        ↓
              {Check: Last Review < 24h ago?}
                   ↓              ↓
                  Yes             No
                   ↓              ↓
            ┌──────────┐    [Proceed with
            │ Warning: │     New Review]
            │ Recent   │          ↓
            │ Review   │    {Clone Latest}
            │ Exists   │          ↓
            └──────────┘    [Full Flow]
                   ↓
            [Proceed Anyway?]
               ↓        ↓
              Yes       No
               ↓        ↓
          [New Review] [View Existing]
```

### Data Tracked

```yaml
code_review:
  - review_id: string
  - user_id: string
  - repository_url: string
  - repository_name: string
  - repository_language: string
  - is_private: boolean
  - created_at: timestamp
  - analysis_results: object
    - overall_score: number (0-100)
    - strengths: array[string]
    - issues: array[object]
    - suggestions: array[object]
  - user_feedback: text (optional)
  - follow_up_questions: number
```

---

## 4. Mentor Request Flow

### Complete Flow Diagram

```
                              [START]
                                 ↓
                         ┌───────────────┐
                         │   Dashboard   │
                         │      or       │
                         │  Mentorship   │
                         │     Page      │
                         └───────────────┘
                                 ↓
                    [Click "Find a Mentor"]
                                 ↓
                         ┌───────────────┐
                         │   Mentor      │
                         │ Matching Form │
                         └───────────────┘
                                 ↓
              <Select Topics of Interest>
                                 ↓
                   <Select Meeting Frequency>
                                 ↓
                     <Enter Specific Goals>
                                 ↓
                 <Preferred Communication Style>
                                 ↓
                     [Click "Find Matches"]
                                 ↓
                    {Run Matching Algorithm}
                    - Match by topics
                    - Match by availability
                    - Match by experience
                    - Calculate compatibility
                                 ↓
                      [Mentors Available?]
                         ↓              ↓
                        Yes             No
                         ↓              ↓
                {Generate 3-5}    ┌──────────────┐
                  {Matches}       │ No mentors   │
                         ↓        │ available    │
                ┌───────────────┐ └──────────────┘
                │ Show Mentor   │        ↓
                │  Profiles     │ ┌──────────────┐
                │ with Scores   │ │ Add to       │
                └───────────────┘ │ Waitlist?    │
                         ↓        └──────────────┘
           [User Browses Profiles]    ↓         ↓
                         ↓            Yes        No
           ┌─────────────┼────────┐   ↓         ↓
           ↓             ↓        ↓   {Add}  Dashboard
    [View Profile] [Compare] [Select]  ↓         ↓
           ↓             ↓        ↓   [END]    [END]
           ↓      [Side by Side] ↓
           │       Comparison     │
           │             ↓        │
           └─────────────┼────────┘
                         ↓
                <Select Preferred Mentor>
                         ↓
                  [Add Personal Note]
                         ↓
                 [Click "Send Request"]
                         ↓
                 {Create Match Request}
                 {Notify Mentor}
                         ↓
                 ┌───────────────┐
                 │ Request Sent  │
                 │ Confirmation  │
                 └───────────────┘
                         ↓
              [Wait for Mentor Response]
            (User receives notification)
                         ↓
              ┌──────────┼──────────┐
              ↓                     ↓
      [Mentor Accepts]      [Mentor Declines]
              ↓                     ↓
    {Create Relationship}    {Notify User}
    {Create Chat Channel}          ↓
              ↓              ┌──────────────┐
     ┌───────────────┐      │ Suggest Next │
     │ Success!      │      │ Best Match   │
     │ You're        │      └──────────────┘
     │ Matched!      │             ↓
     └───────────────┘      [Offer Alternative]
              ↓                     ↓
     ┌───────────────┐      [User Decides]
     │ Intro Message │        ↓        ↓
     │ from Mentor   │      Accept   Decline
     └───────────────┘        ↓        ↓
              ↓               │    Dashboard
     [Start Conversation]     │        ↓
              ↓               │      [END]
     ┌───────────────┐        │
     │ Mentorship    │        │
     │ Dashboard     │        │
     └───────────────┘        │
              ↓               │
              └───────────────┘
              ↓
           [END]
```

### Decision Points

#### Matching Algorithm
```
Calculate Compatibility Score (0-100):
  - Topic overlap: 40 points
    (Number of shared topics / Total topics)

  - Experience level match: 30 points
    (Mentor experience > Mentee level + 1)

  - Availability alignment: 20 points
    (Overlapping time slots)

  - Communication style: 10 points
    (Preferences match)

Return top 3-5 mentors with score ≥ 60
```

#### Mentor Availability
```
Check Mentor Status:
  - Active: ✓
  - Current mentees < 5: ✓
  - Accepting requests: ✓

All must be ✓ to include in matches
```

### Alternative Flows

#### Request Timeout (No Response After 7 Days)
```
Request Sent → [Wait 7 Days]
                    ↓
            [Response Received?]
                    ↓
                   No
                    ↓
            {Auto-expire Request}
                    ↓
            ┌──────────────┐
            │ Notify User: │
            │ No response  │
            └──────────────┘
                    ↓
         [Suggest Alternative Mentors]
                    ↓
            [User Can Re-request]
```

#### User Changes Mind Before Acceptance
```
Request Pending → [User Cancels]
                        ↓
                  [Confirm Cancel?]
                    ↓        ↓
                   Yes       No
                    ↓        ↓
            {Cancel Request}  Return
            {Notify Mentor}
                    ↓
                Dashboard
```

### Data Tracked

```yaml
mentor_match_request:
  - request_id: string
  - mentee_id: string
  - mentor_id: string
  - topics: array[string]
  - meeting_frequency: string
  - goals: text
  - personal_note: text
  - compatibility_score: number
  - status: enum (pending, accepted, declined, expired)
  - created_at: timestamp
  - responded_at: timestamp (optional)

mentor_relationship:
  - relationship_id: string
  - mentor_id: string
  - mentee_id: string
  - started_at: timestamp
  - status: enum (active, paused, ended)
  - communication_channel_id: string
  - meeting_count: number
  - last_interaction: timestamp
```

---

## 5. Community Engagement Flow

### Complete Flow Diagram

```
                              [START]
                                 ↓
                         ┌───────────────┐
                         │   Dashboard   │
                         └───────────────┘
                                 ↓
                  [Click "Browse Community"]
                                 ↓
                         ┌───────────────┐
                         │  Community    │
                         │     Page      │
                         └───────────────┘
                                 ↓
              [Display Available Rooms]
                                 ↓
          ┌────────────────┬─────┴─────┬────────────┐
          ↓                ↓           ↓            ↓
    [Browse All]  [Filter by Topic] [Search] [Create Room]
          ↓                ↓           ↓            ↓
    [See All Rooms] <Select Filter> <Enter Query> <Request>
          ↓                ↓           ↓            ↓
          │         {Filter Results} {Search}  {Admin Review}
          │                ↓           ↓            ↓
          │         [Filtered List] [Results] [Pending...]
          │                ↓           ↓            ↓
          └────────────────┴─────┬─────┴────────────┘
                                 ↓
                      [User Selects Room]
                                 ↓
                         ┌───────────────┐
                         │   Room Info   │
                         │     Page      │
                         └───────────────┘
                                 ↓
              [Display: Title, Description,
               Members, Recent Activity]
                                 ↓
                        [Click "Join Room"]
                                 ↓
                  [Room Type: Public/Private?]
                         ↓              ↓
                      Public        Private
                         ↓              ↓
                  {Join Immediately}  [Request Access]
                         ↓              ↓
                         │        {Notify Moderator}
                         │              ↓
                         │        [Wait for Approval]
                         │         ↓           ↓
                         │      Approved    Denied
                         │         ↓           ↓
                         │      {Join}    [Notify User]
                         │         ↓           ↓
                         └─────────┼───────────┘
                                   ↓         Dashboard
                          {Add User to Room}    ↓
                                   ↓          [END]
                           ┌───────────────┐
                           │  Chat Room    │
                           │   Interface   │
                           └───────────────┘
                                   ↓
                        [User Can Now:]
                        - Read messages
                        - Send messages
                        - Share code
                        - React to messages
                                   ↓
                      <User Sends Message>
                                   ↓
                        {Broadcast to Room}
                                   ↓
                    [All Members See Message]
                                   ↓
                      [Continue Interaction]
                                   ↓
              ┌────────────────────┼────────────────────┐
              ↓                    ↓                    ↓
       [Leave Room]        [Report Message]      [Continue Chat]
              ↓                    ↓                    ↓
       {Remove User}      {Flag for Review}        [Active]
              ↓                    ↓                    ↑
         Dashboard         {Notify Moderator}          │
              ↓                    ↓                    │
            [END]            [Moderator Reviews]       │
                                   ↓                    │
                           [Take Action]               │
                             ↓        ↓                │
                        Remove    No Action            │
                        Message      ↓                 │
                             ↓       │                 │
                        {Delete}    │                 │
                        {Notify}    │                 │
                             ↓      │                 │
                             └──────┘                 │
                                   ↓                  │
                              [Continue] ─────────────┘
```

### Decision Points

#### Room Privacy Level
```
Public Room:
  - Anyone can join immediately
  - Messages visible to all members
  - Open discovery in room list

Private Room:
  - Join request required
  - Moderator approval needed
  - Not shown in public room list
  - Invite-only discovery
```

#### Message Moderation
```
Auto-Flag Conditions:
  - Profanity detected: Flag
  - Spam pattern: Flag
  - Excessive caps: Warning
  - Links to external sites: Review

Moderator Actions:
  - Delete message: Remove + notify sender
  - Warn user: Warning + log
  - Timeout user: Mute for X minutes
  - Ban user: Permanent removal
```

### Alternative Flows

#### User Creates New Room Proposal
```
Community Page → [Click "Propose Room"]
                        ↓
                 ┌──────────────┐
                 │ Room Proposal│
                 │     Form     │
                 └──────────────┘
                        ↓
            <Enter: Title, Topic,
             Description, Privacy>
                        ↓
                [Submit for Review]
                        ↓
                {Notify Moderators}
                        ↓
              [Moderator Reviews]
                 ↓            ↓
             Approved      Rejected
                 ↓            ↓
           {Create Room}  {Notify User}
           {Notify User}  with Reason
                 ↓            ↓
              [Join Room]  Dashboard
                 ↓            ↓
            [Chat Active]  [END]
                 ↓
              [END]
```

### Data Tracked

```yaml
community_room:
  - room_id: string
  - name: string
  - topic: string
  - description: text
  - is_private: boolean
  - created_by: string
  - created_at: timestamp
  - member_count: number
  - moderators: array[string]

room_membership:
  - membership_id: string
  - room_id: string
  - user_id: string
  - joined_at: timestamp
  - role: enum (member, moderator)
  - last_read: timestamp

room_message:
  - message_id: string
  - room_id: string
  - user_id: string
  - content: text
  - created_at: timestamp
  - edited_at: timestamp (optional)
  - reactions: array[object]
  - is_flagged: boolean
```

---

## 6. Progress Tracking Flow

### Complete Flow Diagram

```
                              [START]
                                 ↓
                         ┌───────────────┐
                         │   Dashboard   │
                         └───────────────┘
                                 ↓
                  [Click "View Progress"]
                                 ↓
                         ┌───────────────┐
                         │   Progress    │
                         │     Page      │
                         └───────────────┘
                                 ↓
              {Fetch User Progress Data}
                                 ↓
              ┌──────────────────┼──────────────────┐
              ↓                  ↓                  ↓
      [Overview Tab]     [Skills Tab]    [Achievements Tab]
              ↓                  ↓                  ↓
      Display:           Display:           Display:
      - Streak           - Skill Levels     - Earned Badges
      - Total Exercises  - Progress Bars    - Locked Badges
      - Time Spent       - Recommendations  - Milestones
      - Charts                  ↓                  ↓
              ↓                  ↓                  ↓
      [Interactive Charts]  [Skill Details] [Badge Details]
              ↓                  ↓                  ↓
      ┌─────────────┐    ┌─────────────┐   ┌─────────────┐
      │ Line Chart: │    │ Show        │   │ Show        │
      │ Exercises   │    │ Exercises   │   │ Requirements│
      │ Over Time   │    │ for Skill   │   │ to Unlock   │
      └─────────────┘    └─────────────┘   └─────────────┘
              ↓                  ↓                  ↓
      <Hover for Details> <Click Skill>   <Track Progress>
              ↓                  ↓                  ↓
      [Show Tooltip]     ┌─────────────┐          │
        Date, Count      │ Skill Detail│          │
              ↓          │    Modal    │          │
              │          └─────────────┘          │
              │                  ↓                │
              │          Display:                 │
              │          - Mastery %              │
              │          - Recent Exercises       │
              │          - Suggested Topics       │
              │                  ↓                │
              │          [Practice This Skill]    │
              │                  ↓                │
              │          {Generate Exercise}      │
              │                  ↓                │
              │          [Exercise View]          │
              │                  ↓                │
              └──────────────────┼────────────────┘
                                 ↓
                      [Background Process:]
                      {Check for New Achievements}
                                 ↓
                      [Achievement Unlocked?]
                          ↓              ↓
                         Yes             No
                          ↓              ↓
                  {Trigger Animation}   Continue
                          ↓              ↓
                  ┌─────────────┐        │
                  │ 🎉 Badge    │        │
                  │ Unlocked!   │        │
                  │ Celebration │        │
                  └─────────────┘        │
                          ↓              │
                  [Show Badge Details]   │
                          ↓              │
                  [Share Achievement?]   │
                    ↓            ↓       │
                   Yes           No      │
                    ↓            ↓       │
              {Generate     [Close]     │
               Shareable     Modal      │
               Image}          ↓        │
                    ↓          │        │
              [Social Share]  │        │
                    ↓          │        │
                    └──────────┼────────┘
                               ↓
                         [User Can:]
                         - Export Progress
                         - Print Report
                         - Compare with Goals
                               ↓
                    <User Selects Action>
                               ↓
          ┌────────────────────┼────────────────────┐
          ↓                    ↓                    ↓
    [Export PDF]        [Print Report]      [Goal Comparison]
          ↓                    ↓                    ↓
    {Generate PDF}      {Format Print}      {Calculate Gap}
          ↓                    ↓                    ↓
    [Download]          [Print Dialog]      ┌─────────────┐
          ↓                    ↓            │ Show:       │
       [END]                [END]           │ - Goal      │
                                            │ - Current   │
                                            │ - Remaining │
                                            └─────────────┘
                                                   ↓
                                            [Suggest Plan]
                                                   ↓
                                                [END]
```

### Decision Points

#### Achievement Unlock Logic
```
Achievement Types:
  1. Streak-based:
     - Check consecutive_days
     - Thresholds: 7, 30, 100, 365

  2. Exercise-based:
     - Check total_completed
     - Thresholds: 10, 50, 100, 500

  3. Skill-based:
     - Check skill_level for each topic
     - Unlock when level ≥ advanced (80%)

  4. Community-based:
     - Check message_count, helpful_votes
     - Various thresholds

Process:
  - Run check after each tracked action
  - If threshold crossed: Unlock badge
  - Store unlock timestamp
  - Trigger notification
```

#### Streak Calculation
```
Current Streak:
  - Count consecutive days with ≥1 exercise completed
  - Break if any day missed (no completion)
  - Reset to 0 on break
  - Grace period: None (strict consecutive)

Longest Streak:
  - Track historical maximum
  - Never decreases
  - Update when current > longest
```

### Alternative Flows

#### Export Progress Report
```
Progress Page → [Click "Export Report"]
                        ↓
                [Select Format]
                  ↓         ↓
                PDF       CSV
                  ↓         ↓
           {Generate    {Generate
            PDF with     CSV with
            Charts}      Raw Data}
                  ↓         ↓
              [Download File]
                  ↓
               [END]
```

### Data Tracked

```yaml
user_progress:
  - user_id: string
  - current_streak: number
  - longest_streak: number
  - total_exercises_completed: number
  - total_time_spent: number (minutes)
  - last_active: timestamp
  - skill_levels: object
    - python: number (0-100)
    - javascript: number (0-100)
    - algorithms: number (0-100)
    - etc.

achievement_unlock:
  - achievement_id: string
  - user_id: string
  - unlocked_at: timestamp
  - shared: boolean
```

---

## Cross-Flow Integrations

### Notification System
All flows can trigger notifications:

```
{Event Occurs}
      ↓
{Create Notification}
      ↓
[Delivery Method:]
  ↓        ↓        ↓
Email   In-App   Push
```

### Error Handling Pattern
Standard error flow across all features:

```
{Operation Fails}
      ↓
{Log Error}
      ↓
[User-Facing?]
  ↓         ↓
 Yes        No
  ↓         ↓
[Show     {Alert
 Error     Admin}
 Message]    ↓
  ↓       [END]
[Offer
 Retry
 Action]
  ↓
[END]
```

---

## Implementation Notes for AI Agents

### State Management
Each flow requires managing:
- **Navigation state**: Current screen, history
- **Form state**: User inputs, validation
- **Loading state**: API calls, processing
- **Error state**: Error messages, retry logic

### API Endpoints Needed
```
Authentication:
  POST /api/auth/register
  POST /api/auth/login
  POST /api/auth/verify-email
  POST /api/auth/oauth/{provider}

Exercises:
  GET /api/exercises/daily
  POST /api/exercises/{id}/submit
  GET /api/exercises/{id}/hint
  POST /api/exercises/{id}/complete

GitHub:
  POST /api/github/review
  GET /api/github/reviews/{id}

Mentorship:
  GET /api/mentors/match
  POST /api/mentors/request
  GET /api/mentorship/relationships

Community:
  GET /api/community/rooms
  POST /api/community/rooms/{id}/join
  POST /api/community/rooms/{id}/messages

Progress:
  GET /api/progress
  GET /api/progress/achievements
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial user flow documentation |

---

## Related Documents

- `wireframes.md` - Screen wireframes
- `design-system.md` - Design system guidelines
- `components.md` - Component specifications
- `requirements.md` - Functional requirements

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-12-05
**Maintained by**: Design System Engineer (AI Agent)
