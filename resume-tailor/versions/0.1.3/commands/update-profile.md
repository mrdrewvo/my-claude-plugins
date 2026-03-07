---
description: Build or refresh your experience vault from your resumes
allowed-tools: Read, Write, Edit, Glob, WebSearch, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch
argument-hint: [optional: add a specific accomplishment or note]
---

You are running the `/update-profile` command. Your goal is to build or refresh the user's experience vault — a structured, living document of their career history and accomplishments that can be drawn from for any future resume tailoring session.

The user's argument (if provided) is: $ARGUMENTS

---

## Step 1: Check for Existing Vault

**Important:** The experience vault is a local file, not a Google Drive file. The Google Drive connector is read-only — Drive search/fetch is only used in Step 3 to pull in source resume documents. The vault is always read from and written to the user's locally mounted folder.

To find the mounted folder, list the `/sessions/` directory to identify the current session name, then look in `/sessions/{session-name}/mnt/`. Never hardcode the session name — it changes with every new Cowork session.

Search for an existing `experience-vault.md` file using Glob with pattern `**/experience-vault.md` in the mounted folder you just discovered.

If it exists, read it in full. Note what's already captured — you'll add to it without duplicating.

If it doesn't exist, you'll create it from scratch in the mounted folder.

---

## Step 2: Check for a Manually Provided Update

If $ARGUMENTS is non-empty, the user may be providing:
- A specific accomplishment to add ("I just led a $5M product launch at Acme")
- A new role or job change
- A skill or certification to add
- General content to absorb

If $ARGUMENTS describes a specific update, go directly to Step 4 to add it — you don't need to re-scan all resumes unless the user asks.

---

## Step 3: Scan Source Resumes from Google Drive

Search Google Drive for resume documents using the google_drive_search tool:
`fullText contains 'resume' OR name contains 'resume' OR name contains 'CV' OR name contains 'curriculum vitae'`

Sort by most recently modified. Fetch up to 5 documents using google_drive_fetch.

Also check the connected folder for any local resume files using Glob: `**/*.docx`, `**/*.pdf`, `**/*.md`, `**/*.txt`

Read all source resumes you find.

---

## Step 4: Extract and Structure Career Data

From all source documents (and $ARGUMENTS if provided), extract:

### For each Role:
- **Company name** and brief description (industry, stage, size if mentioned)
- **Job title** (exact)
- **Start date – End date** (Month Year format; "Present" if current)
- **Location** (city, state, or Remote)
- **Key accomplishments** — every bullet point, preserved with all metrics intact
- **Tools and platforms** used in this role
- **Scope** — team size managed, budget owned, geographic reach, revenue influenced

### Career-Wide:
- **Technical skills and tools** — all mentioned across all roles
- **Domain expertise** — industries, verticals, functional areas
- **Methodologies** — Agile, OKR, A/B testing, Six Sigma, etc.
- **Certifications** — official names and issuing organizations
- **Education** — degree, field, institution, graduation year

---

## Step 5: Write or Update the Vault

### If creating from scratch, write `experience-vault.md` with this structure:

```markdown
# Experience Vault
*Last updated: [today's date]*

---

## Career Summary
[2–3 sentence synthesis of career arc, key strengths, and domain expertise — useful for drafting summaries]

---

## Work Experience

### [Job Title] | [Company Name]
*[Start Month Year] – [End Month Year] | [Location]*

**About [Company]:** [1 sentence: industry, stage, what they do]

**Accomplishments:**
- [Exact bullet from resume, with all metrics preserved]
- [...]

**Tools & Skills used in this role:** [comma-separated list]

---

[Repeat for each role, most recent first]

---

## Skills & Expertise

### Technical Skills
[List]

### Domain Expertise
[List]

### Methodologies & Frameworks
[List]

### Tools & Platforms
[List]

---

## Education
- [Degree], [Field] — [Institution], [Year]

## Certifications
- [Certification Name] — [Issuer], [Year]

---

## Accomplishment Bank
*High-impact bullets with strong metrics — quick-reference for tailoring*

- [Your strongest metric-driven bullets, pulled from all roles]
```

### If updating an existing vault:
- Add new roles at the top of Work Experience (most recent first)
- Append new accomplishments to the relevant role's section
- Add new skills to the Skills section if not already listed
- Update "Last updated" date
- Add any exceptional new bullets to the Accomplishment Bank

Use Edit (not Write) to update an existing file to preserve existing content.

---

## Step 6: Confirm and Summarize

Tell the user what was captured:
- How many roles are now in the vault
- Any new skills or tools added
- If anything looked ambiguous (overlapping dates, unclear role scope, etc.)

Say: "Your experience vault is up to date. Run `/tailor-resume` any time you want to generate a tailored resume for a specific job."

If there were gaps or ambiguities in the source material, ask one clarifying question (not multiple) to fill the most important one:
- "I noticed your [role] doesn't list specific outcomes — do you have any metrics you'd want to add for that period?"
- "I saw [Company] listed but no bullet points — would you like to add some accomplishments for that role?"
