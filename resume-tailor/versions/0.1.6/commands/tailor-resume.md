---
description: Tailor your resume to a specific job description
allowed-tools: Read, Write, Glob, Bash, WebFetch, WebSearch, Task, mcp__cowork__request_cowork_directory, mcp__cowork__present_files, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch
argument-hint: [job-description-url-or-paste-below]
---

<!--
  PLUGIN CUSTOMIZATION
  - Google Drive tools are pre-configured for this installation
    (mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search / google_drive_fetch).
  - If you're using a different installation, replace the UUID above with your own.
  - The local folder + paste fallback works for everyone out of the box.
-->

You are running the `/tailor-resume` command. Your goal is to produce a tailored, ATS-optimized, and compelling resume for a specific job. Work through these phases carefully.

The user's argument (if provided) is: $ARGUMENTS

---

## Phase 0: Connect to Your Files

Run these checks silently before saying anything to the user.

**Check 1 — Local folder:** Run `ls mnt/ 2>/dev/null | head -5`. If files are present, a local folder is already mounted. Note the path (`mnt/`).

**Check 2 — Google Drive connector:** Look at your available tools. If any tool name contains `google_drive_search`, a Drive connector is available.

Now present a brief, friendly status to the user based on what you found:

---

**Scenario A — Local folder mounted, no Drive connector:**
> "Your folder is connected — I can read `.md`, `.docx`, and `.pdf` files directly and save outputs there. Ready to go whenever you are."

Proceed to Phase 1. Store access mode: **LOCAL**.

---

**Scenario B — Drive connector available, no local folder:**
> "Your Google Drive is connected. One thing to know: the Drive connector reads native Google Docs only — it can't open `.docx` or `.pdf` files directly. Would you also like to connect a local folder (useful if you use Google Drive for Desktop)? Just say yes and I'll open the folder picker, or say no to continue with Drive only."

If the user says yes → call `mcp__cowork__request_cowork_directory` to open the folder picker, then confirm the mount succeeded with `ls mnt/ | head -5`. Store access mode: **BOTH**.

If the user says no → store access mode: **DRIVE_ONLY**.

---

**Scenario C — Both local folder and Drive connector available:**
> "You're fully set up — I have your local folder for reading all file types and saving outputs, and your Google Drive connector as a backup for any Google Docs not synced locally. Let's go."

Proceed to Phase 1. Store access mode: **BOTH**.

---

**Scenario D — Neither available:**
> "To get started, how would you like to share your resume files?
> 1. **Select a folder** — recommended if you use Google Drive for Desktop or have files locally
> 2. **Paste your resume** — paste the text directly in this chat
> 3. **Google Drive link** — share a link to a Google Doc (publicly shared or signed-in)
>
> Which works best for you?"

- Option 1 → call `mcp__cowork__request_cowork_directory`, confirm mount, store mode: **LOCAL**
- Option 2 → ask user to paste; store mode: **PASTE**
- Option 3 → ask for the URL; store mode: **URL**

---

## Phase 1: Gather the Job Description

If $ARGUMENTS contains a URL, use WebFetch to retrieve the job description.

If $ARGUMENTS contains pasted text (not a URL), treat it as the job description directly.

If $ARGUMENTS is empty, ask the user: "Please paste the job description below, or share the URL to the posting."

Confirm by stating the job title and company name.

---

## Phase 2: Load the Experience Vault

Search for `experience-vault.md` using Glob with pattern `**/experience-vault.md`.

If found:
- **If the file is on a FUSE-mounted filesystem (Google Drive for Desktop):** Copy to `/tmp/` first to avoid deadlocks, then read:
  ```bash
  cp "PATH_TO_FILE" /tmp/experience-vault.md
  ```
  Read from `/tmp/experience-vault.md`.
- **Otherwise:** Read the file directly.

If not found, say: "I didn't find an experience vault yet. I'll work from your source resumes instead. You can build your vault anytime with `/update-profile`."

---

## Phase 3: Load Source Resumes

Use the access mode set in Phase 0.

### Mode: LOCAL or BOTH

**Step 1 — Find resume files** using Glob:
- `mnt/**/*.md`
- `mnt/**/*.docx`
- `mnt/**/*.pdf`

