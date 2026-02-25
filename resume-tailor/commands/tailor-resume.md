---
description: Tailor your resume to a specific job description
allowed-tools: Read, Write, Glob, Bash, WebFetch, WebSearch, Task, mcp__cowork__request_cowork_directory, mcp__cowork__present_files
argument-hint: [job-description-url-or-paste-below]
---

You are running the `/tailor-resume` command. Your goal is to produce a tailored, ATS-optimized, and compelling resume for a specific job. Work through these phases carefully.

The user's argument (if provided) is: $ARGUMENTS

---

## Phase 1: Gather the Job Description

If $ARGUMENTS contains a URL, use WebFetch to retrieve the job description from that URL.

If $ARGUMENTS contains pasted text (not a URL), treat it as the job description directly.

If $ARGUMENTS is empty, ask the user: "Please paste the job description below, or share the URL to the posting."

Once you have the job description, confirm you've captured it by stating the job title and company name.

---

## Phase 2: Load the Experience Vault

Search for a file named `experience-vault.md` using Glob with pattern `**/experience-vault.md` (no path prefix — the working directory is the current session folder, which contains the `mnt/` folder).

If found, copy the file to `/tmp/experience-vault.md` using Bash before reading it (required to avoid FUSE filesystem deadlocks on Google Drive for Desktop files):
```bash
cp "PATH_TO_FILE" /tmp/experience-vault.md
```
Then read from `/tmp/experience-vault.md`. This is the primary source of accomplishments and career history.

If not found, say: "I didn't find an experience vault yet. I'll work from your source resumes instead. You can build your vault anytime with `/update-profile`."

---

## Phase 3: Load Source Resumes from Local Drive

The workspace folder (`mnt/`) is the user's Google Drive for Desktop folder synced locally — all file types are accessible directly as a regular filesystem.

**Step 1 — Find resume files.** Use Glob to search for likely resume files:
- `mnt/**/*.md` — markdown resumes
- `mnt/**/*.docx` — Word documents
- `mnt/**/*.pdf` — PDFs

Look for files with names containing "resume", "cv", or the user's name. Skip any file that looks like an output you already created in a prior run (e.g., files ending in `-Resume.md`).

**Step 2 — Read the files.** For each relevant file found:

- **`.md` files**: Copy to `/tmp/` first to avoid FUSE deadlocks, then read:
  ```bash
  cp "mnt/path/to/file.md" /tmp/source-resume.md
  ```
  Then use the Read tool on `/tmp/source-resume.md`.

- **`.docx` files**: Copy to `/tmp/`, then extract text via Python:
  ```bash
  cp "mnt/path/to/file.docx" /tmp/source-resume.docx
  pip install python-docx --break-system-packages -q
  python3 -c "
  import docx
  doc = docx.Document('/tmp/source-resume.docx')
  for p in doc.paragraphs:
      if p.text.strip():
          print(p.text)
  "
  ```

- **`.pdf` files**: Copy to `/tmp/`, then extract text via Python:
  ```bash
  cp "mnt/path/to/file.pdf" /tmp/source-resume.pdf
  pip install pdfplumber --break-system-packages -q
  python3 -c "
  import pdfplumber
  with pdfplumber.open('/tmp/source-resume.pdf') as pdf:
      for page in pdf.pages:
          print(page.extract_text() or '')
  "
  ```

**If no files are found or the folder isn't mounted yet**, use `mcp__cowork__request_cowork_directory` to ask the user to select their resumes folder, then re-run the Glob search.

Consolidate all experience from the vault + source resumes into a working profile in your context.

---

## Phase 4: Research the Company

Using WebSearch, research the target company:
1. Search for the company name + "mission," "values," and recent news
2. Look for recent press releases, funding announcements, or product launches
3. Search for the company on Glassdoor or LinkedIn for culture signals

Synthesize what you find into a brief intel summary: what is this company focused on right now, what do they value, and what does success in this role likely look like beyond the JD?

---

## Phase 5: Analyze the Job Description

