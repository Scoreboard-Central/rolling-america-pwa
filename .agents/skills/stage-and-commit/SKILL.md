---
name: stage-and-commit
description: Stages all changes in the git repository and commits them with a detailed, high-quality commit message describing the modifications.
---
# Stage and Commit Skill

This skill guides the agent in staging all working directory changes, analyzing the modifications, and committing them with a detailed, structured, and informative commit message.

## Workflow

Follow these steps to stage and commit changes:

### Step 1: Stage All Changes
Stage all modified, created, and deleted files in the repository:
```bash
git add -A
```

### Step 2: Analyze the Changes
To write an accurate and detailed commit message, inspect the staged changes:
1. Get the list of staged files:
   ```bash
   git status --short
   ```
2. Inspect the detailed diff of the staged changes:
   ```bash
   git diff --cached
   ```

### Step 3: Generate the Detailed Commit Message
Draft a professional commit message that adheres to the following structure:

1. **Header (Subject Line)**:
   - A single concise line (under 72 characters).
   - Use the Conventional Commits format if applicable (e.g., `feat(component): description`, `fix(bug): description`, `refactor(module): description`, `docs(readme): description`).
   - Use the imperative, present tense: "change", not "changed" or "changes" (e.g., "add login page" instead of "added login page").
   - Keep it lowercase for the type, and capitalize/format the subject appropriately.

2. **Body**:
   - Separate the header from the body with a blank line.
   - Describe **why** the change was made, **what** was changed, and **how** it was done.
   - Break down the changes by component or file when multiple distinct edits are included.
   - Use bullet points for readability.

#### Commit Message Template:
```text
<type>(<scope>): <short summary>

<detailed description of the problem/motivation for this change>

Proposed changes:
- <file/component>: <what was changed and why>
- <file/component>: <what was changed and why>

Verification:
- <how it was tested or verified>
```

### Step 4: Commit the Changes
Commit the staged changes with the generated detailed message:
```bash
git commit -m "<detailed_commit_message>"
```