Look for files with "resume", "cv", or the user's name in the filename. Skip obvious output files (e.g., names ending in `-Resume.md` or matching the output naming pattern).

**Step 2 — Read each file:**

- **`.md` files:** Copy to `/tmp/` first (FUSE deadlock prevention), then read with the Read tool:
  ```bash
  cp "mnt/path/to/file.md" /tmp/source-resume.md
  ```

- **`.docx` files:** Copy to `/tmp/`, extract text:
  ```bash
  cp "mnt/path/to/file.docx" /tmp/source-resume.docx
  pip install python-docx --break-system-packages -q
  python3 -c "
  import docx; doc = docx.Document('/tmp/source-resume.docx')
  for p in doc.paragraphs:
      if p.text.strip(): print(p.text)
  "
  ```

- **`.pdf` files:** Copy to `/tmp/`, extract text:
  ```bash
  cp "mnt/path/to/file.pdf" /tmp/source-resume.pdf
  pip install pdfplumber --break-system-packages -q
  python3 -c "
  import pdfplumber
  with pdfplumber.open('/tmp/source-resume.pdf') as pdf:
      for page in pdf.pages: print(page.extract_text() or '')
  "
  ```

If no resume files are found in `mnt/`, fall through to the Drive search step (if BOTH) or ask the user to paste.

**Step 2b (BOTH mode only) — Search Drive for resumes:**

After reading local files, search Google Drive for any resumes not present locally. Run all three searches:

**Search 1 — Google Docs:**
- Query: `mimeType = 'application/vnd.google-apps.document' and (name contains 'resume' or name contains 'cv')`
- Fetch results with `google_drive_fetch` — returns content reliably for native Google Docs.

**Search 2 — PDF resumes:**
- Query: `mimeType = 'application/pdf' and (name contains 'resume' or name contains 'cv')`
- Try `google_drive_fetch` for each result. This usually returns empty for uploaded PDFs in Cowork (Linux VM) — that's expected.

**Search 3 — DOCX resumes:**
- Query: `mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and (name contains 'resume' or name contains 'cv')`
- Try `google_drive_fetch` for each result. Same limitation applies.

For any PDF or DOCX files found in Drive that returned empty content, tell the user:
> "I found [filename] in your Drive but can't read it directly — the Drive connector only reads native Google Docs. To use this file, copy it into your connected local folder and I'll pick it up automatically."