Apply the full JD analysis framework from the resume-expert skill:

1. Extract and categorize the top 10–15 keywords (Technical Skills, Domain Knowledge, Methodologies, Soft Skills)
2. Identify required vs. preferred qualifications
3. Read between the lines: what is this role really about? What signals does the language send about the team's situation and culture?
4. Map the user's experience to each requirement
5. Identify any gaps and determine how to handle them

Present a brief **Job Intel Report** to the user (5–8 bullets) covering:
- What this role is really about
- The top keywords to target
- Interesting company context
- Your recommended positioning angle
- Any gaps worth flagging

Ask: "Does this read right to you? Is there anything about your background or goals I should factor in before I start writing?"

Wait for the user's response before proceeding.

---

## Phase 6: Write the Tailored Resume

Using all gathered context, write a fully tailored resume:

### Structure (in order):
1. **Header** — Name, email, phone, LinkedIn URL, city/state (no full street address)
2. **Professional Summary** — 3–4 lines, tailored to this specific role. Include the target job title or close variant, 2–3 priority keywords, and a distinctive value statement. Mirror the JD's language and energy.
3. **Work Experience** — Ordered chronologically (most recent first). For each role: company name, title, dates (Month Year – Month Year), location (City, ST or Remote). 4–6 bullets per recent role, 2–3 for older roles. Lead every bullet with a strong action verb. Quantify impact. Order bullets within each role by relevance to THIS job (most relevant first, not just most impressive).
4. **Skills** — Single-column or simple comma list. Pull from keyword inventory. Include tools, platforms, methodologies, and domain expertise.
5. **Education** — Degree, field, institution, year. Place after Work Experience unless this is a role where credentials lead (academic, legal, medical).
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

Present the full resume to the user.

Then ask targeted review questions:
- "Does the summary feel accurate to how you'd describe yourself?"
- "Are there any accomplishments I missed that would strengthen this?"
- "Any bullets you'd want to reframe or soften?"
- "Does the overall story make sense for this move?"

Incorporate feedback and revise as needed. Repeat until the user is satisfied.

---

## Phase 8: Output Files

Once the user approves the final resume, produce all three output files. Save them directly into the workspace folder (`mnt/`) — this is the user's Google Drive folder and is where they'll find the files.

Use the naming convention `[Company]-[Role]-Resume` (e.g., `Solovis-DirectorAI-Resume`). Keep it short with no spaces.

### Step 1: Save the Markdown file

Use the Write tool to save the final resume as `mnt/[Company]-[Role]-Resume.md`. This is the source-of-truth file and takes only seconds — do it first.

### Step 2: Create the Word document (.docx)

Read `mnt/.skills/skills/docx/SKILL.md` for formatting instructions, then produce a professionally formatted Word document saved as `mnt/[Company]-[Role]-Resume.docx`.

This is the primary ATS submission format. Use clean, ATS-safe formatting: standard fonts (Calibri or Arial 10–11pt), clear section headers, no tables, no columns, no text boxes, no graphics.

### Step 3: Create the PDF

Read `mnt/.skills/skills/pdf/SKILL.md` for instructions, then produce a clean PDF saved as `mnt/[Company]-[Role]-Resume.pdf`.

This is for email attachments and direct submissions where PDF is accepted.

**Note on PDF generation:** The `write_pdf` tool cannot write directly to Google Drive mount paths. If it fails with a path error, use `reportlab` via a Python script instead:
```bash
pip install reportlab --break-system-packages -q
python3 /path/to/build-pdf.py
```

### Step 4: Present all three files

Use the `present_files` tool to share all three files with the user:
- `mnt/[Company]-[Role]-Resume.md`
- `mnt/[Company]-[Role]-Resume.docx`
- `mnt/[Company]-[Role]-Resume.pdf`

Tell the user: "Your resume is ready in three formats — submit the **.docx** to ATS systems, and the **.pdf** for email or direct submissions."

Also offer: "Would you like me to add the accomplishments used here to your experience vault?"