After the user adds files and re-mounts (or if they confirm they're already in the folder), re-run the local Glob from Step 1.

Merge all successfully read content, deduplicating as needed.

---

### Mode: DRIVE_ONLY

Search Google Drive in three passes:

**Pass 1 — Google Docs:**
- Query: `mimeType = 'application/vnd.google-apps.document' and (name contains 'resume' or name contains 'cv')`
- Fetch results with `google_drive_fetch`

**Pass 2 — PDF resumes:**
- Query: `mimeType = 'application/pdf' and (name contains 'resume' or name contains 'cv')`
- Try `google_drive_fetch` for each result

**Pass 3 — DOCX resumes:**
- Query: `mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and (name contains 'resume' or name contains 'cv')`
- Try `google_drive_fetch` for each result

If PDFs or DOCX files were found but returned empty content, tell the user:
> "I found [filename] in your Drive but can't read it directly — the Drive connector only reads native Google Docs. To use it, either open it in Google Docs to convert it, or connect a local folder containing the file."

If no readable resume content was found at all, fall back to asking the user to paste their resume or connect a local folder.

---

### Mode: PASTE

Use the resume content the user pasted in Phase 0. Skip file searching.

---

### Mode: URL

Use WebFetch to retrieve the content from the URL the user provided. If it's a Google Doc sharing link, fetch the published/export URL directly.

---

Consolidate all experience from vault + source resumes into a working profile in context.

---

## Phase 4: Research the Company

Using WebSearch, research the target company:
1. Company name + "mission," "values," recent news
2. Recent press releases, funding, product launches
3. Glassdoor or LinkedIn for culture signals

Synthesize into a brief intel summary: what is this company focused on, what do they value, what does success in this role look like beyond the JD?

---

## Phase 5: Analyze the Job Description

Apply the full JD analysis framework:

1. Extract and categorize the top 10–15 keywords (Technical Skills, Domain Knowledge, Methodologies, Soft Skills)
2. Identify required vs. preferred qualifications
3. Read between the lines — what is this role really about? What does the language signal about team situation and culture?
4. Map the user's experience to each requirement
5. Identify gaps and determine how to handle them

Present a **Job Intel Report** to the user (5–8 bullets):
- What this role is really about
- Top keywords to target
- Interesting company context
- Recommended positioning angle
- Any gaps worth flagging

Ask: "Does this read right to you? Is there anything about your background or goals I should factor in before I start writing?"

Wait for the user's response before proceeding.

---

## Phase 6: Write the Tailored Resume

### Structure (in order):
1. **Header** — Name, email, phone, LinkedIn URL, city/state (no full street address)
2. **Professional Summary** — 3–4 lines tailored to this role. Include the target job title or close variant, 2–3 priority keywords, a distinctive value statement. Mirror the JD's language and energy.
3. **Work Experience** — Chronological (most recent first). Company, title, dates (Month Year – Month Year), location. 4–6 bullets per recent role, 2–3 for older ones. Strong action verb leads every bullet. Quantify impact. Order bullets by relevance to this job.
4. **Skills** — Single-column or comma list. Tools, platforms, methodologies, domain expertise.
5. **Education** — Degree, field, institution, year.
6. **Certifications** (if applicable) — Official full names only.

### Quality Checks:
- Every bullet leads with an action verb
- At least 60% of bullets contain a quantified result
- Summary includes job title and top 2–3 keywords
- No tables, columns, text boxes, or fancy formatting
- All required qualifications addressed somewhere in the document
- Top 10 JD keywords appear at least once

---

## Phase 7: Collaborative Review

Present the full resume to the user, then ask:
- "Does the summary feel accurate to how you'd describe yourself?"
- "Are there any accomplishments I missed that would strengthen this?"
- "Any bullets you'd want to reframe or soften?"
- "Does the overall story make sense for this move?"

Incorporate feedback and revise as needed. Repeat until the user is satisfied.

---

## Phase 8: Output Files

**Step 0 — Get today's date:**
```bash
date +%Y.%m.%d
```

Use the naming convention `YYYY.MM.DD [Company]-[Role]-Resume` (e.g., `2026.02.25 Solovis-DirectorAI-Resume`). Keep the slug short with no spaces.

**Determine the output path based on the access mode from Phase 0:**
- **LOCAL or BOTH** → save to `mnt/` (the user's connected folder)
- **DRIVE_ONLY, PASTE, or URL** → save to the session working directory (e.g., `./outputs/`); use `present_files` to give the user access to download

---

### Step 1: Save the Markdown file

Write the final resume to `OUTPUT_PATH/YYYY.MM.DD [Company]-[Role]-Resume.md`.

---

### Step 2: Create the Word document (.docx)

Read `mnt/.skills/skills/docx/SKILL.md` (if available) for formatting guidance. Build an ATS-safe `.docx` — Calibri or Arial 10–11pt, clean section headers, no tables, columns, or text boxes. Save to `OUTPUT_PATH/YYYY.MM.DD [Company]-[Role]-Resume.docx`.

---

### Step 3: Create the PDF

Read `mnt/.skills/skills/pdf/SKILL.md` (if available) for guidance. Save to `OUTPUT_PATH/YYYY.MM.DD [Company]-[Role]-Resume.pdf`.

**Note on PDF generation:** If the `write_pdf` tool fails with a path error (common on FUSE-mounted paths), fall back to `reportlab`:
```bash
pip install reportlab --break-system-packages -q
# then build via Python script
```

---

### Step 4: Present all three files

Use the `present_files` tool:
- `OUTPUT_PATH/YYYY.MM.DD [Company]-[Role]-Resume.md`
- `OUTPUT_PATH/YYYY.MM.DD [Company]-[Role]-Resume.docx`
- `OUTPUT_PATH/YYYY.MM.DD [Company]-[Role]-Resume.pdf`

Tell the user: "Your resume is ready in three formats — submit the **.docx** to ATS systems, and the **.pdf** for email or direct submissions."

Also offer: "Would you like me to add the accomplishments used here to your experience vault?"
